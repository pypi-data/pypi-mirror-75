DESCR = """
Denim wastage by supplier

Description:

     Five suppliers cut denim material for a jeans manufacturer. An
     algorithm is used to estimate how much material will be wasted
     given the dimensions of the material supplied. Typically, a
     supplier wastes more material than the target based on the
     algorithm although occasionally they waste less. The percentage of
     waste relative to target was collected weekly for the 5 suppliers.
     In all, 95 observations were recorded.

Variables:

     A data frame with 95 observations on the following 2 variables.

     ‘waste’ percentage wastage

     ‘supplier’ a factor with levels ‘1’ ‘2’ ‘3’ ‘4’ ‘5’

Source:

     Unknown

Examples:

     data(denim)
     ## maybe str(denim) ; plot(denim) ...
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'denim.csv.bz2')
    return data
