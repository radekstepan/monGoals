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
        # validate
        error = []
        if 'name' not in request.form or not request.form['name']: error.append('Goal name is missing')
        if 'file' not in request.files or not request.files['file']: error.append('Reward image file is missing')

        if not error:
            # meta
            goal = {'name': request.form['name'], 'description': request.form['description'], 'status': 'active'}

            # dates
            goal['date'] = {
                'begin': utils.timestamp_new(),
                'end': utils.timestamp_new(
                        year = request.form['due-date[year]'],
                        month = request.form['due-date[month]'],
                        day = request.form['due-date[day]'])
            }

            goal['reward'] = utils.file_to_mongo(request.files['file'])
            goal['variant'] = request.form['variant']
            goal['log'] = []

            # points system
            if goal['variant'] == 'points':
                # validate
                if 'points[target]' not in request.form or not request.form['points[target]']:
                    error.append('Target amount of points is missing')
                if 'points[name-0]' not in request.form or not request.form['points[name-0]']:
                    error.append('At least one currency activity is missing')

                if not error:
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
                # validate
                if 'values[begin]' not in request.form or not request.form['values[begin]']:
                    error.append('A starting value is missing')
                if 'values[end]' not in request.form or not request.form['values[end]']:
                    error.append('A target value is missing')
                if 'target[points]' not in request.form or not request.form['target[points]']:
                    error.append('Target amount of points is missing')

                if not error:
                    goal['values'] = {
                        'begin': float(request.form['values[begin]']),
                        'end': float(request.form['values[end]']),
                        'current': float(request.form['values[begin]'])
                    }
                    goal['points'] = {
                        'target': int(request.form['target[points]']),
                        'logged': 0,
                        'conversion': (float(request.form['values[end]']) - float(request.form['values[begin]'])) / float(request.form['target[points]']),
                        'unit': request.form['unit']
                    }

            if not error:
                # save
                g = Goals()
                id = g.save(goal)

                return redirect(url_for('goals.goal', id=id))

    g = Goals()
    goals = utils.sort_list_by_points(g.to_list(g.find_all()))
    fibonacci = [1,2,3,5,8,13,20]
    return render_template('new.html', **locals())

@goals.route('/goal/<id>')
def goal(id):
    '''goal detail'''
    g, m = Goals(), Meta()

    goal = g.find_one(id)
    meta = m.from_log(goal['log'])
    print meta

    return render_template(goal['variant']+'-goal.html', **locals())

@goals.route('/goal/<id>/log', methods=['GET', 'POST'])
def log(id):
    '''log progress on a goal'''
    g = Goals()
    goal = g.find_one(id)
    if goal:
        if request.method == 'POST':
            error = []
            
            # fetch the log
            log = goal['log']
            if goal['variant'] == 'value':
                # validate
                if 'value' not in request.form or not request.form['value']: error.append('New value is missing')

                if not error:
                    if not log: # difference from the beginning
                        points = (float(request.form['value']) - goal['values']['begin']) / goal['points']['conversion']
                    else: # difference from last log
                        points = (float(request.form['value']) - log[-1]['value']) / goal['points']['conversion']
                    entry = {
                        'value': round(float(request.form['value']), 1),
                        'points': round(points, 1),
                        'description': request.form['description'],
                        'date': utils.timestamp_new(
                            year = request.form['date[year]'],
                            month = request.form['date[month]'],
                            day = request.form['date[day]'])
                    }
            else:
                entry = {
                    'points': goal['points']['currency'][int(request.form['points'])]['points'],
                    'name': goal['points']['currency'][int(request.form['points'])]['name'],
                    'description': request.form['description'],
                    'date': utils.timestamp_new(
                        year = request.form['date[year]'],
                        month = request.form['date[month]'],
                        day = request.form['date[day]'])
                }

            if not error:
                # append to the log
                log.append(entry)

                # sort (yeah, not smart when already sorted)
                log = utils.sort_list(log)

                # update current value on the last entry (by date, not actual entry)
                if goal['variant'] == 'value':
                    g.update(id, 'values.current', log[-1]['value'])

                # update the entry
                g.update(id, 'log', log)
                # increment running total of logged points
                g.increment(id, 'points.logged', entry['points'])

                return redirect(url_for('goals.goal', id=id))

        date = utils.date_list(utils.timestamp_new())
        return render_template(goal['variant']+'-log.html', **locals())
    else:
        return redirect(url_for('goals.all'))

@goals.route('/goal/<id>/remove')
@goals.route('/goal/<id>/delete')
def remove(id):
    '''remove'''
    g = Goals()
    g.remove(id)
    return redirect(url_for('goals.all'))

@goals.route('/goal/<id>/archive')
@goals.route('/goal/<id>/close')
@goals.route('/goal/<id>/hide')
def archive(id):
    '''hide from main page'''
    g = Goals()
    g.update(id, 'status', 'archived')
    return redirect(url_for('goals.all'))

@goals.route('/goal/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    '''goal detail'''
    g = Goals()
    goal = g.find_one(id)

    if request.method == 'POST':
        error = []

        # change name, description, due date and reward file
        if 'name' in request.form and request.form['name']:
            goal['name'] = request.form['name']
        if 'description' in request.form and request.form['description']:
            goal['description'] = request.form['description']
        if 'file' in request.files and request.files['file']:
            goal['reward'] = utils.file_to_mongo(request.files['file'])

        goal['date']['end'] = utils.timestamp_new(
                year = request.form['due-date[year]'],
                month = request.form['due-date[month]'],
                day = request.form['due-date[day]'])

        # two different systems
        if goal['variant'] == 'value': # target value

            # validate
            if 'values[begin]' not in request.form or not request.form['values[begin]']:
                error.append('A starting value is missing')
            if 'values[end]' not in request.form or not request.form['values[end]']:
                error.append('A target value is missing')
            if 'target[points]' not in request.form or not request.form['target[points]']:
                error.append('Target amount of points is missing')

            # change the values
            if not error:
                goal['values']['begin'] = float(request.form['values[begin]'])
                goal['values']['end'] = float(request.form['values[end]'])

                goal['points']['target'] = int(request.form['target[points]'])
                goal['points']['conversion'] = (float(request.form['values[end]']) - float(request.form['values[begin]'])) / float(request.form['target[points]'])
                goal['points']['unit'] = request.form['unit']

        else: # points
            pass

        if not error:
            # update
            g.replace(goal['_id'], goal)

            return redirect(url_for('goals.goal', id=id))

    goals = utils.sort_list_by_points(g.to_list(g.find_all()))
    date = utils.date_list(goal['date']['end'])

    return render_template(goal['variant']+'-edit.html', **locals())