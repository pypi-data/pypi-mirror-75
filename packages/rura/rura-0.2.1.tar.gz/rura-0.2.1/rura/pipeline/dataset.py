from rura.pipeline.base import Base
from rura.utils.dataset import split_patients
from rura.utils.file import read_file
import os


class Dataset(Base):
    def __init__(self, version, files, **kwargs):
        super().__init__(**kwargs)
        self.version = version
        self.files = files
        self._get_files()

    def load(self):
        pass

    def _get_files(self):
        pass

    def get_path(self, file=None):
        path = super().get_path(file=file)
        if file is None:
            return path

        if self.version is not None:
            parts = os.path.splitext(path)
            return parts[0] + '.v' + str(self.version) + parts[1]

        return path

    # def get_data(self, name):
    #     if isinstance(name, list):
    #         return tuple([read_file(self.get_path(file), self.files[file]) for file in name])
    #
    #     if name not in self.files:  # TODO - Is this an ok long term solution?
    #         for file in self.files.keys():
    #             if file.startswith(name):
    #                 name = file
    #                 break
    #
    #     return read_file(self.get_path(name), self.files[name])

    def make(self):
        raise NotImplementedError

    def make_files(self, split):
        df = self.make()
        if split is not None:
            if isinstance(split, dict):
                seed = split.get('seed', 3)
            else:
                seed = 3
            df_train, df_val, df_test = split_patients(df, seed=seed)
            df_train = df_train.reset_index()
            df_val = df_val.reset_index()
            df_test = df_test.reset_index()

            print('Train/Val/Test Suicide Patient Counts')
            print(df_train.groupby('PatientID')['Output'].max().sum())
            print(df_val.groupby('PatientID')['Output'].max().sum())
            print(df_test.groupby('PatientID')['Output'].max().sum())

            df_train.to_feather(self.get_path('train'))
            df_val.to_feather(self.get_path('val'))
            df_test.to_feather(self.get_path('test'))
        else:
            raise NotImplementedError
