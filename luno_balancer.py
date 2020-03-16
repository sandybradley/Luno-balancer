'''
Luno Balancer
2020 - Sandy Bay

Re-balances every hour based on manually fixed allocations
Defaults to limit orders which are cancelled if unfilled and recalculated for the new rebalance

Dependencies
pip install luno-python

'''
import math
import time
import pandas as pd
import numpy as np
from luno_python.client import Client
from apscheduler.schedulers.blocking import BlockingScheduler

# set keys
api_key = ''
api_secret = ''

# set weights
# look for 6 to 12 month value
# hedge fiat (usd,rub,try,eur)
# focus on trusted cryptos with the following priority
# security
# value
# usage
# fees
# privacy
# speed

lastweights = {
    "XBT": 0.50,  
    "ZAR": 0.50 } 

# globals
prices = {} # asset prices in btc
prices['XBT'] = 1.0
XBTZAR = 0.0
balances = {}
balancesbtc = {}
totalbtc = 0
diffs = {}
steps = {}
ticks = {}
minQtys = {}

# connect
# public_client = cbpro.PublicClient()
# auth_client = cbpro.AuthenticatedClient(api_key, api_secret, passphrase)
auth_client = Client(api_key_id=api_key, api_key_secret=api_secret)
public_client = auth_client

def getPrices():
    global prices, XBTZAR
    # get prices
    for asset in lastweights:
        if asset != 'XBT':
            if asset == 'ZAR':
                priceinfo = public_client.get_ticker(pair='XBTZAR')
                p = float(priceinfo['last_trade'])
                XBTZAR = p
                prices['ZAR'] = 1 / p
            # else:
            #     priceinfo = public_client.get_product_ticker(product_id=(asset+'-BTC'))
            #     p = float(priceinfo['price'])
            #     prices[asset] = p
    
    print('Prices (BTC)')
    print(prices)

def getBalance():
    global balances, balancesbtc, totalbtc 
    totalbtc = 0
    # get balance
    info = auth_client.get_balances()
    print(info)
    for balance in info['balance']:
        # print('{}: {}'.format(balance['currency'],balance['balance']))
        bal =  float( balance['balance'] )
        asset = balance['asset']
        if asset in lastweights:
            balances[ asset ] = bal
            balancesbtc[ asset ] = bal * prices[asset]
            totalbtc = totalbtc + bal * prices[asset]
    # # print(balances)
    print("Balances (BTC)")
    print(balancesbtc)

def getDiffs():
    global diffs
    # get difference
    for asset in lastweights:
        adjshare = totalbtc * lastweights[asset]
        currshare = balancesbtc[asset]
        diff = adjshare - currshare
        diffs [ asset ] = diff
    diffs = dict(sorted(diffs.items(), key=lambda x: x[1]))
    print('Adjustments (BTC)')
    print(diffs)

def cancelOrders():
    # cancel current orders
    print('Canceling open orders')
    orders = auth_client.list_orders(created_before=None, limit=None, pair=None, state="PENDING")
    for order in orders["orders"]:
        orderid = order['order_id']
        result = auth_client.stop_order(orderid)
        print(result)
        # print('Cancel, {}, {}'.format(asset,orderid))


def step_size_to_precision(ss):
    return ss.find('1') - 1

def format_value(val, step_size_str):
    precision = step_size_to_precision(step_size_str)
    if precision > 0:
        return "{:0.0{}f}".format(val, precision)
    return math.floor(int(val))

def getSteps():
    global steps, ticks, minQtys
    # step sizes
    # info = public_client.get_products()
    # for dat in info:
    #     sym = dat['id']
    #     asset = dat['base_currency']
    #     quote = dat['quote_currency']
    #     # if quote == 'BTC' and asset in lastweights:
    #     #     steps[asset] = dat['base_min_size'] 
    #     #     ticks[asset] = dat['quote_increment']
    #     #     minQtys[asset] = dat['base_min_size']
    #     # el
    #     if sym == 'XBTZAR':
    steps[sym] = '0.0005' 
    ticks[sym] = '0.01'
    minQtys['ZAR'] = '10.0'

