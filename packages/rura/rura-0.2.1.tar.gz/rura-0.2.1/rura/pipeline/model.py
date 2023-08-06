from rura.pipeline.base import Base


class Model(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None

    def set_parameters_data(self, x_train, y_train, x_val, y_val, x_test, y_test):
        pass

    def log_parameters(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def fit(self, x_train, y_train, x_val, y_val):
        raise NotImplementedError

    def fit_metrics(self, x_train, y_train, x_val=None, y_val=None):
        raise NotImplementedError

    def log_model(self):
        raise NotImplementedError

    def predict(self, x):
        raise NotImplementedError
