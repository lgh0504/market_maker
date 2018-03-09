# Market Maker Bot
# This bot was created by Izak Fritz
# March 8th, 2018

The bot will work in the following manner:
1. The bot will start with a Bittrex account with a total balance composed half on
an altcoin and half Bitcoin.
2. Then check the current price of that altcoin and evaluate the current spread
3. From here it will calculate what orders it wants to place based on the
total account balance and what orders are currently open on the book
4. Evaluate if it needs to take an aggressive or passive MM approach
5. Evaluate what price the positions should be and what size they should be
5. Place the orders at the specified prices and wait 10 seconds (this is considered 1 trading period)
6. Cancel all open orders and start again at step 2
