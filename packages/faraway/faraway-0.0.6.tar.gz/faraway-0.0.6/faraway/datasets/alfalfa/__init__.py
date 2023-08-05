DESCR = """
Effects of seed inoculum, irrigation and shade on alfalfa yield

Description:

     The ‘alfalfa’ data frame has 25 rows and 4 columns. Data comes
     from an experiment to test the effects of seed inoculum,
     irrigation and shade on alfalfa yield. A latin square design has
     been used.

Variables:

     This data frame contains the following columns:

     ‘shade’ Distance of location from tree line divided into 5 shade
          areas

     ‘irrigation’ Irrigation effect divided into 5 levels

     ‘inoculum’ Four types of seed incolum, A-D with E as control.

     ‘yield’ Dry matter yield of alfalfa

Source:

     Petersen, R.G. 1994. Agricultural Field Experiments, Design and
     Analysis. Marcel Dekker, Inc., New York.  Pages 70-74. 1994
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'alfalfa.csv.bz2')
    return data
