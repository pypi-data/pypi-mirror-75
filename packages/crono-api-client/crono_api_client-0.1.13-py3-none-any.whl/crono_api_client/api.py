from crono_api_client import job as _job
from crono_api_client import triggers

# Jobs

def jobs(*args, **kwargs):
	return _job.Job.jobs(*args, **kwargs)

def job(*args, **kwargs):
	return _job.Job.job(*args, **kwargs)

def delete(*args, **kwargs):
	return _job.Job.delete(*args, **kwargs)

# Tasks

def log(*args, **kwargs):
	return _job.Job(task={'name': 'log', 'args': args, 'kwargs': kwargs})

def request(*args, **kwargs):
	return _job.Job(task={'name': 'request', 'args': args, 'kwargs': kwargs})

def message(*args, **kwargs):
	return _job.Job(task={'name': 'message', 'args': args, 'kwargs': kwargs})

def email(*args, **kwargs):
	return _job.Job(task={'name': 'email', 'args': args, 'kwargs': kwargs})

# Triggers

def on(datetime_):
	trigger = triggers.on(datetime_)
	return _job.Job(trigger=trigger)

def after(hours=None, minutes=None, seconds=None):
	trigger = triggers.after(hours=hours, minutes=minutes, seconds=seconds)
	return _job.Job(trigger=trigger)

def every(hours=None, minutes=None, seconds=None):
	trigger = triggers.every(hours=hours, minutes=minutes, seconds=seconds)
	return _job.Job(trigger=trigger)

def cron(expression):
	trigger = triggers.cron(expression)
	return _job.Job(trigger=trigger)
