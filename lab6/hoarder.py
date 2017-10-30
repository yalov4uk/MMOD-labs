class Hoarder(object):
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
