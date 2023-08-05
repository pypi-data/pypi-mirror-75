from anna_lib.task.abstract_task import AbstractTask


class Click(AbstractTask):
	def __execute__(self):
		self.click('#test-click')

	def after_execute(self):
		self._assert('element_exists', '.clicked')
