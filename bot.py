# This is the main driver for the bot
# Created on March 8th, 2018
# By Izak Fritz

import engine
import time

if __name__ == "__main__":
    newEngine = engine.tradingEngine()
    while 1:
        newEngine.order_calculations()
        print ("Make Orders..............")
        newEngine.make_orders()
        print ("Wait ...............")
        print ("\n")
        time.sleep(5)
        newEngine.check_orders()
        print ("\n")
