class Transformer:
    @staticmethod
    def transform(transformer):
        if transformer.is_complete():
            # transformer.load_files()
            # transformer.load()
            print('Skipping transformer ' + '/'.join(transformer.path) + '; already exists.')
            return

        for source in transformer.sources:
            source.load_files()
            source.load()

        dataset = transformer.sources[0]

        print('Running transformer ' + '/'.join(transformer.path) + '...')
        if transformer.all_files:
            file_names = ['train_x', 'train_y', 'val_x', 'val_y', 'test_x', 'test_y']
            files = transformer.transform(dataset.get_data(file_names), None)
            for file, data in zip(file_names, files):
                transformer.save_data(file, 'npy', data)
        else:
            for data_type in ['train', 'val', 'test']:
                file = data_type
                if data_type not in dataset.files:  # TODO - Figure out how to do this better in the future
                    for f in dataset.files:
                        if f.startswith(data_type):
                            file = f
                            break
                result = transformer.transform(dataset.get_data(file), data_type)
                if transformer.has_y:
                    x, y = result
                    transformer.save_data(data_type + '_y', transformer.output_type, y)
                else:
                    x = result

                transformer.save_data(data_type + '_x', transformer.output_type, x)

        print('Done!')
