DESCR = """
1981 French Presidential Election

Description

Elections for the French presidency proceed in two rounds. In 1981, there were 10 candidates in the first round. The top two candidates then went on to the second round, which was won by Francois Mitterand over Valery Giscard-d'Estaing. The losers in the first round can gain political favors by urging their supporters to vote for one of the two finalists. Since voting is private, we cannot know how these votes were transferred, we might hope to infer from the published vote totals how this might have happened. Data is given for vote totals in every fourth department of France:


This dataframe contains the following columns (vote totals are in thousands)

EI
Electeur Inscrits (registered voters)

A
Voters for Mitterand in the first round

B
Voters for Giscard in the first round

C
Voters for Chirac in the first round

D
Voters for Communists in the first round

E
Voters for Ecology party in the first round

F
Voters for party F in the first round

G
Voters for party G in the first round

H
Voters for party H in the first round

I
Voters for party I in the first round

J
Voters for party J in the first round

K
Voters for party K in the first round

A2
Voters for Mitterand in the second round

B2
Voters for party Giscard in the second round

N
Difference between the number of voters in the second round and in the first round

Source

"The Teaching of Practical Statistics" by C.W. Anderson and R.M. Loynes, Wiley,1987
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'fpe.csv.bz2')
    return data