def placeOrders():
    # all go through btc
    # this can be smart routed later
    global diffs
    print('Setting orders')
    getSteps()
    # set sell orders
    for asset in diffs:
        diff = diffs[asset]
        if asset != 'XBT':
            thresh = float(minQtys[asset])
            if  diff <  -0.0002 : # threshold $ 1
                # if asset != 'BTC' and asset != 'ZAR':
                    # sym = asset + '-BTC'
                    # amount = 0-diff # amount in btc
                    # if ( amount / prices[asset] ) > thresh:
                    #     diffs[asset] = diffs[asset] + amount
                    #     diffs['BTC'] = diffs['BTC'] - amount
                    #     amount = format_value ( amount / prices[asset] , steps[asset] )
                    #     price = format_value ( prices [ asset ] + 0.007 * prices [ asset ], ticks[asset] )# adjust for fee
                    #     print('Setting sell order for {}, amount:{}, price:{}'.format(asset,amount,price))
                    #     auth_client.post_limit_order(pair, price, type, volume, base_account_id=None, counter_account_id=None, post_only=None)
                    #     place_limit_order(
                    #         product_id = sym, 
                    #         side = 'sell', 
                    #         price = price, 
                    #         size = amount )
                        
                    
                if asset == 'ZAR':
                    sym = 'XBTZAR'
                    amount = 0-diff
                    if amount > ( thresh / XBTZAR ):
                        diffs[asset] = diffs[asset] + amount
                        diffs['XBT'] = diffs['XBT'] - amount
                        amount = format_value ( amount  , steps[sym] )
                        price = format_value ( XBTZAR - 0.005 * XBTZAR , ticks[sym])# adjust for fee
                        print('Setting buy order for {}, amount:{}, price:{}'.format(asset,amount,price))
                        auth_client.post_limit_order( pair=sym, price=price, type='BID', volume=amount, base_account_id=None, counter_account_id=None, post_only=True)
                       
                        

    # set buy orders
    diffs = dict(sorted(diffs.items(), key=lambda x: x[1], reverse=True))

    for asset in diffs:
        diff = diffs[ asset ]
        if asset != 'XBT':
            thresh = float( minQtys[ asset ] )
            if  diff >  0.0002 : # threshold $ 1
                # if asset != 'BTC' and asset != 'ZAR':
                    # sym = asset + '-BTC'
                    # amount = diff
                    # print('{}: amount: {},thresh: {}'.format(sym,( amount / prices[asset] ),thresh))
                    # if ( amount / prices[asset] ) > thresh:
                    #     diffs[asset] = diffs[asset] - amount
                    #     diffs['BTC'] = diffs['BTC'] + amount
                    #     amount = format_value ( amount / prices[asset] , steps[asset] )
                    #     price = format_value ( prices [ asset ] - 0.007 * prices [ asset ] , ticks[asset] )# adjust for fee
                    #     print('Setting buy order for {}, amount:{}, price:{}'.format(asset,amount,price))
                    #     auth_client.place_limit_order(
                    #         product_id = sym, 
                    #         side = 'buy', 
                    #         price = price, 
                    #         size = amount )
                        
                    
                if asset == 'ZAR':
                    sym = 'XBTZAR'
                    amount = diff
                    if amount > ( thresh / XBTZAR ):
                        diffs[asset] = diffs[asset] - amount
                        diffs['XBT'] = diffs['XBT'] + amount
                        amount = format_value ( amount  , steps[sym] )
                        price = format_value ( XBTZAR + 0.005 * XBTZAR , ticks[sym])# adjust for fee
                        print('Setting sell order for {}, amount:{}, price:{}'.format(asset,amount,price))
                        auth_client.post_limit_order( pair=sym, price=price, type='ASK', volume=amount, base_account_id=None, counter_account_id=None, post_only=True)              
                        

    print ( 'Final differences' )
    print ( diffs )

def iteratey():
    getPrices()
    getBalance()
    getDiffs()
    cancelOrders()
    placeOrders()    

iteratey()

scheduler = BlockingScheduler()
scheduler.add_job(iteratey, 'interval', hours=1)
scheduler.start()
