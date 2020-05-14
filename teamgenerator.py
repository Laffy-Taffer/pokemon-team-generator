import csv, itertools

# Opens a csv with every valid type combination(each type a base19 character) and writes it to a list
with open('Pokemon Team Comps/types.csv', 'r') as f:
    f.__next__()
    csv_reader = csv.reader(f)
    typelist = []
    matchup = []
    for line in csv_reader:
        typelist += [''.join(line[0])]
        typelist[-1] = ''.join(sorted(typelist[-1]))
        matchup += [line[1:-1]]

with open('Pokemon Team Comps/teams.csv', 'wt', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Check #", "Team", "Max # of weaknesses"])

    # For progress checking and debugging
    teamnum = 0

    for team in itertools.combinations(range(171), 6):

        # Matches each base 171 key with its base 19 value, then matches that base 19 key with its type matchup
        teamnum += 1
        if teamnum % 100000 == 0:
            print(teamnum, "teams")
        squad = [] + [typelist[a] for a in team]
        defenses = [] + [matchup[team[a]] for a in range(len(squad))]

        # Caclulates the number of weakenesses to each type that exists on the team
        weaknesses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for defense in defenses:
            for element in range(len(defense)):
                if float(defense[element]) > 1:
                    weaknesses[element] += 1

        # Writes check#(for debugging), team(in base19), and largest # of weaknesses to any type on team all into CSV
        squad = ''.join([item for sublist in squad for item in sublist])
        csv_writer.writerows([[teamnum, squad, str(max(weaknesses))]])
