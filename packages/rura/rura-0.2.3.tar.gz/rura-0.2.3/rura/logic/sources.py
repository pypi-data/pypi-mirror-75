class Sources:
    RUNNER = None

    @classmethod
    def __get_list(cls, item):
        if 'source' in item:
            sources = item['source']
        elif 'sources' in item:
            sources = item['sources']
        else:
            raise ValueError('Sources not defined for this item.')

        if not isinstance(sources, list):
            sources = [sources]

        return [cls.__get_info(source) for source in sources]

    @classmethod
    def __get_info(cls, source):
        if source.startswith('data:'):
            return {
                'type': 'dataset',
                'title': source.replace('data:', ''),
            }

        pipeline = cls.RUNNER.config['pipelines'][cls.RUNNER.current_pipeline_name]
        model_sub = None
        if ':' in source:
            parts = source.split(':')
            source = parts[0]
            model_sub = parts[1]

        for item in pipeline:
            if item['hash'] == source:
                return {
                    'type': item['type'],
                    'title': source,
                    'config': item,
                    'run_id': model_sub,
                }

        raise ValueError('Unable to find the source.')

    @classmethod
    def get_sources(cls, item, dictionary):
        sources = cls.__get_list(item)

        data = []
        for source in sources:
            if source['title'] in dictionary:
                if source['run_id'] is None:
                    raise ValueError('No run_id specified for source: ' + source['config']['hash'])
                data.append(dictionary[source['title']][source['run_id']])
            elif source['type'] == 'dataset':
                data.append(cls.RUNNER.get_dataset(source['title']))
            else:
                raise ValueError('Unable to find current source: ' + str(source))

        return data
