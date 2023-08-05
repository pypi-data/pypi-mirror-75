from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class SwitchTo(AbstractTask):
	def __execute__(self):
		events.switch_to(self.driver, '#test-switch-to')

	def after_execute(self):
		self.result.append({'passed': True})
