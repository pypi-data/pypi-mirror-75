from rura.pipeline.process import Process
from rura.utils.paths import RESULTS
import os


class TempProcess(Process):
    def run(self, model):
        # Get the train and val data
        x_train, y_train, x_val, y_val, x_test, y_test = model.sources[0].get_data(
            ['train_x', 'train_y', 'val_x', 'val_y', 'test_x', 'test_y'], allow_none=True)

        # TODO - Rename to compute_parameters_data
        model.set_parameters_data(x_train, y_train, x_val, y_val, x_test, y_test)

        # Build the model
        model.build()

        # Officially log parameters
        # TODO - Auto log stuff from the init function
        model.log_parameters()

        # Fit the model (send validation as an optional parameter since some models dont use it)
        model.fit(x_train, y_train, x_val=x_val, y_val=y_val)

        model.fit_metrics(x_train, y_train, x_val=x_val, y_val=y_val)

        model.log_model()

        if not os.path.exists(self.get_output_path(model)):
            os.makedirs(self.get_output_path(model))

        self.extra_metrics(model, x_train, y_train, 'train')
        self.extra_metrics(model, x_val, y_val, 'val')

    @staticmethod
    def get_output_path(model, file=''):
        return os.path.join(RESULTS, *model.path, file)

    def extra_metrics(self, model, x, y, data_type):
        pass

    def evaluate(self, model):
        for filename in os.listdir(os.path.join(RESULTS, *model.path)):
            if filename.startswith('test_'):
                print('Skipping evaluation due to already evaluated.')
                return

        # Get the test data
        x_test, y_test = model.sources[0].get_data(['test_x', 'test_y'], allow_none=True)
        self.extra_metrics(model, x_test, y_test, 'test')
