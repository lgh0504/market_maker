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
class trading_engine():
    def __init__(self):
        self.openOrders = order_database()
        self.closedOrders = order_database()

# The order database will keep track of all orders and will store them in a table
# The first table will contain a list of all of the orders made, and store them
# in the following columns: uuid | price | size | filled? | date | time
class order_database():
    def __init__(self):
        # Create a new database
        self.orderDb = data_processor.db_manager("orderDb")
        self.orderDb.create_table("orders",
                                  ['uuid', 'price', 'size', 'filled', 'date', 'time'],
                                  ['TEXT', 'REAL', 'REAL', 'INTEGER', 'TEXT', 'TEXT'])

    # Get an order by ID
    def get_order_by_ID(self, uuid):
        return self.orderDb.get_line_for_param("orderDb", ['uuid', uuid]))

    # Insert an order into the db
    def insert_order(self, uuid, price, size, filled, date, time):
        self.orderDb.insert_entry("orderDb", [uuid, price, size, filled, date, time])

    # Delete an order by ID
    def delete_order(self, uuid):
        self.orderDb.get_line_for_param("orderDb", ['uuid', uuid])
        
