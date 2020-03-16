# Luno-Balancer 
Portfolio re-balancer for luno. Herein I provide a script to automate digital asset portfolio re-balance at user specified intervals (defaults to every hour). Note this is long only spot portfolio.

# Why diversify ?

Diverse investments mitigate risk of loss and can offer significant return improvements over any single asset. The dawn of crypto enables anyone to set up their own portfolio at near zero cost. Moreover, I present tools to enable anyone to automate re-balancing at any interval, based on manually pre-defined allocations.

# How to setup my balancer ?

Steps to get started:

1. [Download and install python framework](https://www.python.org/downloads/)
2. [Set up a Luno account](https://www.luno.com/en/invite/RV5Q7)
3. Generate API keys in Luno settings
4. Fund your Luno account
5. Download this luno balancer script
6. Edit API keys in luno_balancer.py
7. Edit your configuration:

```python
lastweights = {     "XBT":0.5, "ZAR":0.5 }
```
Install dependencies:

```
pip install python-binance
```
Run the script (it will automatically re-balance for you every hour):

```
python binance-balancer.py
```

# Final thoughts 

Hopefully, you have found my software of value. I offer my extensive testing, results and software for your benefit. That is for financial sovereignty of the populous. Please consider donating.

# Karma Jar
BTC - 112eMCQJUkUz7kvxDSFCGf1nnFJZ61CE4W

LTC - LR3BfiS77dZcp3KrEkfbXJS7U2vBoMFS7A

ZEC - t1bQpcWAuSg3CkBs29kegBPXvSRSaHqhy2b

XLM - GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A Memo: 1015040538

Nano - nano_1ca5fxd7uk3t61ghjnfd59icxg4ohmbusjthb7supxh3ufef1sykmq77awzh

XRP - rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh Tag: 103535357

EOS - binancecleos Memo: 103117718

# Recommended links
Getting started - [Coinbase](https://www.coinbase.com/join/bradle_6r)

Portfolio balance - [Binance](https://www.binance.com/en/register?ref=LTUMGDDC)

Futures trading - [Deribit](https://www.deribit.com/reg-8106.6912)

Cold wallet - [Atomic](https://atomicWallet.io?kid=12GR52)
