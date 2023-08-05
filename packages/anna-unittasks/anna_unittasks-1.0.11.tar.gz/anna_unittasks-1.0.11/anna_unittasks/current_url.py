from anna_lib.task.abstract_task import AbstractTask


class CurrentUrl(AbstractTask):
	def __execute__(self):
		self.click('#test-current-url')

	def after_execute(self):
		self._assert('in_url', 'test/switchto')
