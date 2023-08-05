from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Select(AbstractTask):
	def __execute__(self):
		events.click(self.driver, '$xpath//select[@name="xpath"]/option[@value="option"]')

	def after_execute(self):
		self.result.append({'passed': True})
