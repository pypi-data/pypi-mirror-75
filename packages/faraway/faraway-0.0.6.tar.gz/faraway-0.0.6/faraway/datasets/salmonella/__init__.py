DESCR = """
Salmonella reverse mutagenicity assay

Description:

     The data was collected in a salmonella reverse mutagenicity assay
     where the numbers of revertant colonies of TA98 Salmonella
     observed on each of three replicate plates for different doses of
     quinoline

Variables:

     A data frame with 18 observations on the following 2 variables.

     colonies numbers of revertant colonies of TA98 Salmonella

     dose dose level of quinoline

Source:

     Breslow N.E. (1984), Extra-Poisson Variation in Log-linear Models,
     ApplStat, pp. 38-44.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'salmonella.csv.bz2')
    return data
