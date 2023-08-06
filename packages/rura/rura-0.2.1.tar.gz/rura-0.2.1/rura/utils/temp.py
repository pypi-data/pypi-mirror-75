from rura.utils.paths import TEMP
import datetime
import os


def get_temp_file_path(ext):
    if not os.path.exists(TEMP):
        os.makedirs(TEMP)

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    return os.path.join(TEMP, 'temp-' + suffix + '.' + ext)
