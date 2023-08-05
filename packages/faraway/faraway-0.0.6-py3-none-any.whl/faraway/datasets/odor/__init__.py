DESCR = """
Odor of chemical by production settings

Description:

     Data from an experiment to determine the effects of column
     temperature, gas/liquid ratio and packing height in reducing
     unpleasant odor of chemical product that was being sold for
     household use

Variables:

     ‘odor’ Odor score

     ‘temp’ Temperature coded as -1, 0 and 1

     ‘gas’ Gas/Liquid ratio coded as -1, 0 and 1

     ‘pack’ Packing height coded as -1, 0 and 1

Source:

     "Statistical Design and Analysis of Experiments" by P. John,
     Macmillan, 1971
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'odor.csv.bz2')
    return data
