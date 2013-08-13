# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class product_product(osv.osv):
    """ Product Product """
    _name = "product.product"
    _inherit = "product.product"

    def _update_cost_usd(self,cr,uid,ids=None,context=None):

	product_obj = self.pool.get('product.product')
	invoice_obj = self.pool.get('account.invoice')
	invoice_line_obj = self.pool.get('account.invoice.line')
	currency_obj = self.pool.get('res.currency')

	currency_id = currency_obj.search(cr,uid,[('name','=','USD')])
	if not currency_id:
		_logger.debug('USD currency not present in the system. Exiting')
		exit(0)
	currency_rate = 0
	for currency in currency_obj.browse(cr,uid,currency_id):
		currency_rate = currency.rate

	product_ids = product_obj.search(cr,uid,[('id','>',0)])
	
	import pdb;pdb.set_trace()	
	for product in product_obj.browse(cr,uid,product_ids):
		invoice_line_ids = invoice_line_obj.search(cr,uid,[('product_id','=',product.id)])
		for invoice_line in invoice_line_obj.browse(cr,uid,invoice_line_ids):
			if invoice_line.invoice_id.currency_id.id == currency_id[0]:
				price_unit_usd = invoice_line.price_unit * currency_rate
	
				vals_product = {
					'standard_price': price_unit_usd
					}
				return_id = product_obj.write(cr,uid,product.id,vals_product)
				_logger.debug("Updated product " + product.name)
			
		"""
		if product.bom_ids == []:
			vals_cost = {
				'product_id': product.id,
				'date': datetime.today(),
				'name': product.name,
				'cost': product.standard_price,
				}
			product_cost_history_ids = product_cost_history_obj.create(cr,uid,vals_cost)
		else:
			for bom in self.pool.get('mrp.bom').browse(cr,uid,product.bom_ids):
				vals_cost = {
					'product_id': product.id,
					'date': datetime.today(),
					'name': bom.id.name,
					'cost': bom.id.manufacturing_cost,
					}
				product_cost_history_ids = product_cost_history_obj.create(cr,uid,vals_cost)
		"""
	return None

product_product()

