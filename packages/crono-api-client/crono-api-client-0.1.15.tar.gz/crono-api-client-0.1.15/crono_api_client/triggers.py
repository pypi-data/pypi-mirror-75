import datetime

def on(datetime_):
	
	if datetime_.tzinfo:
		datetime_ = datetime_.astimezone(tz=datetime.timezone.utc)

	return {
		'name': 'on',
		'args': [
			datetime_.isoformat()
		]
	}

def after(hours=None, minutes=None, seconds=None):
	return {
		'name': 'after',
		'kwargs': {
			'hours': int(hours),
			'minutes': int(minutes),
			'seconds': int(seconds)
		}
	}

def every(hours=None, minutes=None, seconds=None):
	return {
		'name': 'every',
		'kwargs': {
			'hours': int(hours),
			'minutes': int(minutes),
			'seconds': int(seconds)
		}
	}

def cron(expression):
	return {
		'name': 'cron',
		'args': [
			str(expression)
		]
	}
