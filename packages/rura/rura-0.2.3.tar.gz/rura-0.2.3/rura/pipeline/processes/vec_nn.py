from rura.pipeline.process import Process


class VecNNProcess(Process):
    # TODO - Remove this class by making the regular training process automatically make any y values be None
    def run(self, model):
        # Get the train and val data
        x_train, y_train, x_val, y_val, x_test, y_test = model.sources[0].get_data(
            ['train_x', 'train_y', 'val_x', 'val_y', 'test_x', 'test_y'])

        # Set parameters dynamically
        model.set_parameters_data(x_train, y_train, x_val, y_val, x_test, y_test)

        # Build the model
        model.build()

        # Officially log parameters
        model.log_parameters()

        # Fit the model (send validation as an optional parameter since some models dont use it)
        model.fit(x_train, y_train, x_val=x_val, y_val=y_val)

        model.fit_metrics(x_train, x_train, x_val=x_val, y_val=y_val)

        model.log_model()
