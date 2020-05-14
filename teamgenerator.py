import csv

# Opens a csv with every valid type combination(each type a base19 character) and writes it to a list
with open('alltypes.csv', 'rt') as f:
    csv_reader = csv.reader(f)
    typelist = []
    for line in csv_reader:
        typelist += [''.join(line)]
        typelist[-1] = ''.join(sorted(typelist[-1]))


# Returns a list with each value corresponding to a digit of n written in base b
def numbertobase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


# See movetype table for corresponding type
matchup = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1],
    [1, 1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1],
    [1, 1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1],
    [1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1],
    [1, 1, 0.5, 2, 1, 0.5, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1],
    [1, 1, 0.5, 0.5, 1, 2, 0.5, 1, 0.5, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5],
    [1, 1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2],
    [1, 1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1],
    [1, 1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1],
    [1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1],
    [1, 1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5],
    [1, 1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0],
    [1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5],
    [1, 1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2],
    [1, 1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1]]

# Doesn't actually do anything, its just for my own reference
movetype = {"none":     "0",
            "normal":   "1",
            "fire":     "2",
            "water":    "3",
            "electric": "4",
            "grass":    "5",
            "ice":      "6",
            "fighting": "7",
            "poison":   "8",
            "ground":   "9",
            "flying":   "a",
            "psychic":  "b",
            "bug":      "c",
            "rock":     "d",
            "ghost":    "e",
            "dragon":   "f",
            "dark":     "g",
            "steel":    "h",
            "fairy":    "i"}


with open('teams.csv', 'wt', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Check #", "Team", "Max # of weaknesses"])

    # For progress checking and debugging
    checktotal = 0
    teamnum = 0
    teamprev = 0
    teams = []

    # Start is minimum value to generate a valid team, end is maximum value(+1)
    for b171 in range(865124915, 24414690227212):

        # Progress checking
        checktotal += 1
        if checktotal % 10000 == 0:
            print(checktotal, "checked", teamnum-teamprev, "new teams", teamnum, "total")
            teamprev = teamnum

        # Converts number to a list, each item corresponding to a digit in base 171(# of unique pkmn types)
        team = numbertobase(b171, 171)
        if len(team) == 5:
            team = [0] + team
        team.sort()
        
        retry = False
        for digit in range(len(team)):
            if digit != 0:
                if team[digit] < team[digit]:
                    retry = True
                    break
        # Checks for dupes and repeated combos
        if len(team) != len(set(tuple(team))) or team in teams or retry:
            if len(team) != len(set(tuple(team))) or team in teams or retry:
                continue

        teamnum += 1
        teams += [team]

        # Matches each base 171 key with its base 19 value, then matches that base 19 key with its type matchup
        squad = []
        squad += [typelist[a] for a in team]
        defenses = []
        for pokemon in squad:
            defenses += [[a*b for a, b in zip(matchup[int(pokemon[0], 19)], matchup[int(pokemon[1], 19)])]]

        # Caclulates the number of weakenesses to each type that exists on the team
        weaknesses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for defense in defenses:
            for element in range(len(defense)):
                if defense[element] > 1:
                    weaknesses[element] += 1

        # Writes check#(for debugging), team(in base19), and largest # of weaknesses to any type on team all into CSV
        squad = ''.join([item for sublist in squad for item in sublist])
        csv_writer.writerows([[checktotal, squad, str(max(weaknesses))]])
