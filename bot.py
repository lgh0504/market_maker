# This is the main driver for the bot
# Created on March 8th, 2018
# By Izak Fritz

import wrapper
import data_processor
import engine

if __name__ == "__main__":
    newEngine = engine.orderPlacement("USDT-BTC")
    newEngine.update_data()
    newEngine.update_aggressive_or_passive(.5)
