#! /usr/local/bin/python3
# builtins
import argparse
# 3rd party
import numpy as np
import pandas as pd
# custom
import gen, store, query
from util import log, logaz, mapl, vali_date


N_SYM = 10
SPAN = ('20140101','20160101')
OPT_GEN = 'g'
OPT_STORE = 's'
OPT_QUERY = 'q'
@logaz('z')
def parse():
  def q_syms_id2full(_str):
    ids = _str.split(',')
    return gen.gen_syms(ids)
  parser = argparse.ArgumentParser(description='Get & execute arguments from commandline',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    # RawTextHelpFormatter -> direct control text
    )
  # operation
  parser.add_argument('-o','--ops',help='''define operation(s), space-separated: (g)en|(s)tore|(q)uery; 
    \ng s -> generate & store data;
    \nq s -> query & store results''',
    nargs='*',choices=(OPT_GEN,OPT_STORE,OPT_QUERY),default='q')
  parser.add_argument('--q_syms',help='set comma-delimited (symbol-)ids to query',type=q_syms_id2full,default=[])
  # parser.add_argument('--save',help='if to save query-results to file',default=False,action='store_const',const=True)
  # params
  parser.add_argument('--n_syms',help='set number of symbols/tickers',default=10,type=int)
  parser.add_argument('-a','--d0',help='set start date (yyyymmdd)',default='20140301',type=vali_date)
  parser.add_argument('--n_days',help='set number of (business) days',default=500,type=int)
  parser.add_argument('-z','--d1',help='set end date (yyyymmdd)',type=vali_date)
  # validate & interpolate/derive
  args = parser.parse_args()
  if OPT_QUERY in args.ops:
    assert args.q_syms
  assert args.n_days or args.d1
  vars(args)['span'] = gen.gen_span(args.d0,args.d1,args.n_days)
  vars(args)['syms'] = gen.gen_syms(range(args.n_syms))
  return args


if __name__=='__main__':
  # t_0z = ('20141107','20150121')
  # q_span = gen.gen_span(*t_0z)
  # q_syms = sorted(np.random.choice(syms,3,replace=False))
  args = parse()
  if OPT_GEN in args.ops:
    df = gen.gen_sym2price(args.span, args.syms)
    if OPT_STORE in args.ops:
      store.distribute(df)
  elif OPT_QUERY in args.ops:
    df = query.find(args.span, args.q_syms)
    if OPT_STORE in args.ops:
      query.write(df, args.span, args.q_syms)
    else:
      gen.glean(df)


