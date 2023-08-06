from rura.utils.file import read_file, save_file
from rura.utils.paths import DATA_EXTERNAL
import os


# TODO - Make the folder allowed to be an array and pull it apart
class ExternalData:
    @staticmethod
    def get_ext(file):
        return os.path.splitext(file)[1][1:]

    @classmethod
    def get_data(cls, folder, file, options={}):
        ext = cls.get_ext(file)
        return read_file(os.path.join(DATA_EXTERNAL, folder, file), ext, options=options)

    @classmethod
    def save_data(cls, folder, file, data):
        ext = cls.get_ext(file)
        save_file(os.path.join(DATA_EXTERNAL, folder), ext, data)
