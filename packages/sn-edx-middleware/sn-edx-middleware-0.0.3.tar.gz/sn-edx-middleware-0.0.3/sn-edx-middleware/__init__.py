from os import environ


class SkillsNetworkEdxMiddleware(object):
    """
    Middleware to report errors to Skills Network staff
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):  # pragma: no cover
        self.process_request(request)
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, e)
            raise
        return self.process_response(request, response)

    def process_request(self, request):
        print("processing request")

    def process_response(self, request, response):
        print(environ)
        print(environ.get("RELEASE_NAME"))
        print("processing response")
        return response

    def process_exception(self, request, exception):
        print("processing exception")
