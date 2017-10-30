import numpy as np

from const import CHANNEL_FREE, CHANNEL_WAIT, CHANNEL_WORK


class Phase(object):
    def __init__(self, channels, hoarder):
        self.channels = channels
        self.hoarder = hoarder
        self.requests_in_hoarder = []

    def is_free(self):
        return self.hoarder.is_empty() and np.all([channel.state is CHANNEL_FREE for channel in self.channels])

    def has_place_for_request(self):
        return self.hoarder.has_free_volume()

    def send_request(self, request):
        self.hoarder.send_request(request)

    def move(self, time_delta):
        self.requests_in_hoarder.append(len(self.hoarder.requests))
        waiting_channels = []
        for channel in self.channels:
            channel.checked_states.append(channel.state)
            if channel.state is CHANNEL_WAIT:
                waiting_channels.append(channel)
            elif channel.state is CHANNEL_WORK:
                if channel.move(time_delta):
                    waiting_channels.append(channel)
            else:
                if not self.hoarder.is_empty():
                    channel.send_request(self.hoarder.requests.pop(0))
        return waiting_channels
