import numpy as np
import pandas as pd
S = pd.Series
DF = pd.DataFrame
# custom
from util import log, logaz, timit



# generate symbols
def gen_syms(ids):
  return ['sym_%s'%_id for _id in ids]

## str, str -> span of business days
def gen_span(d0,d1=None,n=None):
  assert d1 or n
  if d1:
    n = None
  else:
    d1 = None
  return pd.date_range(start=d0,end=d1,periods=n,freq='B')

## n-step path via Laplace distribution
def gen_walk(n):
  steps = np.random.laplace(loc=0.,scale=1.,size=n)
  path = steps.cumsum()/np.sqrt(n)
  return path

## prices
PRECISION = 3
def gen_prices(span,start=(10,100)):
  walk = gen_walk(len(span)) # treat as %-deltas
  price_0 = np.random.choice(range(*start)) # starting price
  prices = np.absolute( (1+walk) * price_0 ) # price trajectory
  return pd.Series(prices,span).round(PRECISION)

## {sym -> price} : DF
@timit()
@logaz()
def gen_sym2price(span,syms):
  return DF({sym:gen_prices(span)
    for sym in syms})

# assume Series/DataFrame,etc
def glean(obj):
  log('\n%s', DF(obj).describe())


# tests
if __name__=='__main__':
  # test unit
  span = gen_span('20140101','20160101',500)
  glean(span)
  syms = gen_syms(range(10))
  glean(syms)
  walk = gen_walk(len(span))
  glean(walk)
  prices = gen_prices(span)
  glean(prices)
  df_sym2px = gen_sym2price(span,syms)
  glean(df_sym2px)


