import csv, itertools, os
from multiprocessing import Pool

with open('all types sorted.csv', 'rt') as f:  # Reads type matchup list and assigns it to typelist and matchup
    f.__next__()
    csv_reader = csv.reader(f)
    typelist = []  # list of 2 character type combos
    matchup = []  # 2d array of damage multipliers. Rows correspond to typelist. Columns are attacking type
    for line in csv_reader:
        typelist += [line[0]]
        matchup += [line[1:]]


teamlist = list(itertools.combinations(range(len(matchup)-4), 2))
teamcount = len(teamlist)


def matchupcheck(team):  # Checks if a team has no shared weaknesses
    for element in range(18):
        i = 0
        for pokemon in team:
            if float(pokemon[element]) > 1:
                i += 1
            if i > 1:
                return False
    return True


def teamcomp(types):  # Generate team combinations, runs matchupcheck, writes team to
    global typelist, matchup, teamlist
    if os.path.isfile('output/' + str(types[0]) + '/' + str(types[1]) + ' done.csv'):
        teamlist.remove(types)
        return
    print("Starting pass on " + str(types))
    savecount = 0

    with open('output/' + str(types[0]) + '/' + str(types[1]) + '.csv', 'wt', newline='') as c:
        writer = csv.writer(c)
        match1 = matchup[types[0]]
        match2 = matchup[types[1]]
        for team in itertools.combinations(range(types[1]+1, len(matchup)), 4):
            squad = [match1] + [match2] + [matchup[t] for t in team]
            if matchupcheck(squad):
                savecount += 1
                writer.writerow([''.join([typelist[a] for a in team])])

    os.rename('output/' + str(types[0]) + '/' + str(types[1]) + '.csv',
              'output/' + str(types[0]) + '/' + str(types[1]) + ' done.csv')
    teamlist.remove(types)
    x = (((teamcount - len(teamlist)) / teamcount) * 100)
    print("       Completed " + str(types) + " Saved:" + str(savecount) + " Remaining:" + str(len(teamlist)) + " " +
          "%.3f" % x + "%")


def poolhandler(wcount):
    p = Pool(wcount)
    p.map(teamcomp, reversed(list(itertools.combinations(range(len(matchup)-4), 2))))


if __name__ == '__main__':

    for outputnum in range(len(typelist) - 5):  # Creates output folders and files
        if not os.path.exists('output/' + str(outputnum)):
            os.makedirs('output/' + str(outputnum))

    poolhandler(int(input('Worker count:')))
