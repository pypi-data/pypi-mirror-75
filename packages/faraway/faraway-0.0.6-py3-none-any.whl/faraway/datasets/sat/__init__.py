DESCR = """
School expenditure and test scores from USA in 1994-95

Description:

     The ‘sat’ data frame has 50 rows and 7 columns.  Data were
     collected to study the relationship between expenditures on public
     education and test results.

Variables:

     This data frame contains the following columns:

     ‘expend’ Current expenditure per pupil in average daily attendance
          in public elementary and secondary schools, 1994-95 (in
          thousands of dollars)

     ‘ratio’ Average pupil/teacher ratio in public elementary and
          secondary schools, Fall 1994

     ‘salary’ Estimated average annual salary of teachers in public
          elementary and secondary schools, 1994-95 (in thousands of
          dollars)

     ‘takers’ Percentage of all eligible students taking the SAT,
          1994-95

     ‘verbal’ Average verbal SAT score, 1994-95

     ‘math’ Average math SAT score, 1994-95

     ‘total’ Average total score on the SAT, 1994-95

Source:

     "Getting What You Pay For: The Debate Over Equity in Public School
     Expenditures" D. Guber, Journal of Statistics Education, 1999
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'sat.csv.bz2')
    return data
