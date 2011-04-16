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
    '''list all goals'''
    return render_template('main.html', elmo="elmo")

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
    g = Goals()
    goal = g.find_one(id)
    meta = __meta(goal['log'])
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

def __meta(log):
    '''calculate the progress past today, 7 days, 30 days'''
    # find out cutoff times for time-frames (x2 for % progress)
    now = utils.timestamp_new()
    meta = {
        'today': {
            'current': {
                'cutoff': now - (60*60*24),
                'points': 0
            },
            'previous': {
                'cutoff': now - (60*60*24*2),
                'points': 0
            },
        },
        'seven': {
            'current': {
                'cutoff': now - (60*60*24*7),
                'points': 0
            },
            'previous': {
                'cutoff': now - (60*60*24*7*2),
                'points': 0
            },
        },
        'thirty': {
            'current': {
                'cutoff': now - (60*60*24*30),
                'points': 0
            },
            'previous': {
                'cutoff': now - (60*60*24*30*2),
                'points': 0
            },
        },
    }

    # traverse all log entries...
    for entry in log:
        p = entry['points']['points']
        if entry['date'] > meta['today']['current']['cutoff']:
            meta['today']['current']['points'] += p
            meta['seven']['current']['points'] += p
            meta['thirty']['current']['points'] += p
        else:
            if entry['date'] > meta['today']['previous']['cutoff']:
                meta['today']['previous']['points'] += p
                meta['seven']['current']['points'] += p
                meta['thirty']['current']['points'] += p
            else:
                if entry['date'] > meta['seven']['current']['cutoff']:
                    meta['seven']['current']['points'] += p
                    meta['thirty']['current']['points'] += p
                else:
                    if entry['date'] > meta['seven']['previous']['cutoff']:
                        meta['seven']['previous']['points'] += p
                        meta['thirty']['current']['points'] += p
                    else:
                        if entry['date'] > meta['thirty']['current']['cutoff']:
                            meta['thirty']['current']['points'] += p
                        elif entry['date'] > meta['thirty']['previous']['cutoff']:
                            meta['thirty']['previous']['points'] += p
    return meta