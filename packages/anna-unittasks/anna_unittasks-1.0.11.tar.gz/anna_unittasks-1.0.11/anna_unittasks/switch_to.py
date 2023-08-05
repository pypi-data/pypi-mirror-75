from anna_lib.task.abstract_task import AbstractTask


class SwitchTo(AbstractTask):
	def __execute__(self):
		self.switch_to('#test-switch-to')

	def after_execute(self):
		self.result.append({'passed': True})
