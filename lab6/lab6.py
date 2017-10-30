from numpy.random import normal, triangular

from model import Model


class Lab6(object):
    """
    Variant 13
    """

    def __init__(self):
        self.generator1 = lambda: normal(loc=5, scale=1)
        self.generator2 = lambda: triangular(left=3, right=8, mode=(3 + 8) / 2.0)
        self.generator3 = lambda: normal(loc=7, scale=2)

    def run(self):
        model = Model(
            phases_settings=[
                {'channels_count': 3, 'channel_dist': self.generator1, 'hoarder_volume': 2},
                {'channels_count': 4, 'channel_dist': self.generator2, 'hoarder_volume': 3},
                {'channels_count': 4, 'channel_dist': self.generator3, 'hoarder_volume': 3},
            ],
        )

        model_stats, total_time = model.emulate_work(
            time_delta=0.01,
            requests_total_count=10000,
        )

        model_stats.show_requests_stats()
        model_stats.show_phases_stats()
