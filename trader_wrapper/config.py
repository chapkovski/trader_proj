class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Params(AttrDict):
    tick_frequency = 5
    max_length = 10
    round_length = tick_frequency * max_length
    starting_price = 10
    crash_probabilities = [0.01, 0.02, 0.03, 0.05, 0.02]
    game_rounds = len(crash_probabilities)
    training_rounds = [1]
    exchange_rate = 0.05
    assert (game_rounds - len(
        training_rounds)) % 2 == 0, 'Number of payble rounds should be even (so we can split them into gamified and nongamified'
