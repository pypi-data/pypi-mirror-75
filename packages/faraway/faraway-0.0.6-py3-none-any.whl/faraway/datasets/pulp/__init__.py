DESCR = """
Brightness of paper pulp depending on shift operator

Description:

     The ‘pulp’ data frame has 20 rows and 2 columns. Data comes from
     an experiment to test the paper brightness depending on a shift
     operator.

Variables:

     This data frame contains the following columns:

     ‘bright’ Brightness of the pulp as measured by a reflectance meter

     ‘operator’ Shift operator a-d

Source:

     "Statistical techniques applied to production situations" F.
     Sheldon (1960) Industrial and Engineering Chemistry, 52, 507-509
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'pulp.csv.bz2')
    return data
