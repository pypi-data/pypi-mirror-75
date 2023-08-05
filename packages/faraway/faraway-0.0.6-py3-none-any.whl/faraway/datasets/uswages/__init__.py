DESCR = """
Weekly wages of US male workers in 1988

Description:

     The ‘uswages’ data frame has 2000 rows and 10 columns. Weekly
     Wages for US male workers sampled from the Current Population
     Survey in 1988.

Variables:

     This data frame contains the following columns:

     ‘wage’ Real weekly wages in dollars (deflated by personal
          consumption expenditures - 1992 base year)

     ‘educ’ Years of education

     ‘exper’ Years of experience

     ‘race’ 1 if Black, 0 if White (other races not in sample)

     ‘smsa’ 1 if living in Standard Metropolitan Statistical Area, 0 if
          not

     ‘ne’ 1 if living in the North East

     ‘mw’ 1 if living in the Midwest

     ‘we’ 1 if living in the West

     ‘so’ 1 if living in the South

     ‘pt’ 1 if working part time, 0 if not

Source:

     Bierens, H.J., and D. Ginther (2001): "Integrated Conditional
     Moment Testing of Quantile Regression Models", Empirical Economics
     26, 307-324
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'uswages.csv.bz2')
    return data
