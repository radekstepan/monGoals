#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module
from flask import render_template, request, redirect
from flask.helpers import url_for

from models.goals import Goals
import utils

goals = Module(__name__)

@goals.route('/')
def all():
    return render_template('main.html', elmo="elmo")

@goals.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # meta
        goal = {'name': request.form['name'], 'description': request.form['description']}

        # dates
        goal['date'] = {
            'begin': utils.timestamp_new(),
            'end': utils.timestamp_new(
                    year = request.form['due-date[year]'],
                    month = request.form['due-date[month]'],
                    day = request.form['due-date[day]'])
        }

        goal['reward'] = request.form['file']
        goal['variant'] = request.form['variant']

        # points system
        if goal['variant'] == 'points':
            points = {
                'target': int(request.form['points[target]']),
                'currency': [] }

            for n in range(10):
                if 'points[name-'+str(n)+']' in request.form and len(request.form['points[name-'+str(n)+']']) > 0:
                    currency = {
                        'name': request.form['points[name-'+str(n)+']'],
                        'points': int(request.form['points[currency-'+str(n)+']']) }
                    points['currency'].append(currency)

            goal['points'] = points

        # target value system
        else:
            goal['target'] = {
                'current': request.form['target[current]'],
                'end': request.form['target[end]'] }

        # save
        g = Goals()
        id = g.save(goal)

        return redirect(url_for('goals.goal', id=id))
    else:
        fibonacci = [1,2,3,5,8,13,20]
        return render_template('new.html', **locals())

@goals.route('/goal/<id>')
def goal(id):
    g = Goals()
    goal = g.find_one(id)
    return render_template('goal.html', goal=goal)

@goals.route('/log')
def log():
    return render_template('log.html', elmo="elmo")