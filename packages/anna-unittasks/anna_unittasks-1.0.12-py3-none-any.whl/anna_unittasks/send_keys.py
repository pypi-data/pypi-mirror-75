from anna_lib.task.abstract_task import AbstractTask


class SendKeys(AbstractTask):
	def __execute__(self):
		self.send_keys(target='#test-send-keys', value='test_send_keys')

	def after_execute(self):
		self._assert('element_exists', '.test_send_keys')
