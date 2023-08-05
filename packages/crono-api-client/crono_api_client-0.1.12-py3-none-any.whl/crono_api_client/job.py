import os
import requests

from crono_api_client import utils

API_URL = os.getenv('CRONO_API_URL')
API_KEY = os.getenv('CRONO_API_KEY')

class Job:

	headers = {'Authorization': f'Bearer {API_KEY}'}

	def __init__(self, trigger=None, task=None):
		self.trigger = trigger
		self.task = task
		self.sent = False

	def send(self):

		if self.sent == False and self.task != None and self.trigger != None:
			url = f'{API_URL}/jobs'
			json = {'task': self.task, 'trigger': self.trigger}
			response = requests.post(url, headers=Job.headers, json=json)

			if response.status_code != requests.codes.ok:
				return False

			self.sent = True
			return response.json()
		
		return self

	# Jobs

	@classmethod
	def jobs(cls):
		url = f'{API_URL}/jobs'
		response = requests.get(url, headers=Job.headers)

		if response.status_code != requests.codes.ok:
			return False
		
		return response.json()

	@classmethod
	def job(cls, uuid):
		url = f'{API_URL}/jobs/{uuid}'
		response = requests.get(url, headers=Job.headers)
		
		if response.status_code != requests.codes.ok:
			return False

		return response.json()		

	@classmethod
	def delete(cls, uuid):
		url = f'{API_URL}/jobs/{uuid}'
		response = requests.delete(url, headers=Job.headers)

		if response.status_code != requests.codes.ok
			return False
		
		return response.json()

	# Tasks

	def log(self, *args, **kwargs):
		self.task = {'name': 'log', 'args': args, 'kwargs': kwargs}
		return self.send()

	def request(self, *args, **kwargs):
		self.task = {'name': 'request', 'args': args, 'kwargs': kwargs}
		return self.send()

	def message(self, *args, **kwargs):
		self.tas = {'name': 'message', 'args': args, 'kwargs': kwargs}
		return self.send()

	def email(self, *args, **kwargs):
		self.task = {'name': 'email', 'args': args, 'kwargs': kwargs}
		return self.send()

	# Triggers

	def on(self, datetime_):
		self.trigger = triggers.on(datetime_)
		return self.send()

	def after(self, hours=None, minutes=None, seconds=None):
		self.trigger = triggers.after(hours=hours, minutes=minutes, seconds=seconds)
		return self.send()

	def every(self, hours=None, minutes=None, seconds=None):
		self.trigger = triggers.every(hours=hours, minutes=minutes, seconds=seconds)
		return self.send()

	def cron(self, expression):
		self.trigger = triggers.cron(expression)
		return self.send()
