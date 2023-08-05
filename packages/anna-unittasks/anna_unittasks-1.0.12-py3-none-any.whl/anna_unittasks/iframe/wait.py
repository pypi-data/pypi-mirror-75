from anna_lib.task.abstract_task import AbstractTask


class Wait(AbstractTask):
	def before_execute(self):
		self.timeout = 5

	def __execute__(self):
		self.scroll_to('#iframe-test-wait')
		self.click('#iframe-test-wait')
		self.wait('#iframe-test-wait-get')

	def after_execute(self):
		self._assert('element_exists', '#iframe-test-wait-get')
