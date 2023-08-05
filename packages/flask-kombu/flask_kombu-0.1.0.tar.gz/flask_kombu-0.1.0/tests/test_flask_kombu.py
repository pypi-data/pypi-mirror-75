#!/usr/bin/env python

"""Tests for `flask_kombu` package."""
from unittest.mock import Mock

from flask import Flask
from kombu import Exchange

from flask_kombu import Kombu


def test_integration():
    app = Flask(__name__)
    app.config["AMQP_URI"] = "amqp://guest:guest@localhost:5672/"
    ko = Kombu()
    ko.init_app(app=app)

    assert "kombu" in app.extensions


def test_send():
    app = Flask(__name__)
    app.config["AMQP_URI"] = "amqp://guest:guest@localhost:5672/"
    ko = Kombu()
    ko.init_app(app=app)
    ko.producer.channel = Mock()
    ko.send("something", exchange=Exchange('foo'), delivery_mode='transient')

    assert ko.producer._channel.basic_publish.call_args[1]['exchange'], 'foo'
