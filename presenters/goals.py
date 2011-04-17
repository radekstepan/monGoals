#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module
from flask import render_template, request, redirect
from flask.helpers import url_for

from models.goals import Goals
from models.meta import Meta
from models.progress import Progress

import utils

goals = Module(__name__)

@goals.route('/')
def all():
    '''list all goals'''
    g, m, p = Goals(), Meta(), Progress()

    goals = g.to_list(g.find_all())
    for goal in goals:
        m.from_log(goal['log'])
        p.add_log(goal['log'])
    meta = m.meta
    progress_all = p.sort_log()

    return render_template('main.html', goals=goals, meta=meta, progress_all=progress_all)

@goals.route('/new', methods=['GET', 'POST'])
def new():
    '''create new goal'''
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
        goal['log'] = []

        # points system
        if goal['variant'] == 'points':
            points = {
                'target': int(request.form['points[target]']),
                'logged': 0,
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
    '''goal detail'''
    g, m = Goals(), Meta()

    goal = g.find_one(id)
    meta = m.from_log(goal['log'])

    return render_template('goal.html', **locals())

@goals.route('/goal/<id>/log', methods=['GET', 'POST'])
def log(id):
    '''log progress on a goal'''
    g = Goals()
    goal = g.find_one(id)
    if goal:
        if request.method == 'POST':
            entry = {
                'points': goal['points']['currency'][int(request.form['points'])],
                'description': request.form['description'],
                'date': utils.timestamp_new(
                    year = request.form['date[year]'],
                    month = request.form['date[month]'],
                    day = request.form['date[day]'])
            }
            
            log = goal['log']
            log.append(entry)

            g.update(id, 'log', log)
            g.increment(id, 'points.logged', entry['points']['points'])

            return redirect(url_for('goals.goal', id=id))
        else:
            return render_template('log.html', **locals())
    else:
        return redirect(url_for('goals.all'))