from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Click(AbstractTask):
	def __execute__(self):
		events.click(self.driver, '#test-click')

	def after_execute(self):
		self.assert_element_exists('.clicked')
