# This is the main driver for the bot
# Created on March 8th, 2018
# By Izak Fritz

import engine
import time

if __name__ == "__main__":
    newEngine = engine.tradingEngine()
    while 1:
        newEngine.order_calculations()
        print ("Trade Aggreessive: " + str(newEngine.orderPlacement.tradeAggresive))
        print ("Our position: " + str(newEngine.orderPlacement.ourPosition))
        print ("Make Orders..............")
        newEngine.make_orders()
        print ("Wait ...............")
        print ("\n")
        time.sleep(2)
        newEngine.check_orders()
        print ("\n")
