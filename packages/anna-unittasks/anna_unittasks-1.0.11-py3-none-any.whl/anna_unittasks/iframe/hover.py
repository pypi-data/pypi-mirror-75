from anna_lib.task.abstract_task import AbstractTask


class Hover(AbstractTask):
	def __execute__(self):
		self.scroll_to('#iframe-test-hover')
		self.hover('#iframe-test-hover')

	def after_execute(self):
		self._assert('element_exists', '.iframe-hovered')
