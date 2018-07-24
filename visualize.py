import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from binance.client import Client
import json
import time

with open('C:\\Users\\Clement\\Pycharm\\crypto_arbitrage\\keys\\binance.key') as f:
    key = json.load(f)

binance_engine = Client(key['key'], key['secret'])

plt.style.use("bmh")
fig = plt.figure(figsize=(15,8))
ax1 = fig.add_subplot(1, 1, 1)
spread = 0.5/100

def animate(i):
    order_book = binance_engine.get_order_book(symbol='ETHUSDT')

    bid_price = float(order_book['bids'][0][0])
    ask_price = float(order_book['asks'][0][0])
    mid_price = (bid_price + ask_price) / 2
    price_min = mid_price * (1 - spread)
    price_max = mid_price * (1 + spread)

    # BIDS
    prices = []
    qtys_bids = []
    qtys_asks = []
    total = 0

    cummul_buy = 0
    for i in range(len(order_book['bids'])):
        if float(order_book['bids'][i][0]) >= price_min:
            prices.append(float(order_book['bids'][i][0]))
            qtys_bids.append(cummul_buy + float(order_book['bids'][i][1]))
            cummul_buy += float(order_book['bids'][i][1])
            qtys_asks.append(np.nan)
    qtys_bids = list(reversed(qtys_bids))
    prices = list(reversed(prices))

    # ASKS
    cummul_sell = 0
    for i in range(len(order_book['asks'])):
        if float(order_book['asks'][i][0]) <= price_max:
            prices.append(float(order_book['asks'][i][0]))
            qtys_asks.append(cummul_sell + float(order_book['asks'][i][1]))
            cummul_sell += float(order_book['asks'][i][1])
            qtys_bids.append(np.nan)

    score = np.nan
    if cummul_buy > cummul_sell:
        score = cummul_buy / cummul_sell - 1
    else:
        score = 1 - cummul_sell / cummul_buy

    ax1.clear()
    ax1.plot(prices, qtys_bids, 'g', linewidth=1.0)
    ax1.fill_between(prices, qtys_bids, color='g', alpha=0.5)
    ax1.plot(prices, qtys_asks, 'r', linewidth=1.0)
    ax1.fill_between(prices, qtys_asks, color='r', alpha=0.5)
    ax1.set_ylim(0)
    ax1.set_xlim(prices[0], prices[-1])
    ax1.set_ylabel('Quantities')
    ax1.set_xlabel('Price')
    ax1.set_title('Best bid : {bbid:.2f}, Best ask : {aask:.2f}, Score : {score:.0%}'.format(bbid=bid_price, aask=ask_price, score=score))

ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()