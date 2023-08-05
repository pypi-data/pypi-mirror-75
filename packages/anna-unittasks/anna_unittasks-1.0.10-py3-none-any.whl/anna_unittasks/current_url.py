from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class CurrentUrl(AbstractTask):
	def __execute__(self):
		events.click(self.driver, '#test-current-url')

	def after_execute(self):
		self.assert_in_url('test/switchto')
