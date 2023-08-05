from anna_lib.selenium import events, util, assertions
from anna_lib.task.abstract_task import AbstractTask


class Add(AbstractTask):
	def before_execute(self):
		events.click(self.driver, target='#btn-cookie-allow')

	def __execute__(self):
		events.click(self.driver, target='#search')
		events.send_keys(self.driver, target='#search', value='Magni')
		events.submit(self.driver, target='#search')
		events.click(self.driver, target='.category-item-link')
		events.scroll_to(self.driver, target='.category-view')
		events.hover(self.driver, target='a.product-item-photo')
		events.click(self.driver, target='.tocart')

	def after_execute(self):
		self.result.append(assertions.element_exists(self.driver, target='.message-success'))
		events.click(self.driver, target='.mfp-close')
