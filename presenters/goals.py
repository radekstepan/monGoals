#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module
from flask import render_template, request, redirect
from flask.helpers import url_for

from models.goals import Goals

goals = Module(__name__)

@goals.route('/')
def all():
    return render_template('main.html', elmo="elmo")

@goals.route('/new')
def new():
    return render_template('new.html', elmo="elmo")

@goals.route('/goal')
def goal():
    if (True):
        return render_template('goal.html')
    else:
        return redirect(url_for('goals.detail'))

@goals.route('/log')
def log():
    return render_template('log.html', elmo="elmo")