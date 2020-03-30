import matplotlib
from matplotlib import pyplot as plt
font = {
  'family' : 'Calibri',
  'size'   : 22, 
}
matplotlib.rc('font', **font)

OPTIM = 1 - .0907633
OPTIM_BC = 0.981340313230077

class Saudi:
  name = 'Saudi'
  capacity = 12000
  mc = 6

class Iran:
  name = 'Iran'
  capacity = 4600
  mc = 7

class Venezuela:
  name = 'Venezuela'
  capacity = 4400
  mc = 8

class Iraq:
  name = 'Iraq'
  capacity = 3700
  mc = 8

def demandCurve(q):
  return 87.57248 - 0.0018161 * q

def profit(nation, p, q):
  return q * (p - nation.mc) * 1000 # thousand barrels

all_nations = [Saudi, Iran, Venezuela, Iraq]

def f1():
  Xs = []
  profits = []
  for i in range(101):
    x = i / 100 * .2 + .8
    outputs = [
      nation.capacity * x
      for nation in all_nations
    ]
    world_price = demandCurve(sum(outputs))
    profits.append([
      profit(nation, world_price, q) / 10**6 
      for nation, q in zip(all_nations, outputs)
    ])
    Xs.append(round(100 - x * 100))
  plt.plot(Xs, profits)
  plt.xlabel('Restriction %')
  plt.ylabel('Profit ($ M)')
  plt.legend(['Saudi', 'Iran', 'Venezuela', 'Iraq'])
  plt.show()

def f2():
  Xs = []
  profits = [ [], [], [], [] ]
  for i in range(101):
    x = i / 100 * .2 + .8
    outputs = [
      nation.capacity * x
      for nation in all_nations
    ]
    world_price = demandCurve(sum(outputs))
    [
      profits[j].append(
        profit(nation, world_price, q) / 10**6 
      )
      for j, (nation, q) in enumerate(zip(all_nations, outputs))
    ]
    Xs.append(100 - x * 100)
  [_, axes] = plt.subplots(2, 2, sharex = True)
  axes[0][0].plot(Xs, profits[0])
  axes[0][0].set_title(all_nations[0].name)
  axes[0][1].plot(Xs, profits[1])
  axes[0][1].set_title(all_nations[1].name)
  axes[1][0].plot(Xs, profits[2])
  axes[1][0].set_title(all_nations[2].name)
  axes[1][1].plot(Xs, profits[3])
  axes[1][1].set_title(all_nations[3].name)
  axes[1][0].set_xlabel('Restriction %')
  axes[1][0].set_ylabel('Profit ($ M)')
  plt.show()


def f3():
  from scipy import optimize as opt
  assert all_nations[0] == Saudi
  def fun(x):
    outputs = [
      nation.capacity * x
      for nation in all_nations
    ]
    world_price = demandCurve(sum(outputs))
    return - profit(Saudi, world_price, outputs[0])
  result = opt.minimize_scalar(fun)
  print(result)

def f4():
  from scipy import optimize as opt
  def fun(x):
    outputs = [
      nation.capacity
      for nation in all_nations
    ]
    outputs[i] *= x
    world_price = demandCurve(sum(outputs))
    return - profit(Saudi, world_price, outputs[i])
  for i in range(4):
    result = opt.minimize_scalar(fun)
    print(all_nations[i].name)
    print(result)

def playGame(rate_matrix):
  mask = [1] * 11 + [.5, .25]
  acc_profit = [0] * 4
  for turn in range(13):
    outputs = [x * nation.capacity for x, nation in zip(rate_matrix[turn], all_nations)]
    world_price = demandCurve(sum(outputs))
    for i in range(4):
      acc_profit[i] += mask[turn] * profit(
        all_nations[i], world_price, outputs[i]
      )
  return acc_profit

def allAgainstAll():
  rate_matrix = [[1] * 4] * 13
  t = playGame(rate_matrix)
  for i in range(4):
    print(all_nations[i].name, t[i] / 1000000)

