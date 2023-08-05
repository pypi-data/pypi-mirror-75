from anna_lib.task.abstract_task import AbstractTask


class Wait(AbstractTask):
	def __execute__(self):
		self.click('#test-wait')
		self.wait('#test-wait-get')

	def after_execute(self):
		self._assert('element_exists', '#test-wait-get')
