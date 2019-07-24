
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