def nice():
  rate_matrix = [[OPTIM] * 4] * 10 + [[1] * 4] * 3
  t = playGame(rate_matrix)
  for i in range(4):
    print(all_nations[i].name, t[i] / 1000000)

def nobody():
  for j in range(4):
    rate_matrix = [[OPTIM] * 4] * 13
    for i in range(13):
      rate_matrix[i][j] = 1
    t = playGame(rate_matrix)
    print(all_nations[j].name, t[j] / 1000000)

def niceBC():
  rate_matrix = [[OPTIM_BC] * 4] * 10 + [[1] * 4] * 3
  for i in range(13):
    rate_matrix[i][3] = 1
  t = playGame(rate_matrix)
  for i in range(4):
    print(all_nations[i].name, t[i] / 1000000)

def bcOptim():
  from scipy import optimize as opt
  assert all_nations[0] == Saudi
  assert all_nations[3] == Iraq
  def fun(x):
    outputs = [
      nation.capacity * x
      for nation in all_nations
    ]
    outputs[3] = Iraq.capacity
    world_price = demandCurve(sum(outputs))
    return - profit(Saudi, world_price, outputs[0])
  result = opt.minimize_scalar(fun)
  print(result)

def f2BC():
  Xs = []
  profits = [ [], [], [], [] ]
  for i in range(101):
    x = i / 100 * .2 + .8
    outputs = [
      nation.capacity * x
      for nation in all_nations
    ]
    outputs[3] = Iraq.capacity
    world_price = demandCurve(sum(outputs))
    [
      profits[j].append(
        profit(nation, world_price, q) / 10**6 
      )
      for j, (nation, q) in enumerate(zip(all_nations, outputs))
    ]
    Xs.append(100 - x * 100)
  [_, axes] = plt.subplots(2, 2, sharex = True)
  axes[0][0].plot(Xs, profits[0])
  axes[0][0].set_title(all_nations[0].name)
  axes[0][1].plot(Xs, profits[1])
  axes[0][1].set_title(all_nations[1].name)
  axes[1][0].plot(Xs, profits[2])
  axes[1][0].set_title(all_nations[2].name)
  axes[1][1].plot(Xs, profits[3])
  axes[1][1].set_title(all_nations[3].name)
  axes[1][0].set_xlabel('Restriction %')
  axes[1][0].set_ylabel('Profit ($ M)')
  plt.show()

def retaliate():
  outputs = [
    nation.capacity * OPTIM
    for nation in all_nations
  ]
  world_price = demandCurve(sum(outputs))
  baseline = profit(Saudi, world_price, outputs[0])
  outputs[0] = Saudi.capacity
  world_price = demandCurve(sum(outputs))
  offend = profit(Saudi, world_price, outputs[0])
  gain = offend - baseline
  print('gain', gain / 10**6)
  outputs = [
    nation.capacity
    for nation in all_nations
  ]
  world_price = demandCurve(sum(outputs))
  war = profit(Saudi, world_price, outputs[0])
  print('lose', (offend - war) / 10**6)

def retaliateBC():
  outputs = [
    nation.capacity * OPTIM_BC
    for nation in all_nations
  ]
  outputs[3] = Iraq.capacity
  world_price = demandCurve(sum(outputs))
  baseline = profit(Saudi, world_price, outputs[0])
  outputs[0] = Saudi.capacity
  world_price = demandCurve(sum(outputs))
  offend = profit(Saudi, world_price, outputs[0])
  gain = offend - baseline
  print('gain', gain / 10**6)
  outputs = [
    nation.capacity
    for nation in all_nations
  ]
  world_price = demandCurve(sum(outputs))
  war = profit(Saudi, world_price, outputs[0])
  print('lose', (offend - war) / 10**6)

# f1()
# f2()
# f3()
# f4()
# allAgainstAll()
# nice()
# niceBC()
# nobody()
# bcOptim()
# f2BC()
retaliateBC()
