from rura.pipeline.base import Base
from rura.utils.file import save_file


class Transform(Base):
    def __init__(self, all_files=False, output_type='npy', has_y=True, **kwargs):
        super().__init__(**kwargs)
        self.all_files = all_files
        self.output_type = output_type
        self.has_y = has_y

    def load(self):
        pass

    def transform(self, data, data_type):
        raise NotImplementedError

    def save_data(self, file, file_type, data):
        save_file(self.get_path(file + '.' + file_type), file_type, data)
        self.files[file] = file_type
