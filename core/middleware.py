from models import HttpLogEntry


class HttpLogMiddleware:
    def process_request(self, request):
        log_entry = HttpLogEntry(url=request.path)
        log_entry.save()
