import time
# class SleepMiddleware(object):

#     def process_request(self, request):
#         time.sleep(5)



class SleepMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        time.sleep(3)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response