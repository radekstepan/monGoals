#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module
from flask import render_template, request, redirect
from flask.helpers import url_for

from models.goals import Goals

import time
from datetime import date

goals = Module(__name__)

@goals.route('/')
def all():
    return render_template('main.html', elmo="elmo")

@goals.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        goal = {'name': request.form['name'], 'description': request.form['description']}

        goal['date'] = {'begin': date.today(), 'end': date(
                int(request.form['due-date[year]']),
                int(request.form['due-date[month]']),
                int(request.form['due-date[day]']))}

        goal['variant'] = request.form['variant']

        if goal['variant'] == 'points':
            points = {
                'target': request.form['points[target]'],
                'currency': [] }

            for n in range(10):
                if 'points[name-'+str(n)+']' in request.form and len(request.form['points[name-'+str(n)+']']) > 0:
                    currency = {
                        'name': request.form['points[name-'+str(n)+']'],
                        'points': int(request.form['points[currency-'+str(n)+']']) }
                    points['currency'].append(currency)

            goal['points'] = points
            
        else:
            goal['target'] = {
                'current': request.form['target[current]'],
                'end': request.form['target[end]'] }

        print goal

        return redirect(url_for('goals.goal'))
    else:
        fibonacci = [1,2,3,5,8,13,20]
        return render_template('new.html', **locals())

@goals.route('/goal')
def goal():
    if (True):
        return render_template('goal.html')
    else:
        return redirect(url_for('goals.detail'))

@goals.route('/log')
def log():
    return render_template('log.html', elmo="elmo")