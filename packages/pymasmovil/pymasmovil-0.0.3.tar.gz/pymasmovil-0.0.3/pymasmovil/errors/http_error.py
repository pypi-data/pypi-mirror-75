class HTTPError(Exception):

    def __init__(self, error):
        self.status_code = error['statusCode']
        self.fields = error['fields']
        self.message = error['message']
