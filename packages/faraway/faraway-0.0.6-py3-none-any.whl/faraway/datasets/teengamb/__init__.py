DESCR = """
Study of teenage gambling in Britain

Description:

     The ‘teengamb’ data frame has 47 rows and 5 columns. A survey was
     conducted to study teenage gambling in Britain.

Variables:

     This data frame contains the following columns:

     ‘sex’ 0=male, 1=female

     ‘status’ Socioeconomic status score based on parents' occupation

     ‘income’ in pounds per week

     ‘verbal’ verbal score in words out of 12 correctly defined

     ‘gamble’ expenditure on gambling in pounds per year

Source:

     Ide-Smith & Lea, 1988, Journal of Gambling Behavior, 4, 110-118
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'teengamb.csv.bz2')
    return data
