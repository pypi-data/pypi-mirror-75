from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class NotRequired(AbstractTask):
	def before_execute(self):
		self.required = False

	def __execute__(self):
		events.click(self.driver, '.some-element-that-isn\'t-clickable')

	def after_execute(self):
		pass
