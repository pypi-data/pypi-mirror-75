from anna_lib.selenium import events, util, assertions
from anna_lib.task.abstract_task import AbstractTask


class Remove(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.click(self.driver, target='a.showcart')
		if util.get_element(self.driver, target='#mini-cart > li.product-item.item.product'):
			events.hover(self.driver, target='li.product-item.item.product')
		if util.get_element(self.driver, target='.delete'):
			events.click(self.driver, target='.delete')
		if util.get_element(self.driver, target='.action-accept'):
			events.click(self.driver, target='.action-accept')

	def after_execute(self):
		pass
