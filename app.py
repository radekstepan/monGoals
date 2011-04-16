#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Flask

import utils

def create_app(database, drop=False):
    # create our little application :)
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.secret_key = 'DtJe0TW8ZQqLWT7UVE7alBN6vxxI6xBCDjVbcgY3'

    # db import
    from db import init_connection, table_drop

    # db setup
    init_connection(database)
    # db cleanup?
    if drop:
        table_drop('goals')

    # presenters
    from presenters.goals import goals

    # register modules
    app.register_module(goals)

    # template filters
    @app.template_filter('timestamp_format')
    def timestamp_format(timestamp):
        return utils.timestamp_format(timestamp)

    return app

if __name__ == '__main__':
    app = create_app(database='mongoals')
    app.run(port=5002)
