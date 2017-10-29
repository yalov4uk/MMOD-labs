import numpy as np
from scipy.stats import expon#, uniform, norm, triang
from numpy.random import exponential, normal, triangular, uniform
from collections import Counter
from matplotlib import pyplot as plt
from copy import deepcopy

CHANNEL_FREE = 0
CHANNEL_WORK = 1
CHANNEL_WAIT = 2

uniform_generator = lambda : uniform(low=3, high=9)
norm_generator = lambda : normal(loc=5, scale=1)
triangle_generator = lambda : triangular(left=3, right=9, mode=6)

def main():
    #Variant 1
    model = Model(
        phases_settings=[
            {'channels_count': 3, 'channel_dist': uniform_generator, 'accumulator_volume': 3},
            {'channels_count': 4, 'channel_dist': norm_generator, 'accumulator_volume': 5},
            {'channels_count': 3, 'channel_dist': triangle_generator, 'accumulator_volume': 3},
        ],
    )

    model_stats, total_time = model.emulate_work(
        time_delta=0.01,
        requests_total_count=10000,
    )

    print 'Model work time: {}'.format(total_time)
    model_stats.show_requests_stats()
    model_stats.show_phases_stats()


class Model:
    def __init__(self, phases_settings):
        self.phases = [Phase(
            channels=[
                Channel(deepcopy(phase_settings['channel_dist']))
                for _ in xrange(phase_settings['channels_count'])
            ],
            accumulator=Accumulator(volume=phase_settings['accumulator_volume']),
        ) for phase_settings in phases_settings]

    def emulate_work(self, time_delta, requests_total_count):
        current_time = 0.
        requests = []
        time_to_next_req_gen = self._get_time_req_gen(expon(scale=2.), requests_total_count)
        time_to_next_req = 0
        c = 0
        while np.any([not phase.is_free() for phase in self.phases]) or time_to_next_req_gen.has_next():
            while time_to_next_req == 0 and time_to_next_req_gen.has_next():
                requests.append(Request(time_start=current_time))
                if self.phases[0].has_place_for_request():
                    self.phases[0].send_request(requests[-1])
                else:
                    c += 1
                if time_to_next_req_gen.has_next():
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
            if current_time % 500 == 0:
                print current_time, 'model seconds'#, time_to_next_req
            #print len(requests), len([1 for r in requests if r.time_end is not None])
        print 'lost phirst phase', c
        return ModelStatistics(requests=requests, phases=self.phases), current_time

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


class Phase:
    def __init__(self, channels, accumulator):
        self.channels = channels
        self.accumulator = accumulator
        self.requests_in_accum = []

    def is_free(self):
        return self.accumulator.is_empty() and \
            np.all([channel.state is CHANNEL_FREE for channel in self.channels])

    def has_place_for_request(self):
        return self.accumulator.has_free_volume()
               #or np.any([channel.state is CHANNEL_FREE for channel in self.channels])

    def send_request(self, request):
        #if np.any([channel.state is CHANNEL_FREE for channel in self.channels]):
        #    for channel in self.channels:
        #        if channel.state is CHANNEL_FREE:
        #            channel.send_request(request)
        #else:
        self.accumulator.send_request(request)

    def move(self, time_delta):
        self.requests_in_accum.append(len(self.accumulator.requests))
        waiting_channels = []
        for channel in self.channels:
            #print channel.state
            channel.checked_states.append(channel.state)
            if channel.state is CHANNEL_WAIT:
                waiting_channels.append(channel)
            elif channel.state is CHANNEL_WORK:
                if channel.move(time_delta):
                    waiting_channels.append(channel)
            else:
                if not self.accumulator.is_empty():
                    channel.send_request(self.accumulator.requests.pop(0))
        return waiting_channels


class Request:
    def __init__(self, time_start):
        self.time_start = time_start
        self.time_end = None


class Channel:
    def __init__(self, dist):
        self.state = CHANNEL_FREE
        self.work_time_gen = self._get_work_time_gen(dist)
        self.checked_states = []
        self.request = None
        self.work_time = 0.

    def _get_work_time_gen(self, dist):
        while True:
            #yield dist.rvs(size=1)[0]
            yield dist()

    def send_request(self, request):
        self.work_time = round(self.work_time_gen.next(), 2)
        self.request = request
        self.state = CHANNEL_WORK

    def move(self, time_delta):
        if self.work_time == 0:
            if self.request is not None:
                self.state = CHANNEL_WAIT
                return True
            else:
                return False
        else:
            self.work_time = round(self.work_time - time_delta, 2)
            return False

    def take_request(self):
        self.state = CHANNEL_FREE
        request = self.request
        self.request = None
        return request


class Accumulator:
    def __init__(self, volume):
        self.requests_in_counts = []
        self.volume = volume
        self.requests = []

    def is_empty(self):
        return len(self.requests) == 0

    def has_free_volume(self):
        return len(self.requests) < self.volume

    def send_request(self, request):
        self.requests.append(request)


class ModelStatistics:
    def __init__(self, requests, phases):
        self.requests = requests
        self.phases = phases

    def show_requests_stats(self):
        self._show_requests_end_intervals()
        self._show_requests_durations()
        self._show_failure_proccent()

    def _show_requests_end_intervals(self):
        intervals = np.array([])
        time_ends = [request.time_end for request in self.requests if request.time_end is not None]
        time_ends.sort()
        last_time_end = time_ends.pop(-1)
        for time_end in reversed(time_ends):#[:-1]):
            interval = last_time_end - time_end
            last_time_end -= interval
            intervals = np.append(intervals, interval)
        print 'end intervals M: {}, D: {}'.format(intervals.mean(), intervals.std())# ** 2)
        plt.hist(intervals, normed=True)
        plt.show()

    def _show_requests_durations(self):
        durations = np.array([
            request.time_end - request.time_start for request in self.requests
            if request.time_end is not None
        ])
        print 'durations M: {}, D: {}'.format(durations.mean(), durations.std())# ** 2)
        plt.hist(durations, normed=True)
        plt.show()

    def _show_failure_proccent(self):
        total_requests_count = len(self.requests)
        miss_requests_count = len([1 for request in self.requests if request.time_end is None])
        print 'miss requests proccent: {}'.format(miss_requests_count / float(total_requests_count))

    def show_phases_stats(self):
        for i, phase in enumerate(self.phases):
            print 50 * '-'
            print 'phase {}'.format(i + 1)
            print 'Mead requests in accumulator: {}'.format(np.array(phase.requests_in_accum).mean())
            for j, channel in enumerate(phase.channels):
                print 'channel {}'.format(j + 1)
                for key, count in dict(Counter(channel.checked_states)).iteritems():
                    print 'state {} => part {}'.format(key + 1, round(count / float(len(channel.checked_states)), 4))


if __name__ == '__main__':
    main()

phases_settings1 = '''[
                {'channels_count': 3, 'channel_dist': uniform(loc=3, scale=9), 'accumulator_volume': 3},
                            #ravnomern from 3 to 9
                {'channels_count': 4, 'channel_dist': norm(loc=5, scale=1), 'accumulator_volume': 5},
                            #loc == M, scale == D
                {'channels_count': 3, 'channel_dist': triang(c=1, loc=3, scale=9), 'accumulator_volume': 3},
            ],'''
