import importlib
import inspect


class ClassDef:
    @staticmethod
    def get_package(item):
        if item['type'] == 'dataset':
            return 'src.data'
        elif item['type'] == 'transform':
            return 'src.features'
        elif item['type'] == 'model':
            return 'src.models'

        raise ImportError('Unknown type.')

    @classmethod
    def get_class(cls, item):
        package = cls.get_package(item)
        func = item['func']
        base = item.get('base', None)
        if base is None:
            builder = importlib.import_module('._base.' + func, package=package)
        else:
            builder = importlib.import_module('.' + base + '.' + func, package=package)

        for m in inspect.getmembers(builder, inspect.isclass):
            class_def = m[1]
            if class_def.__module__.startswith(package):
                return class_def

        raise ImportError('Unable to find the class definition.')
