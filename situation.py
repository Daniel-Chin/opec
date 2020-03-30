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

N_ROUNDS = 4
RESULTS_readable = {
  1: {'A': [46.00, 59588], 'B': [44.14, 62181], 'C': [46.34, 60925]},
  2: {'A': [42.63, 62525], 'B': [43.57, 60623], 'C': [43.67, 62445]},
  3: {'A': [42.27, 60510], 'B': [43.31, 62142], 'C': [43.13, 62223]},
  4: {'A': [43.04, 61113], 'B': [42.98, 63209], 'C': [44.52, 62591]},
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

OPTIM_A = 1 - .0907633
OPTIM_BC = 0.981340313230077
OPTIM = {'A': OPTIM_A, 'B': OPTIM_BC, 'C': OPTIM_BC}

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

calculateExpectedIncome()

def roundAim(scenario, market, nation_i, round_i):
  if scenario == 'A' or round_i >= 10:
    round_scenario = 'war'
  else:
    round_scenario = 'nice'
  return round_expected_income[round_scenario][market][nation_i], round_scenario

def main(conservative = False):
  for scenario in 'AB':
    score = [
      [ (EVALUATION[scenario][market][nation_i] - SOLD[market][nation_i]) * 1000000 ]
      for (market, nation_i) in all_players
    ]
    for round_i in range(N_ROUNDS):
      for (player_i, (market, nation_i)) in enumerate(all_players):
        player_score = score[player_i]
        nation = all_nations[nation_i]
        aim, round_scenario = roundAim(scenario, market, nation_i, round_i)
        price = RESULTS[round_i][market][0]
        q = nation.capacity
        if round_scenario == 'nice':
          q *= OPTIM[market]
        elif conservative and market == 'C':
          q *= OPTIM[market]
        factual = profit(nation, price, q)
        delta = factual - aim
        player_score.append(player_score[-1] + delta)
    score = [[round(y / 1000000) for y in x] for x in score]
    # from console import console
    # console({**locals(), **globals()})
    [plt.plot(range(N_ROUNDS + 1), x, label=all_nations[nation_i].name + ' ' + market) for x, (market, nation_i) in zip(score, all_players)]
    plt.title('Scenario ' + scenario)
    # my_legend()
    # plt.legend()
    plt.xlabel('Round')
    plt.ylabel('Score (M $)')
    plt.show()

import numpy as np
from scipy import ndimage


def my_legend(axis = None):
    # author: Jan Kuiken
    # https://stackoverflow.com/a/17000662/8622053

    if axis == None:
        axis = plt.gca()

    N = 32
    Nlines = len(axis.lines)
    print(Nlines)

    xmin, xmax = axis.get_xlim()
    ymin, ymax = axis.get_ylim()

    # the 'point of presence' matrix
    pop = np.zeros((Nlines, N, N), dtype=np.float)    

    for l in range(Nlines):
        # get xy data and scale it to the NxN squares
        xy = axis.lines[l].get_xydata()
        xy = (xy - [xmin,ymin]) / ([xmax-xmin, ymax-ymin]) * N
        xy = xy.astype(np.int32)
        # mask stuff outside plot        
        mask = (xy[:,0] >= 0) & (xy[:,0] < N) & (xy[:,1] >= 0) & (xy[:,1] < N)
        xy = xy[mask]
        # add to pop
        for p in xy:
            pop[l][tuple(p)] = 1.0

    # find whitespace, nice place for labels
    ws = 1.0 - (np.sum(pop, axis=0) > 0) * 1.0 
    # don't use the borders
    ws[:,0]   = 0
    ws[:,N-1] = 0
    ws[0,:]   = 0  
    ws[N-1,:] = 0  

    # blur the pop's
    for l in range(Nlines):
        pop[l] = ndimage.gaussian_filter(pop[l], sigma=N/5)

    for l in range(Nlines):
        # positive weights for current line, negative weight for others....
        w = -0.3 * np.ones(Nlines, dtype=np.float)
        w[l] = 0.5

        # calculate a field         
        p = ws + np.sum(w[:, np.newaxis, np.newaxis] * pop, axis=0)
        plt.figure()
        plt.imshow(p, interpolation='nearest')
        plt.title(axis.lines[l].get_label())

        pos = np.argmax(p)  # note, argmax flattens the array first 
        best_x, best_y =  (pos / N, pos % N) 
        x = xmin + (xmax-xmin) * best_x / N       
        y = ymin + (ymax-ymin) * best_y / N       


        axis.text(x, y, axis.lines[l].get_label(), 
                  horizontalalignment='center',
                  verticalalignment='center')

main(conservative=True)
