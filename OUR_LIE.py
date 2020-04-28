import matplotlib
from matplotlib import pyplot as plt
font = {
  'family' : 'Calibri',
  'size'   : 22, 
}
matplotlib.rc('font', **font)

SOLD = {
  'A': [3700, 442, 230, 100],
  'B': [3451, 441, 220],
  'C': [3460, 440, 220],
}

N_ROUNDS = 6
RESULTS_readable = {
  1: {'A': [46.00, 59588], 'B': [44.14, 62181], 'C': [46.34, 60925]},
  2: {'A': [42.63, 62525], 'B': [43.57, 60623], 'C': [43.67, 62445]},
  3: {'A': [42.27, 60510], 'B': [43.31, 62142], 'C': [43.13, 62223]},
  4: {'A': [43.04, 61113], 'B': [42.98, 63209], 'C': [44.52, 62591]},
  5: {'A': [46.05, 61001], 'B': [42.09, 62914], 'C': [42.58, 61722]},
  6: {'A': [43.84, 59200], 'B': [42.47, 61465], 'C': [42.76, 62115]},
}
RESULTS = [RESULTS_readable[i] for i in range(1, N_ROUNDS + 1)]

EVALUATION_sc_a = {
  'A': [3768, 521, 386, 100], 
  'B': [3768, 521, 386, 100], 
  'C': [3768, 521, 386, 100], 
}
EVALUATION_sc_b = {
  'A': [3791, 522, 389, 100], 
  'B': [3748, 502, 367], 
  'C': [3748, 502, 367], 
}
EVALUATION = {'A': EVALUATION_sc_a, 'B': EVALUATION_sc_b}

OPTIM_BC = 0.9583628802587333

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
  return 87.24762532 - 0.001848585468 * q

def profit(nation, p, q):
  return q * (p - nation.mc) * 1000 # thousand barrels

all_nations = [Saudi, Iran, Venezuela, Iraq]
all_players = [
  ['A', 0], 
  ['A', 1], 
  ['A', 2], 
  ['A', 3], 
  ['B', 0], 
  ['B', 1], 
  ['B', 2], 
  ['C', 0], 
  ['C', 1], 
  ['C', 2], 
]

round_expected_income = {
  'war': {
    'A': [-1, -1, -1, -1], 
    'B': [-1, -1, -1, -1], 
    'C': [-1, -1, -1, -1], 
  }, 
  'nice': {
    'A': [-1, -1, -1, -1], 
    'B': [-1, -1, -1, -1], 
    'C': [-1, -1, -1, -1], 
  }, 
}
def calculateExpectedIncome():
  for market in 'ABC':
    for round_scenario in ['war', 'nice']:
      outputs = [
        nation.capacity for nation in all_nations
      ]
      if round_scenario == 'nice':
        outputs[0] *= OPTIM[market]
        outputs[1] *= OPTIM[market]
        outputs[2] *= OPTIM[market]
        if market == 'A':
          outputs[3] *= OPTIM[market]
      q = sum(outputs)
      price = demandCurve(q)
      for i in range(4):
        round_expected_income[round_scenario][market][i] = profit(all_nations[i], price, outputs[i])

# calculateExpectedIncome()

def roundAim(scenario, market, nation_i, round_i):
  if scenario == 'A' or round_i >= 10:
    round_scenario = 'war'
  else:
    round_scenario = 'nice'
  return round_expected_income[round_scenario][market][nation_i], round_scenario

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
  return result

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

print(bcOptim())
print(f'{(1-bcOptim().x) * 100}% restriction is optimal')
f2BC()
