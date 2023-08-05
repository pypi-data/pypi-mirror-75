from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Submit(AbstractTask):
	def __execute__(self):
		events.scroll_to(self.driver, '#iframe-test-submit')
		events.submit(self.driver, '#iframe-test-submit')

	def after_execute(self):
		self.assert_element_exists('.iframe-submitted')
