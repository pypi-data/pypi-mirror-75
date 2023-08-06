import json
import sys, traceback, os
from typing import List

from anna_client.client import Client

import anna.colors as colors
from anna_lib.selenium import driver
from anna_lib.task.abstract_task import AbstractTask
from anna_lib.task import factory


class Worker:
	tasks: List
	task: AbstractTask
	api: bool

	def _log(self, message: str):
		print(message)
		self.log += message

	def __init__(self, args: dict):
		self.passed = None
		self.driver = None
		self.args = args
		self.api = False
		if self.args['resolution'] is None:
			self.args['resolution'] = (1920, 1080)
		else:
			self.args['resolution'] = tuple(int(a) for a in self.args['resolution'].split('x'))

		if 'id' in self.args:
			self.id = self.args['id']
		if self.args['host'] is None and 'ANNA_HOST' in os.environ:
			self.args['host'] = os.environ['ANNA_HOST']
		self.api = self.args['host'] is not None and len(self.args['host']) > 0
		self.client = Client(endpoint=self.args['host'])
		if 'ANNA_TOKEN' in os.environ:
			self.client.inject_token(os.environ['ANNA_TOKEN'])
		if 'token' in self.args and self.args['token'] is not None and len(self.args['token']) > 0:
			self.client.inject_token(self.args['token'])
		self.url, self.tasks = self.get_tasks(namespace=self.args['site'])
		if self.api:
			self.client.update_jobs(where={'id': self.id}, data={'tasks_total': len(self.tasks),
			                                                     'tasks_passed': 0,
			                                                     'status': 'RUNNING'
			                                                     })
		self.task_results = []
		self.log = ''

	def close(self):
		self.driver.close()

	def run(self):
		self.driver = driver.create(driver=self.args['driver'], headless=self.args['headless'],
									resolution=self.args['resolution'])
		self.driver.get(self.url)
		for task in self.tasks:
			name, task = factory.load_task(self.driver, task)
			self.execute_task(self.url, name, task)
			self.task_results.append(task)
			if self.api:
				self.client.update_jobs(where={'id': self.id},
				                        data={'tasks_passed': len([t for t in self.task_results if t.passed]), 'log': '""' + self.log + '""'})
		self.complete()

	def execute_task(self, url, name, task):
		self.task = task
		self._log('Running %s @ %s on %s' % (name, url, self.driver.name))
		try:
			task.execute()
		except KeyboardInterrupt:
			return
		except:
			self.handle_exception(task)
		self.screenshot(name)
		if task.passed:
			self._log(colors.green + 'passed' + colors.white)
		else:
			self.passed = False
			self._log(colors.red + 'failed' + colors.white)

	def complete(self):
		passed = len([task for task in self.task_results if task.passed])
		if self.passed is None:
			self.passed = passed == len(self.task_results) and len(self.task_results) == len(self.tasks)
		self.update_job()
		self.print_result()

	def update_job(self):
		if self.api:
			if self.passed:
				self.client.update_jobs(where={'id': self.id}, data={'status': 'DONE', 'log': '""' + self.log + '""'})
			else:
				self.client.update_jobs(where={'id': self.id}, data={'status': 'FAILED', 'log': '""' + self.log + '""'})

	def print_result(self):
		if self.args['verbose']:
			self.print_task_summary()
		passed = len([task for task in self.task_results if task.passed])
		self._log(str(passed) + '/' + str(len(self.task_results)))

	def print_task_summary(self):
		self._log(colors.red)
		for task in self.task_results:
			self.print_task_result(task)
		self._log(colors.white)

	def print_task_result(self, task):
		if not task.passed:
			self._log('\n' + json.dumps(task.result))

	def handle_exception(self, task):
		task.passed = False
		task.result = traceback.format_exc()
		self._log('\n' + traceback.format_exc())
		if self.args['verbose']:
			traceback.print_exc(file=sys.stdout)

	def screenshot(self, name):
		screenshot_dir = self.get_screenshot_dir()
		try:
			os.makedirs(screenshot_dir)
		except FileExistsError:
			pass
		except IOError:
			return False
		file = screenshot_dir + '/' + name + '.png'
		return self.driver.get_screenshot_as_file(file)

	@staticmethod
	def get_screenshot_dir():
		return '/tmp/anna/'

	def get_tasks(self, namespace):
		if self.api:
			return self.client.get_tasks(namespace)
		return factory.get_tasks(namespace)

