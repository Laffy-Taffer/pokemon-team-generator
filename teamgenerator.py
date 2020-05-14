import csv, itertools
with open('Pokemon Team Comps/types.csv', 'r') as f:
    csv_reader = csv.reader(f)
    typelist = []
    matchup = []
    for line in csv_reader:
        typelist += [''.join(line[0])]
        typelist[-1] = ''.join(sorted(typelist[-1]))
        matchup += [line[1:-1]]

with open('Pokemon Team Comps/teams.csv', 'wt', newline='') as f:
    csv_writer = csv.writer(f)
    for team in itertools.combinations(range(171), 6):
        csv_writer.writerows([team])
