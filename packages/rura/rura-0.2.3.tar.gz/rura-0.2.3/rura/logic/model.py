from rura.pipeline.processes.convert import TrainConvertProcess
from rura.pipeline.processes.suicide import SuicideProcess
from rura.pipeline.processes.temp import TempProcess

from rura.pipeline.processes.vec_nn import VecNNProcess
from rura.tracker import Tracker


class ModelExecute:
    def __init__(self, runner):
        self.runner = runner

    def get_process(self, item):
        process_name = item.get('process', None)
        if process_name == 'TrainConvert':
            return TrainConvertProcess()
        elif process_name == 'VecNN':
            return VecNNProcess()
        elif process_name == 'Suicide':
            return SuicideProcess()

        return TempProcess()

    def run_model(self, item, run, model_class, parameters, execute=True):
        Tracker.setup()
        exp_name = self.runner.analysis_name + ':' + self.runner.current_pipeline_name + ':'
        exp_name += str(item.get('base', 'None')) + ':' + str(item['func']) + ':' + item['hash']
        Tracker.set_experiment(exp_name)

        if execute:
            print('Running model ' + item['hash'] + '...')
        process = self.get_process(item)

        model = model_class(**parameters)

        if not execute:
            return model

        if model.is_complete():
            print('Skipping run ' + run['hash'] + '; already exists.')
            # model.load_files()
            # model.load()
            return model

        # TODO - Save the run_id to the yaml file
        # if Tracker.is_logging():
        run_id = Tracker.start_run(run['hash']).info.run_id

        for source in model.sources:
            source.load_files()
            source.load()

        print('Processing run ' + run['hash'] + '...')
        process.run_id = run['hash']
        process.run(model)

        Tracker.end_run()
        return model

    def evaluate_model(self, item, model, run_hash):
        from mlflow.tracking.client import MlflowClient
        from mlflow.entities import ViewType

        exp_name = self.runner.analysis_name + ':' + self.runner.current_pipeline_name + ':'
        exp_name += str(item.get('base', 'None')) + ':' + str(item['func']) + ':' + item['hash']

        client = MlflowClient()
        experiments = [exp for exp in client.list_experiments() if exp.name == exp_name]
        if len(experiments) == 0 or len(experiments) > 1:
            raise ValueError('Unable to find the experiment.')
        experiment = experiments[0]

        run = client.search_runs(
            experiment_ids=experiment.experiment_id,
            filter_string='tags."mlflow.runName" = ' + "'" + run_hash + "'",
            run_view_type=ViewType.ACTIVE_ONLY,
            max_results=1,
        )[0]

        run_id = run.info.run_id
        Tracker.resume_run(run_id)

        process = self.get_process(item)

        for source in model.sources:
            source.load_files()
            source.load()
        model.load()

        print('Evaluating run ' + run_hash + '...')
        process.run_id = run_hash
        process.evaluate(model)

        Tracker.end_run()
