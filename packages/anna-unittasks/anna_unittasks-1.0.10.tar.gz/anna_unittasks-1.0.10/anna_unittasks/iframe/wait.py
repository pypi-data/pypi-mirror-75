from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Wait(AbstractTask):
	def __execute__(self):
		events.scroll_to(self.driver, '#iframe-test-wait')
		events.click(self.driver, '#iframe-test-wait')
		events.wait(self.driver, '#iframe-test-wait-get')

	def after_execute(self):
		self.assert_element_exists('#iframe-test-wait-get')
