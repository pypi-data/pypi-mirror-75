from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class SendKeys(AbstractTask):
	def __execute__(self):
		events.scroll_to(self.driver, '#iframe-test-send-keys')
		events.send_keys(driver=self.driver, target='#iframe-test-send-keys', value='iframe_test_send_keys')

	def after_execute(self):
		self.assert_element_exists('.iframe_test_send_keys')
