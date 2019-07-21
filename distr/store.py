# builtin
import os
from os.path import abspath, dirname, join, isdir, basename
# custom
import gen
from util import log, logaz, mapl, timit


# directory/path utils
_path_here = abspath(__file__)
PATH_DIR = dirname(_path_here)

def make_dir_if_not(path):
  os.makedirs(path,exist_ok=True)
PATH_DATA = join(PATH_DIR, 'stored')
# recursive-print dir-struct
def list_dirs(path,depth=0):
  def show_dir(name):
    print('%s%s'%('\t'*depth, name))
  show_dir(basename(path))
  if isdir(path):
    for e in os.listdir(path):
      path_child = join(path,e)
      list_dirs(path_child,depth+1)    


"""shard funcs
  data -> shard by [year, month]

  decompose_index: DF.index -> [indices..]
  shard: df -> groupby [
    (
      (indices..),
      df_group
      )..
    ]
  index2path: [indices..] -> path in file-system
  """
def decompose_index(index):
  return (
    index.strftime('%Y'),
    index.strftime('%m'),
    )
def shard(df):
  return df.groupby(decompose_index)
def index2path(index):
  str_indices = mapl(str,index) # [yyyy,mm]
  return join(PATH_DATA,*str_indices)


# write df to file
NAME_FILE = 'data.csv'
def write(indices2df):
  index, df = indices2df
  path_dir = index2path(index)
  make_dir_if_not(path_dir)
  path_file = join(path_dir,NAME_FILE)
  df.to_csv(path_file,index=True)


# data -> write to distributed locations
@timit()
@logaz()
def distribute(df):
  return mapl(write, shard(df))


if __name__=='__main__':
  # test unit
  # make_dir_if_not(PATH_DATA)
  # list_dirs(PATH_DATA)

  # test integration
  span = gen.gen_span('20140101','20160101')
  syms = gen.gen_syms(range(10))
  df_sym2price = gen.gen_sym2price(span,syms)
  gen.glean(df_sym2price)
  indices2df = shard(df_sym2price)
  files = mapl(write, indices2df)
  distribute(df_sym2price)
  # list_dirs(PATH_DATA)

