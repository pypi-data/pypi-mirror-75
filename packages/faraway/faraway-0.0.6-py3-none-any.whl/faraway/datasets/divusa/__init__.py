DESCR = """
Divorce in the USA 1920-1996

Variables:

     year the year from 1920-1996

     divorce divorce per 1000 women aged 15 or more

     unemployed unemployment rate

     femlab percent female participation in labor force aged 16+

     marriage marriages per 1000 unmarried women aged 16+

     birth births per 1000 women aged 15-44

     military military personnel per 1000 population

Source:

     Unknown
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'divusa.csv.bz2')
    return data
