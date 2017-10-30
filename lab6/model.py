from copy import deepcopy

import numpy as np
from scipy.stats import expon

from channel import Channel
from hoarder import Hoarder
from phase import Phase
from request import Request
from statistic import Statistic


class Model(object):
    def __init__(self, phases_settings):
        self.phases = [Phase(
            channels=[
                Channel(deepcopy(phase_settings['channel_dist']))
                for _ in xrange(phase_settings['channels_count'])
            ],
            hoarder=Hoarder(volume=phase_settings['hoarder_volume']),
        ) for phase_settings in phases_settings]

    def emulate_work(self, time_delta, requests_total_count):
        current_time = 0.0
        requests = []
        time_to_next_req_gen = self._get_time_req_gen(expon(scale=2.0), requests_total_count)
        time_to_next_req = 0
        rejected_requests = 0
        while np.any([not phase.is_free() for phase in self.phases]) or time_to_next_req_gen.has_next():
            while time_to_next_req == 0 and time_to_next_req_gen.has_next():
                requests.append(Request(time_start=current_time))
                if self.phases[0].has_place_for_request():
                    self.phases[0].send_request(requests[-1])
                else:
                    rejected_requests += 1
                time_to_next_req = round(time_to_next_req_gen.next(), 2)
            for i, phase in reversed(list(enumerate(self.phases))):
                waiting_channels = phase.move(time_delta)
                if i is not len(self.phases) - 1:
                    while self.phases[i + 1].has_place_for_request() and len(waiting_channels) > 0:
                        channel = waiting_channels.pop(waiting_channels.index(
                            min(waiting_channels, key=lambda channel: channel.request.time_start)
                        ))
                        request = channel.take_request()
                        self.phases[i + 1].send_request(request)
                else:
                    for channel in waiting_channels:
                        request = channel.take_request()
                        request.time_end = current_time
            current_time = round(current_time + time_delta, 2)
            if time_to_next_req > 0:
                time_to_next_req = round(time_to_next_req - time_delta, 2)
            if current_time % 1000 == 0:
                print '{}%'.format(len(requests) / float(requests_total_count))
        print '3.1 Requests process = {}, Current time = {}'.format(len(requests), current_time)
        return Statistic(requests=requests, phases=self.phases), current_time

    def _get_time_req_gen(self, dist, N):
        class gen:
            def __init__(self, dist, N):
                self.dist = dist
                self.N = N
                self.req_count = 0

            def has_next(self):
                return self.req_count < self.N

            def next(self):
                if self.has_next():
                    self.req_count += 1
                    return dist.rvs(size=1)[0]

        return gen(dist, N)
