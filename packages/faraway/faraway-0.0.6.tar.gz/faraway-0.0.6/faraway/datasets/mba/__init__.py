DESCR = """
Description:

     Data were collected from 39 students in a University of Chicago
     MBA class

Variables:

     A data frame with 39 observations on the following 5 variables.

     happy Happiness on a 10 point scale where 10 is most happy

     money family income in thousands of dollars

     sex 1 = satisfactory sexual activity, 0 = not

     love 1 = lonely, 2 = secure relationships, 3 = deep feeling of
          belonging and caring

     work 5 point scale where 1 = no job, 3 = OK job, 5 = great job

Source:

     George and McCulloch (1993) "Variable Selection via Gibbs
     Sampling" JASA, 88, 881-889
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'mba.csv.bz2')
    return data
