from anna_lib.task.abstract_task import AbstractTask


class Click(AbstractTask):
    def before_execute(self):
        self.timeout = 1

    def __execute__(self):
        self.scroll_to('#iframe-test-click')
        self.click('#iframe-test-click')

    def after_execute(self):
        self._assert('element_exists', '.iframe-clicked')
