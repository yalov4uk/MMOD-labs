from collections import Counter

import numpy as np
from matplotlib import pyplot as plt


class Statistic(object):
    def __init__(self, requests, phases):
        self.requests = requests
        self.phases = phases

    def show_requests_stats(self):
        self._show_requests_end_intervals()
        self._show_requests_durations()
        self._show_failure_percent()

    def _show_requests_end_intervals(self):
        intervals = np.array([])
        time_ends = [request.time_end for request in self.requests if request.time_end is not None]
        time_ends.sort()
        last_time_end = time_ends.pop(-1)
        for time_end in reversed(time_ends):
            interval = last_time_end - time_end
            last_time_end -= interval
            intervals = np.append(intervals, interval)
        print '3.2 Intervals: M = {}, D = {}'.format(intervals.mean(), intervals.std() ** 2)
        plt.hist(intervals, normed=True)
        plt.title('Intervals')
        plt.show()

    def _show_requests_durations(self):
        durations = np.array([
            request.time_end - request.time_start for request in self.requests if request.time_end is not None
        ])
        print '3.3 Durations: M = {}, D = {}'.format(durations.mean(), durations.std() ** 2)
        plt.hist(durations, normed=True)
        plt.title('Durations')
        plt.show()

    def _show_failure_percent(self):
        total_requests_count = len(self.requests)
        failure_requests_count = len([1 for request in self.requests if request.time_end is None])
        print '3.4 Probability fail = {}%'.format(failure_requests_count / float(total_requests_count))

    def show_phases_stats(self):
        print '3.5'
        for i, phase in enumerate(self.phases):
            print 'Phase {}'.format(i + 1)
            print '\tAverage number of requests in hoarder = {}'.format(np.array(phase.requests_in_hoarder).mean())
            for j, channel in enumerate(phase.channels):
                print '\tChannel {}'.format(j + 1)
                for key, count in dict(Counter(channel.checked_states)).iteritems():
                    print '\t\tState {} => part {}'.format(key + 1,
                                                           round(count / float(len(channel.checked_states)), 4))
