from rura.pipeline.processes.temp import TempProcess
from rura.tracker import Tracker
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import mlflow


class SuicideProcess(TempProcess):
    def extra_metrics(self, model, x, y, data_type):
        preds = model.predict(x, data_type=data_type)

        self.__save_pr_curve(model, y, preds, data_type)
        self.__save_probs(model, preds, data_type)
        self.__class_reports(model, y, preds, data_type)

    def __class_reports(self, model, y_true, y_pred, data_type):
        y_pred = np.round(y_pred).flatten()

        report = classification_report(y_true, y_pred, output_dict=True)
        for m in ['precision', 'recall', 'f1-score']:
            for c in ['0', '1', 'macro avg', 'weighted avg']:
                if c in report:
                    mlflow.log_metric(data_type + '_' + m + '_c' + c, report[c][m])
                else:
                    mlflow.log_metric(data_type + '_' + m + '_c' + c, np.nan)

        with open(self.get_output_path(model, file='class_reports.txt'), 'a') as w:
            w.write('\n')
            w.write(data_type + '\n')
            w.write(classification_report(y_true, y_pred))
            w.write('\n\n')

        mlflow.log_artifact(self.get_output_path(model, file='class_reports.txt'))

    def __save_probs(self, model, y_pred, data_type):
        y_pred = y_pred.flatten()

        plt.hist(y_pred, color='steelblue')
        plt.title(data_type + ' Prediction Probabilities')
        plt.savefig(self.get_output_path(model, file=data_type + '_probs_hist.png'))
        plt.clf()
        mlflow.log_artifact(self.get_output_path(model, file=data_type + '_probs_hist.png'))

    def __save_pr_curve(self, model, y_true, y_pred, data_type):
        y_pred = y_pred.flatten()

        from sklearn.metrics import precision_recall_curve, average_precision_score, roc_auc_score
        from inspect import signature

        precision, recall, _ = precision_recall_curve(y_true, y_pred)
        average_precision = average_precision_score(y_true, y_pred)
        roc_auc = roc_auc_score(y_true, y_pred)

        if Tracker.IS_LOGGING:
            mlflow.log_metric(data_type + '_auc', roc_auc)
            mlflow.log_metric(data_type + '_auc_pr', average_precision)

        # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
        step_kwargs = ({'step': 'post'}
                       if 'step' in signature(plt.fill_between).parameters
                       else {})
        plt.step(recall, precision, color='b', alpha=0.2,
                 where='post')
        plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('Precision-Recall Curve: AP={0:0.2f}; AUC={0:0.2f}'.format(average_precision, roc_auc))
        plt.savefig(self.get_output_path(model, file=data_type + '_pr_curve.png'))
        plt.clf()
        mlflow.log_artifact(self.get_output_path(model, file=data_type + '_pr_curve.png'))
