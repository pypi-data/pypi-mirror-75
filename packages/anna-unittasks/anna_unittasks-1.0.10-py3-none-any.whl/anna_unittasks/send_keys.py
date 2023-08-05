from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class SendKeys(AbstractTask):
	def __execute__(self):
		events.send_keys(driver=self.driver, target='#test-send-keys', value='test_send_keys')

	def after_execute(self):
		self.assert_element_exists('.test_send_keys')
