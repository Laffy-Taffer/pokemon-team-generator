import csv, itertools, os, math
from multiprocessing import Pool

with open('types.csv', 'rt') as f:
    f.__next__()
    csv_reader = csv.reader(f)
    typelist = []
    matchup = []
    for line in csv_reader:
        typelist += [''.join(line[0])]
        typelist[-1] = ''.join(sorted(typelist[-1]))
        matchup += [line[1:-1]]

length = len(matchup)
teamfact = math.factorial(5)
new = False
if not os.path.exists('output'):
    os.makedirs('output')
    new = True


def teamcomp(r):
    global length, typelist, matchup
    comborange = length - r + 1
    combofact = math.factorial(comborange)
    print("Starting team check", r, "Number of combinations:",
          '{:,}'.format(int(combofact / (teamfact * math.factorial(comborange - 5)))))
    with open('output/teams' + str(r) + '.csv', 'wt', newline='') as c:
        writer = csv.writer(c)
        for team in itertools.combinations(range(r + 1, length), 5):
            team = tuple([r] + [t for t in team])
            weaknesses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            send = True
            for element in range(18):
                for pokemon in team:
                    if float(matchup[pokemon][element]) > 1:
                        weaknesses[element] += 1
                        if weaknesses[element] > 2:
                            send = False
                            break
                if not send:
                    break

            if send:
                output = ''.join([typelist[a] for a in team])
                writer.writerows([[output]])
    os.rename('output/teams' + str(r) + '.csv',
              'output/teams' + str(r) + 'done.csv')
    print("                       Finished with team", r)


def pool_handler(n):
    p = Pool(n)
    starter = reversed(range(start))
    p.map(teamcomp, starter)


if __name__ == '__main__':

    x = os.listdir("output")
    start = length - 5
    # start = highest = 0
    # if not new:
    #    everything = [a.replace('teams', '') for a in x]
    #    highest = max([int(a.replace('teams', '').replace('done', '').replace('.csv', '')) for a in x])
    #    nextone = max([int(a.replace('teams', '').replace('.csv', '')) for a in x if 'done' not in a])
    #    start = input("Input value to count down from\nHighest value: " + str(highest) +
    #                  "  Highest uncalculated value: " + str(nextone) + "\n")
    poolcount = int(input("How many cores do you want to use?\n"))
    pool_handler(poolcount)
