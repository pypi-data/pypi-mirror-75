DESCR = """
Blood clotting times

Description:

     The clotting times of blood for plasma diluted with nine different
     percentage concentrations with prothrombin-free plasma

Variables:

     This data frame contains the following columns:

     ‘time’ time in seconds to clot

     ‘conc’ concentration in percent

     ‘lot’ lot number - either one or two

Source:
     Hurn et al (1945)

References:
     Nelder & McCullagh (1989) Generalized Linear Models (2ed)
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'clot.csv.bz2')
    return data
