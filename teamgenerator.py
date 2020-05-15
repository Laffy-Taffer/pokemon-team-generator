import csv, itertools

with open('Pokemon Team Comps/types.csv', 'rt') as f:
    f.__next__()
    csv_reader = csv.reader(f)
    typelist = []
    matchup = []
    for line in csv_reader:
        typelist += [''.join(line[0])]
        typelist[-1] = ''.join(sorted(typelist[-1]))
        matchup += [line[1:-1]]

length = len(matchup)

with open('Pokemon Team Comps/teams.csv', 'wt', newline='') as f:
    csv_writer = csv.writer(f)
    x = 0
    for team in itertools.combinations(range(length), 6):
        weaknesses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        send = True

        for element in range(18):
            for pokemon in team:
                if not send:
                    break
                if float(matchup[pokemon][element]) > 1:
                    weaknesses[element] += 1
                    if weaknesses[element] > 2:
                        send = False
                        break

        if send:
            output = ''.join([typelist[a] for a in team])
            csv_writer.writerows([[output]])
