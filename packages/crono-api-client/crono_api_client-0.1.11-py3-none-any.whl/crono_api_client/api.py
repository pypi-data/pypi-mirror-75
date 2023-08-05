from crono_api_client import job as _job

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

def on(*args, **kwargs):
	return _job.Job(trigger={'name': 'on', 'args': args, 'kwargs': kwargs})

def after(*args, **kwargs):
	return _job.Job(trigger={'name': 'after', 'args': args, 'kwargs': kwargs})

def every(*args, **kwargs):
	return _job.Job(trigger={'name': 'every', 'args': args, 'kwargs': kwargs})

def cron(*args, **kwargs):
	return _job.Job(trigger={'name': 'cron', 'args': args, 'kwargs': kwargs})

def at(*args, **kwargs):
	return _job.Job(trigger={'name': 'at', 'args': args, 'kwargs': kwargs})
