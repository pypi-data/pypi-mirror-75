from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Hover(AbstractTask):
	def __execute__(self):
		events.scroll_to(self.driver, '#iframe-test-hover')
		events.hover(self.driver, '#iframe-test-hover')

	def after_execute(self):
		self.assert_element_exists('.iframe-hovered')
