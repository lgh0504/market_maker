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
            return self.openOrderDb.get_line_for_param("open", ['uuid', uuid])
        else:
            return self.closedOrderDb.get_line_for_param("closed", ['uuid', uuid])

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

# This class will review API data and give output based on the current market
# It will call the api to find the current ask and bid price to decide the following:
# Aggresive market making or passive market making?
# Our bid price and ask price
class orderPlacement():
    def __init__(self, inCoin1):
        # Store a copy of the current market bid and ask (init as -1)
        self.marketName = str(inCoin1) + "-BTC"
        self.coin1 = str(inCoin1)
        self.lastPrice = None
        self.currentAsk = None
        self.currentBid = None
        self.spread = None
        self.buyTotal = None
        self.sellTotal = None

        # Our data we compute
        self.ourBid = None
        self.ourAsk = None
        self.orderSize = None
        self.tradeAggresive = None # 1 for aggresive buy, 0 for passive, -1 for aggresive sell
        # -2 for very short, -1 for short, 0 for even, 1 for long, 2 for very long
        self.ourPosition = None
        self.btcTotal = None
        self.altTotal = None

        # Retain an instance of an api caller
        self.api = wrapper.bittrex_wrapper()
        self.currentMarketData = self.api.getmarketsummary(self.marketName)
        self.currentBuyBook = self.api.getorderbook(self.marketName, "buy")
        self.currentSellBook = self.api.getorderbook(self.marketName, "sell")

    # Update all of the market data and order books
    def update_data(self):
        self.currentMarketData = self.api.getmarketsummary(self.marketName)
        self.currentBuyBook = self.api.getorderbook(self.marketName, "buy")
        self.currentSellBook = self.api.getorderbook(self.marketName, "sell")
        self.currentAsk = self.currentMarketData['result'][0]['Ask']
        self.currentBid = self.currentMarketData['result'][0]['Bid']
        self.lastPrice = self.currentMarketData['result'][0]['Last']
        self.spread = abs(self.currentAsk - self.currentBid)
        self.buyTotal = 0;
        self.sellTotal = 0;
        for i in range(0, len(self.currentBuyBook['result'])):
            self.buyTotal += self.currentBuyBook['result'][i]['Quantity']
        for i in range(0, len(self.currentSellBook['result'])):
            self.sellTotal += self.currentSellBook['result'][i]['Quantity']

    # Calculate total quantity of altcoin and Bitcoin to deteremine if net long/short
    # Defaults: Very long is defined by greater than 80-20
    # Defaults: Very short is defined by greater than 20-80
    # TODO: Add the ability to change these ratios
    def update_our_position(self):
        tempTotal1 = self.api.getbalance("BTC")
        tempTotal2 = self.api.getbalance(str(self.coin1))
        self.btcTotal = tempTotal1['result']['Balance']
        self.altTotal = tempTotal2['result']['Balance'] / self.lastPrice
        ratio = self.btcTotal / (self.altTotal + self.btcTotal)
        if (ratio >= .8) :
            self.ourPosition = -1
        elif (ratio < .8 and ratio >= .2):
            self.ourPosition = 0
        else:
            self.ourPosition = 1

    # Check if the quantity of orders is over the threshold
    def update_aggressive_or_passive(self, threshold):
        if (threshold < (abs(self.buyTotal - self.sellTotal)/(self.buyTotal + self.sellTotal))):
            self.tradeAggresive = 1
        elif (threshold < (abs(self.sellTotal - self.buyTotal)/(self.buyTotal + self.sellTotal))):
            self.tradeAggresive = -1
        else:
            self.tradeAggresive = 0

    # Calculate buy and sell orders based on aggressive or passive
    def calculate_order_price(self):
        if (self.ourPosition == -1):
            # Very net short, aggressively buy
            self.ourBid = self.lastPrice
            self.ourAsk = self.lastPrice + self.spread
        elif (self.ourPosition == 1):
            # Very net long, aggressively sell
            self.ourBid = self.lastPrice + self.spread
            self.ourAsk = self.lastPrice
        else:
            if (self.tradeAggresive == 1):
                # More buy orders than sell orders
                self.ourBid = self.lastPrice
                self.ourAsk = self.lastPrice + self.spread
            elif (self.tradeAggresive == -1):
                # Very net long, aggressively sell
                self.ourBid = self.lastPrice + self.spread
                self.ourAsk = self.lastPrice
            else:
                # If passive then take the passive approach
                self.ourBid = self.lastPrice - .5 * self.spread
                self.ourAsk = self.lastPrice + .5 * self.spread
