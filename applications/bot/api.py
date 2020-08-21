from tornado import escape
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from textfier.tasks import CausalLanguageModelingTask

# Usage of padding text helps XLNet with short seeds
# Proposed by Aman Rusia in https://github.com/rusiaaman/XLNet-gen#methodology
PADDING = '''In 1991, the remains of Russian Tsar Nicholas II and his family
(except for Alexei and Maria) are discovered.
The voice of Nicholas's young son, Tsarevich Alexei Nikolaevich, narrates the
remainder of the story. 1883 Western Siberia,
a young Grigori Rasputin is asked by his father and a group of men to perform magic.
Rasputin has a vision and denounces one of the men as a horse thief. Although his
father initially slaps him for making such an accusation, Rasputin watches as the
man is chased outside and beaten. Twenty years later, Rasputin sees a vision of
the Virgin Mary, prompting him to become a priest. Rasputin quickly becomes famous,
with people, even a bishop, begging for his blessing. <eod> </s> <eos>'''


class GeneratorHandler(RequestHandler):
    """Handles the text generation requests.

    """

    def initialize(self, **kwargs):
        """Initializes the handler.

        """

        # Defines the task as a property
        self.task = kwargs['task']

    def post(self):
        """Requested used to handle POST and generate the artificial text.

        """

        # Decodes the body looking for information
        body = escape.json_decode(self.request.body)

        # Parses the message
        seed = body.get('seed', None)

        # Verifies if its a string
        if not isinstance(seed, str):
            # Raises error if not
            raise RuntimeError('seed should be a string')

        print(f'Generating text with seed: {seed}')

        # Encodes the input
        inputs = self.task.tokenizer.encode(
            PADDING + seed, add_special_tokens=False, return_tensors='pt')

        # Gathers the length of padded input
        length = len(self.task.tokenizer.decode(
            inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))

        # Performs the generation
        outputs = self.task.model.generate(
            inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)

        # Decodes the generation outputs
        generated = seed + task.tokenizer.decode(outputs[0])[length:]

        print(f'Text generated.')

        # Writes back the response
        self.write(dict(result=generated))


class Server(Application):
    """Holds the server.

    """

    def __init__(self, task):
        """Initializes the application.

        Args:
            task (textfier.core.Task): Textfier's task.

        """

        # Default handlers
        handlers = [
            (r'/', GeneratorHandler, dict(task=task))
        ]

        # Bootstraps the server
        Application.__init__(self, handlers, debug=True, autoreload=True)


if __name__ == '__main__':
    print('Starting server ...')

    # Creates a pre-defined casual modeling task
    task = CausalLanguageModelingTask(model='xlnet-base-cased')

    try:
        print(f'Port: 8080')

        # Creates an application
        app = HTTPServer(Server(task=task))

        # Servers the application on desired port
        app.listen(8080)

        # Starts a IOLoop instance
        IOLoop.instance().start()

    except KeyboardInterrupt:
        exit()
