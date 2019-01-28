
# coding: utf-8

# ## BigCo Assignment Algorithm


COMPANIES = """Anheuser Busch
Accuweather
Axa
Carnival
Citi
Citigroup Technology Inc
Comcast
Credit Karma
Dentons
E*TRADE
Farfetch
Intersection
Mastercard
Oracle
Pfizer
Samsung
TCS
The New York Times
Uber
Willis Towers Watson
Zillow""".split("\n")


import csv
FILENAME = "bigco_votes.csv"
file=open(FILENAME, "r")
votes = csv.reader(file)
VOTES = {}
TEAMS = []
for vote in votes:
    team_name = vote[17]
    TEAMS.append(team_name)
    VOTES[team_name] = {}
    for i in range(0,21):
        VOTES[team_name][COMPANIES[i]] = int(vote[20+i])



from ortools.linear_solver import pywraplp
solver = pywraplp.Solver('StudentProjectGridCBC', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
matches = {}
for c in COMPANIES:
    for t in TEAMS:
        matches[c, t] = solver.IntVar(0, 1, 'matches[%s,%s]' % (c, t))

z = solver.Sum( VOTES[t][c] * matches[c, t]
                 for t in TEAMS
                 for c in COMPANIES)

# One company MUST have 0 or 1 team.
for c in COMPANIES:
    solver.Add(solver.Sum([matches[c, t] for t in TEAMS]) <= 1)
# One team MUST have exactly 1 company.
for t in TEAMS:
    solver.Add(solver.Sum([matches[c, t] for c in COMPANIES]) == 1)
    
    print("Problem stated.")

objective = solver.Minimize(z)
solver.Solve()
s = solver.Objective().Value()


for t in TEAMS:
    for c in COMPANIES:
        if matches[c, t].SolutionValue() != 0:
            print("Team `%s` \t with company \t `%s`." % (t, c))

