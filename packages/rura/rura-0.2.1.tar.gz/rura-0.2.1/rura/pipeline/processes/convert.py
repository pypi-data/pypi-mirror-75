from rura.pipeline.process import Process
from rura.utils.file import save_file


class TrainConvertProcess(Process):
    def train(self, model):
        # Get the train and val data
        x_train, x_val, x_test = model.sources[0].get_data(['train_x', 'val_x', 'test_x'])

        model.set_parameters_data(x_train, None, x_val, None, x_test, None)

        # Build the model
        model.build()

        # Officially log parameters
        model.log_parameters()

        # Fit the model (send validation as an optional parameter since some models dont use it)
        model.fit(x_train, None, x_val=x_val, y_val=None)

        model.fit_metrics(x_train, None, x_val=x_val, y_val=None)

        model.log_model()
        return model

    def run(self, model):
        trained_model = self.train(model)
        self.convert(trained_model)

    def convert(self, model):
        x_train, x_val, x_test = model.sources[0].get_data(['train_x', 'val_x', 'test_x'])
        for data_type, data in zip(['train', 'val', 'test'], [x_train, x_val, x_test]):
            # TODO - Change this to also be a model.save_data() similar to transform ability
            save_file(model.get_path(data_type + '_x.npy'), 'npy', model.predict(data))
