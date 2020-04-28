SOLD = {
  'A': [3791, 442, 389, 100],
  'B': [3748, 441, 367],
  'C': [3748, 440, 367],
}

SAUDI_Q = [11772] * 6 + [12000] * 6
Ven_Q = [4317] * 6 + [4400] * 6
# Ven_Q = [4400] * 11

N_ROUNDS = 12
RESULTS_readable = {
  1:  {'A': [46.00, 59588], 'B': [44.14, 62181], 'C': [46.34, 60925]},
  2:  {'A': [42.63, 62525], 'B': [43.57, 60623], 'C': [43.67, 62445]},
  3:  {'A': [42.27, 60510], 'B': [43.31, 62142], 'C': [43.13, 62223]},
  4:  {'A': [43.04, 61113], 'B': [42.98, 63209], 'C': [44.52, 62591]},
  5:  {'A': [46.05, 61001], 'B': [42.09, 62914], 'C': [42.58, 61722]},
  6:  {'A': [43.84, 59200], 'B': [42.47, 61465], 'C': [42.76, 62115]},
  7:  {'A': [44.77, 61470], 'B': [42.77, 61906], 'C': [45.03, 61043]},
  8:  {'A': [43.17, 59985], 'B': [42.58, 62422], 'C': [41.59, 61683]},
  9:  {'A': [41.82, 62642], 'B': [41.11, 62145], 'C': [42.49, 61223]},
  10: {'A': [42.67, 60776], 'B': [40.58, 62690], 'C': [42.62, 62117]},
  11: {'A': [43.81, 60998], 'B': [43.44, 60887], 'C': [41.28, 61501]},
  12: {'A': [43.81, 60998], 'B': [43.44, 60887], 'C': [41.28, 61501]},
}
RESULTS = [RESULTS_readable[i] for i in range(1, N_ROUNDS + 1)]

class Saudi:
  name = 'Saudi'
  capacity = 12000
  mc = 6

class Venezuela:
  name = 'Venezuela'
  mc = 8

def profit(nation, p, q):
  return q * (p - nation.mc) * 1000 # thousand barrels

for market in 'ABC':
    sum = -SOLD[market][2]
    for round in range(N_ROUNDS):
        sum += profit(Venezuela, RESULTS[round][market][0], Ven_Q[round]) / 1000000
    print('Venezuela', market, 'profit =', sum)
for market in 'ABC':
    sum = -SOLD[market][0]
    for round in range(N_ROUNDS):
        sum += profit(Saudi, RESULTS[round][market][0], SAUDI_Q[round]) / 1000000
    print('Saudi', market, 'profit =', sum)
