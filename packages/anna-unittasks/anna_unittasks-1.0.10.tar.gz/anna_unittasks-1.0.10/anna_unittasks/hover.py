from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Hover(AbstractTask):
	def __execute__(self):
		events.hover(self.driver, '#test-hover')

	def after_execute(self):
		self.assert_element_exists('.hovered')
