from rura.utils.paths import DATA_PROCESSED, DATA_INTERIM
from rura.utils.file import read_file
import os


class Base:
    def __init__(self, path, folder=DATA_PROCESSED, sources=None):
        self.folder = folder

        self.sources = sources

        self.files = {}
        self.path = path

    def load(self):
        raise NotImplementedError

    def load_files(self):
        for file in os.listdir(self.get_path()):
            parts = os.path.splitext(file)
            self.files[parts[0]] = parts[1].replace('.', '')

    def get_path(self, file=None):
        path = os.path.join(self.folder, *self.path)
        if not os.path.exists(path):
            os.makedirs(path)

        if file is None:
            return path

        if file not in self.files:
            return os.path.join(path, file)

        return os.path.join(path, file + '.' + self.files[file])

    def get_data(self, file, allow_none=False):
        if not isinstance(file, list):
            return read_file(self.get_path(file), self.files[file])

        data = []
        for f in file:
            if f not in self.files:
                if allow_none:
                    data.append(None)
                    continue
                raise FileNotFoundError('Unable to find file: ' + f)

            data.append(read_file(self.get_path(f), self.files[f]))

        return data

    def is_complete(self):
        if self.files is None or len(self.files.keys()) == 0:  # TODO - This is temp for transform and model
            return len(list(os.listdir(self.get_path()))) > 0

        for file in self.files:
            if not os.path.exists(self.get_path(file)):
                return False

        # TODO - Delete old files if they exist

        return True
