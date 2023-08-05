from lighter.context import Context
from lighter.decorator import register


class Runner:
    @register(type='experiments.mnist.Experiment', property='experiment')
    def __init__(self):
        pass

    def run(self):
        self.experiment.run()


def exec(config='configs/mnist.config.json'):
    Context.create(config)
    runner = Runner()
    runner.run()
