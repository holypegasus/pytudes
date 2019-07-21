# builtin
from os.path import join
# 3rd party
import pandas as pd
# custom
import gen
from store import (
  PATH_DIR, NAME_FILE,
  make_dir_if_not,
  index2path, decompose_index,
  )
from util import date2str, log, logaz, mapl, timit


def path2df(path_dir,syms):
  path_file = join(path_dir, NAME_FILE)
  return (pd.read_csv(path_file,index_col=0,parse_dates=True)
    [syms] # filter col by syms
    )

# dfs -> df
def stitch(dfs):
  return pd.concat(dfs)

# -> dfs
@timit()
@logaz('zs')
def find(span,syms):
  indices = sorted(set(mapl(decompose_index, span))) # uniq-ify & sort
  path_dirs = mapl(index2path, indices)
  dfs = [path2df(path,syms) for path in path_dirs]
  return (stitch(dfs)
    .loc[span[0]:span[-1]] # filter by time
    )


PATH_QUERY = join(PATH_DIR, 'queried')
# write query output to file
def write(df,span,syms):
  make_dir_if_not(PATH_QUERY)
  name_file = '%s-%s.csv'%(
    '_'.join(mapl(
      date2str,
      (span[0],span[-1]))),
    '_'.join(syms))
  path_file = join(PATH_QUERY, name_file)
  df.to_csv(path_file,index=True)
  log('-> %s', path_file)



if __name__=='__main__':
  t_0z = ('20141107','20150121')
  span = gen.gen_span(*t_0z)
  log('[%s] %s',len(span),t_0z)
  syms = ['sym_3','sym_6','sym_7']

  # test unit
  # path_test = index2path(decompose_index(span[0]))
  # df_test = path2df(path_test,syms)
  # gen.glean(df_test)

  # test integration
  df = find(span,syms)
  assert len(span)>=len(df)
  write(df,span,syms)

