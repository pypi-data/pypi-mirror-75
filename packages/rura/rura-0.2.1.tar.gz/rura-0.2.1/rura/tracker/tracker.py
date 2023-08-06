from rura.utils.paths import PROJECT
from dotenv import load_dotenv
import mlflow
from mlflow.exceptions import RestException
import os


class Tracker:
    URI = None
    USERNAME = None
    PASSWORD = None
    loaded = False
    IS_LOGGING = False
    client = None

    @classmethod
    def __load(cls):
        if cls.loaded:
            return

        path = os.path.join(PROJECT, '.env')
        if not os.path.exists(path):
            raise ValueError('.env file does not exist: ' + str(path))

        load_dotenv(dotenv_path=path)
        cls.URI = os.getenv('TRACKER_URI')
        cls.USERNAME = os.getenv('TRACKER_URI')
        cls.PASSWORD = os.getenv('TRACKER_URI')

    @classmethod
    def setup(cls):
        if not cls.IS_LOGGING:
            return

        if not cls.loaded:
            cls.__load()
            mlflow.set_tracking_uri(cls.URI)
            cls.client = mlflow.tracking.MlflowClient()
            cls.loaded = True

    @classmethod
    def set_experiment(cls, name):
        # if not cls.IS_LOGGING:
        #     return

        mlflow.set_experiment(name)

    @classmethod
    def does_run_exist(cls, run_id):
        if not cls.IS_LOGGING:
            return

        if run_id is None:
            return False

        try:
            cls.client.get_run(run_id)
        except RestException as e:
            if str(e).startswith('RESOURCE_DOES_NOT_EXIST'):
                return False
            else:
                raise e

        return True

    @classmethod
    def get_artifact(cls, run_id, artifact):
        if not cls.IS_LOGGING:
            return

        if not cls.loaded:
            cls.setup()

        cls.client.download_artifacts(run_id, artifact, 'tmp')

    @classmethod
    def resume_run(cls, run_id):
        return mlflow.start_run(run_id=run_id)

    @classmethod
    def start_run(cls, name, nested_id=None):
        # if not cls.IS_LOGGING:
        #     return None

        is_nested = nested_id is not None
        return mlflow.start_run(run_name=name, nested=is_nested)

    @classmethod
    def end_run(cls):
        if not cls.IS_LOGGING:
            return None

        mlflow.end_run()

    @classmethod
    def disable_logging(cls):
        cls.IS_LOGGING = False

    @classmethod
    def enable_logging(cls):
        cls.IS_LOGGING = True

    @classmethod
    def is_logging(cls):
        return cls.IS_LOGGING
