# This will be a tester for all the functions
# Created on March 8th, 2018
# By Izak Fritz

import wrapper
import data_processor

if __name__ == "__main__":
    caller = data_processor.api_calls()

    # Test each of the api calls
    output = caller.getticker("USDT-BTC")
    assert (output['success'] == 1), "getticker failed"
    print ("getticker works!")

    output = caller.getmarketsummaries()
    assert (output['success'] == 1), "getmarketsummaries failed"
    print ("getmarketsummaries works!")

    output = caller.getmarketsummary("USDT-BTC")
    assert (output['success'] == 1), "getmarketsummary failed"
    print ("getmarketsummary works!")

    output = caller.getorderbook("USDT-BTC", 'both')
    assert (output['success'] == 1), "getmarketsummary failed"
    print ("getorderbook works!")

    output = caller.getopenorders("USDT-BTC")
    assert (output['success'] == 1), "getmarketsummary failed"
    print ("getopenorders works!")

    output = caller.getbalances()
    assert (output['success'] == 1), "getmarketsummary failed"
    print ("getbalances works!")

    output = caller.buylimit("USDT-BTC", .001, 100)
    assert (output['success'] == 1), "buylimit failed"
    uuid1 = output['result']['uuid']
    print ("buylimit works!")

    output = caller.getorder(uuid1)
    assert (output['success'] == 1), "getorder failed"
    print ("getorder buylimit works!")

    output = caller.cancel(uuid1)
    assert (output['success'] == 1), "cancel failed"
    print ("cancel a buylimit works!")

    output = caller.selllimit("USDT-BTC", .001, 50000)
    assert (output['success'] == 1), "selllimit failed"
    uuid2 = output['result']['uuid']
    print ("selllimit works!")

    output = caller.getorder(uuid1)
    assert (output['success'] == 1), "getorder failed"
    print ("getorder selllimit works!")

    output = caller.cancel(uuid2)
    assert (output['success'] == 1), "cancel failed"
    print ("cancel a selllimit works!")
