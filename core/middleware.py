from models import HttpLogEntry


class HttpLogMiddleware:
    def process_response(self, request, response):
        log_entry = HttpLogEntry(
            url=request.path,
            method=request.method,
            status_code=response.status_code
        )
        log_entry.save()
        return response
