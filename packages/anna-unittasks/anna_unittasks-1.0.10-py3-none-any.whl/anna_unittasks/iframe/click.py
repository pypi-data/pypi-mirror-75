from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Click(AbstractTask):
	def __execute__(self):
		events.scroll_to(self.driver, '#iframe-test-click')
		events.click(self.driver, '#iframe-test-click')

	def after_execute(self):
		self.assert_element_exists('.iframe-clicked')
