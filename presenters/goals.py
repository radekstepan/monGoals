#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module
from flask import render_template, request, redirect
from flask.helpers import url_for

from models.goals import Goals

goals = Module(__name__)

@goals.route('/goal')
def detail():
    if (True):
        return render_template('detail.html', elmo="elmo")
    else:
        return redirect(url_for('goals.detail'))