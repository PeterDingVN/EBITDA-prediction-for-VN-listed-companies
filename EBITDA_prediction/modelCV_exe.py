from train_test_pipeline import TrainTestPipe

class Execution(TrainTestPipe):
    def __init__(self, data):
        super().__init__(data)
        if 'platform' in self.data.columns.to_list():
            self.data = self.data.drop(columns=['platform'])
        else:
            pass

    def execute(self, n_splits, test_size, test: bool = True):
        if test:
            result = self.hyper_parameter_tuning(n_splits = n_splits, test_size = test_size, test=True)
        else:
            result = self.hyper_parameter_tuning(n_splits = n_splits, test_size = test_size, test=False)
        return result





