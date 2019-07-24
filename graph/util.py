import datetime, logging, time
from functools import wraps


# logging
def get_logger():
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  sh = logging.StreamHandler()
  sh.setFormatter(logging.Formatter(
    '<%(module)s.%(funcName)s:%(lineno)d> %(message)s'))
  logger.addHandler(sh)
  return logger
log = get_logger().warning # quick default logging-function

# hacky check Pandas w/o import
def not_pd_struct(obj):
  return obj.__class__.__name__ not in ('Series','DataFrame')

def logaz(opts='zs',logf=log):
  '''log function input/output
    a -> input
    z -> output
    s -> only summarize output
    '''
  assert opts in ('a','z','az','zs','azs')
  show_input = lambda : 'a' in opts
  show_output_summary = lambda : 's' in opts
  render = lambda res:res if not_pd_struct(res) else '\n%s'%res
  def log_f(f):
    @wraps(f)
    def log_a(*args, **kwargs):
      res = f(*args, **kwargs)
      # if log input
      prefix = '%s; %s'%(args, kwargs) if show_input() else ''
      # how log output
      suffix = len(res) if show_output_summary() else render(res)
      logf('%s: %s -> %s', f.__name__, prefix, suffix)
      return res
    return log_a
  return log_f


# timer
def timit(logf=log):
  def time_f(f):
    @wraps(f)
    def time_a(*args,**kwargs):
      t0 = time.time()
      res = f(*args,**kwargs)
      td = round(time.time() - t0, 4)
      if td <= 1e-2:
        body, unit = td*1e3, 'ms'
      else:
        body, unit = td, 's'
      logf('%s.%s: %.1f %s',f.__module__,f.__name__,body,unit)
      return res
    return time_a
  return time_f


# functional-programming
mapl = lambda f,itr: list(map(f,itr)) # actuate map-generator -> mapped-list
def memo(key=lambda obj:obj,dict_type=dict):
  seen = dict_type()
  def memo_f(f):
    def memo_a(*args,**kwargs):
      k = key(*args,**kwargs)
      if k not in seen:
        seen[k] = f(*args,**kwargs)
      return seen[k]
    return memo_a
  return memo_f


