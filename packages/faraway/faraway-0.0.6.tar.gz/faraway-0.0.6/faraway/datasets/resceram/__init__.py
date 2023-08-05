DESCR = """
Shape and plate effects on current noise in resistors

Description:

     The ‘resceram’ data frame has 12 rows and 3 columns. Shape and
     plate effects on current noise in resistors

Variables:

     This data frame contains the following columns:

     ‘noise’ current noise

     ‘shape’ the geometrical shape of the resistor, A, B, C or D

     ‘plate’ the ceramic plate on which the resistor was mounted. Only
          three resistors will fit on one plate.

Source:

     Natrella, M (1963) "Experimental Statistics" National Bureau of
     Standards Handbook 91, Gaithersburg MD.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'resceram.csv.bz2')
    return data
