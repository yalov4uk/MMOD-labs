from const import CHANNEL_FREE, CHANNEL_WORK, CHANNEL_WAIT


class Channel(object):
    def __init__(self, dist):
        self.state = CHANNEL_FREE
        self.work_time_gen = self._get_work_time_gen(dist)
        self.checked_states = []
        self.request = None
        self.work_time = 0.0

    def _get_work_time_gen(self, dist):
        while True:
            yield dist()

    def send_request(self, request):
        self.work_time = round(self.work_time_gen.next(), 2)
        self.request = request
        self.state = CHANNEL_WORK

    def move(self, time_delta):
        if self.work_time <= 0:
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
