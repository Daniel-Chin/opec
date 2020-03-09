from scipy import optimize as opt
# import matplotlib
# from matplotlib import pyplot as plt
# font = {
#   'family' : 'Calibri',
#   'size'   : 22, 
# }
# matplotlib.rc('font', **font)

class Saudi:
  name = 'Saudi'
  mc = 6

class Iran:
  name = 'Iran'
  mc = 7

class Venezuela:
  name = 'Venezuela'
  mc = 8

class Iraq:
  name = 'Iraq'
  mc = 8

def demandCurve(q):
  return 87.57248 - 0.0018161 * q

def profit(nation, p, q):
  return q * (p - nation.mc) * 1000 # thousand barrels

all_nations = [Saudi, Iran, Venezuela, Iraq]

def f():
  def fun(x, nation, sum_others):
    world_price = demandCurve(sum_others + x)
    return - profit(nation, world_price, x)
  outputs = [0] * 4
  for round in range(100):
    for i, nation in enumerate(all_nations):
      outputs[i] = 0
      result = opt.minimize_scalar(fun, args = (nation, sum(outputs)))
      outputs[i] = result.x
    print('Round', round, outputs)

f()
