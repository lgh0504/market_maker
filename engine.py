# This is the trading engine that makes all of the trading decisions
# Created on March 8th, 2018
# By Izak Fritz

import wrapper
import data_processor

# The engine will be incharge of processing all previous trades, balances,
# orders and cancellations
# It will broken into various parts:
# Order Placement and Cancellation
# Order Sizing
# Mode of Market Making (Aggressive vs. Passive)
# Reporting
class tradingEngine():
    def __init__(self):
        self.orderManager = orderManager()

# The order database will keep track of all orders and will store them in a table
# The first table will contain a list of all of the orders made, and store them
# in the following columns: uuid | price | size | filled? | date | time
class orderManager():
    def __init__(self):
        # Create a databse with two tables to manage open orders and closed orders
        self.orderDb = data_processor.db_manager("openOrderDb")
        self.orderDb.create_table("open",
                                  ['uuid', 'price', 'size', 'filled', 'date', 'time'],
                                  ['TEXT', 'REAL', 'REAL', 'INTEGER', 'TEXT', 'TEXT'])
        self.orderDb.create_table("closed",
                                  ['uuid', 'price', 'size', 'filled', 'date', 'time'],
                                  ['TEXT', 'REAL', 'REAL', 'INTEGER', 'TEXT', 'TEXT'])

    # Get an order by ID
    def get_order_by_ID(self, uuid, open):
        if (open == 1):
            return self.openOrderDb.get_line_for_param("open", ['uuid', uuid]))
        else:
            return self.closedOrderDb.get_line_for_param("closed", ['uuid', uuid]))

    # Insert an order into the db
    def insert_order_to_db(self, uuid, price, size, filled, date, time, open):
        if (open == 1):
            self.orderDb.insert_entry("open", [uuid, price, size, filled, date, time])
        else:
            self.orderDb.insert_entry("closed", [uuid, price, size, filled, date, time])

    # Delete an order by ID
    def delete_order(self, uuid, open):
        if (open == 1):
            self.orderDb.get_line_for_param("open", ['uuid', uuid])
        else:
            self.orderDb.get_line_for_param("closed", ['uuid', uuid])
