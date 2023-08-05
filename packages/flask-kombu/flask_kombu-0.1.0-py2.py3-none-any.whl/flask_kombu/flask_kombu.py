"""Main module."""

import warnings

from kombu import Connection, Producer


class Kombu:
    connection = None
    producer = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if all([
            "AMQP_URI" not in app.config,
        ]):
            warnings.warn(
                "AMQP_URI is not set."
                "Default AMQP_URI set to amqp://guest:guest@localhost:5672/"
            )
        app.config.setdefault("AMQP_URI", "amqp://guest:guest@localhost:5672/")

        self.connection = Connection(app.config["AMQP_URI"])
        self.producer = Producer(self.connection)
        extensions = getattr(app, "extensions", {})
        extensions['kombu'] = self

    def send(self, body, **kwargs):
        self.producer.publish(body, **kwargs)
