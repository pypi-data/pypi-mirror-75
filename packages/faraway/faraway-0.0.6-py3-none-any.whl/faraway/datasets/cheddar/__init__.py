DESCR = """
Taste of Cheddar cheese

Description:

     In a study of cheddar cheese from the LaTrobe Valley of Victoria,
     Australia, samples of cheese were analyzed for their chemical
     composition and were subjected to taste tests. Overall taste
     scores were obtained by combining the scores from several tasters.

Variables:

     A data frame with 30 observations on the following 4 variables.

     ‘taste’ a subjective taste score

     ‘Acetic’ concentration of acetic acid (log scale)

     ‘H2S’ concentration of hydrogen sulfice (log scale)

     ‘Lactic’ concentration of lactic acid

Source:

     Moore, David S., and George P. McCabe (1989). Introduction to the Practice of Statistics.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'cheddar.csv.bz2')
    return data
