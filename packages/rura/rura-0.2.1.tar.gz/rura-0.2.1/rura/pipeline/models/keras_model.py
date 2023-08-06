import ipykernel  # Importing to make keras logging work
from rura.pipeline import Model
import mlflow.keras
from keras.models import load_model


class KerasModel(Model):
    def log_parameters(self):
        mlflow.keras.autolog()

    def log_model(self):
        # TODO - Add this file to the self.files
        self.model.save(self.get_path('model.h5'))

    def load(self):
        self.model = load_model(self.get_path('model.h5'))
