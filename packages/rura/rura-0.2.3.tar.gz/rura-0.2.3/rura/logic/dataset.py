import importlib


class DatasetMaker:
    def __init__(self, datasets):
        self.datasets = datasets

    # TODO - Check dependencies
    def get_dataset(self, data):
        parts = data.split('/')
        section = parts[0]
        title = parts[1]

        config = self.datasets[section][title]
        if config is None:
            parameters = {}
        else:
            parameters = config.get('parameters', {})
        parameters['path'] = [section, title]
        dataset = importlib.import_module('.' + section + '.make_dataset', package='src.data').MakeDataset(**parameters)

        if not dataset.is_complete():
            print('Making dataset ' + section + '/' + title + '...')
            dataset.make_files(config.get('split', None))
            print('Done!')

        return dataset
