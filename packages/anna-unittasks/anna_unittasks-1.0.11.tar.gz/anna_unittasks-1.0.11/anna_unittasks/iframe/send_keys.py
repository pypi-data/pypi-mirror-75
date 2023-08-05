from anna_lib.task.abstract_task import AbstractTask


class SendKeys(AbstractTask):
	def __execute__(self):
		self.scroll_to('#iframe-test-send-keys')
		self.send_keys(target='#iframe-test-send-keys', value='iframe_test_send_keys')

	def after_execute(self):
		self._assert('element_exists', '.iframe_test_send_keys')
