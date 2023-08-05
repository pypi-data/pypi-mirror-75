from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Wait(AbstractTask):
	def __execute__(self):
		events.click(self.driver, '#test-wait')
		events.wait(self.driver, '#test-wait-get')

	def after_execute(self):
		self.assert_element_exists('#test-wait-get')
