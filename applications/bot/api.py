from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler


class GeneratorHandler(RequestHandler):
    """Handles the text generation requests.

    """

    def initialize(self, **kwargs):
        """Initializes the handler.

        """

        pass

    def post(self):
        """Requested used to handle POST and generate the artificial text.

        """

        # Writes the response
        self.write(dict(result='hello'))


class Server(Application):
    """Holds the server.

    """

    def __init__(self):
        """Initializes the application.

        """

        # Default handlers
        handlers = [
            (r'/', GeneratorHandler)
        ]

        # Bootstraps the server
        Application.__init__(self, handlers, debug=True, autoreload=True)


if __name__ == '__main__':
    print('Starting server ...')

    try:
        print(f'Port: 8080')

        # Creates an application
        app = HTTPServer(Server())

        # Servers the application on desired port
        app.listen(8080)

        # Starts a IOLoop instance
        IOLoop.instance().start()

    except KeyboardInterrupt:
        exit()
