# Copyright (c) 2017, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_customer_open_items_per_sales_order(filters)
	return columns, data

def get_columns():
	return [
			_("Item") + ":Link/Item:350",
			_("Qty") + ":Int:50",
			_("Rate") + ":Currency:100",
			_("Sales Order") + ":Link/Sales Order:120"
	]		

def get_customer_open_items_per_sales_order(filters):
	data = frappe.db.sql("""
		SELECT
			`tabSales Order Item`.item_code, 
			((`tabSales Order Item`.qty - `tabSales Order Item`.returned_qty) * `tabSales Order Item`.rate - `tabSales Order Item`.billed_amt) / `tabSales Order Item`.rate AS open_qty,
			`tabSales Order Item`.rate,
			`tabSales Order Item`.parent
		FROM 
			`tabSales Order Item` 
		INNER JOIN 
			`tabSales Order` on `tabSales Order Item`.parent = `tabSales Order`.name
		WHERE 
			`tabSales Order`.customer = '{0}'
			AND `tabSales Order`.status = 'To Bill'
		""".format(filters.customer))
	
	return data
