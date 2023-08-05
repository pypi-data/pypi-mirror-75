DESCR = """
Career choice of high school students

Description:

     Data was collected as a subset of the "High School and Beyond"
     study conducted by the National Education Longitudinal Studies
     (NELS) program of the National Center for Education Statistics
     (NCES).

Variables:

     A data frame with 200 observations on the following 11 variables.

     ‘id’ ID of student

     ‘gender’ a factor with levels ‘female’ ‘male’

     ‘race’ a factor with levels ‘african-amer’ ‘asian’ ‘hispanic’
          ‘white’

     ‘ses’ socioeconomic class - a factor with levels ‘high’ ‘low’
          ‘middle’

     ‘schtyp’ school type - a factor with levels ‘private’ ‘public’

     ‘prog’ choice of high school program - a factor with levels
          ‘academic’ ‘general’ ‘vocation’

     ‘read’ reading score

     ‘write’ writing score

     ‘math’ math score

     ‘science’ science score

     ‘socst’ social science score

Details:

     One purpose of the study was to determine which factors are
     related to the choice of the type of program, academic, vocational
     or general, that the students pursue in high school.

Source:

     National Education Longitudinal Studies (NELS) program of the
     National Center for Education Statistics (NCES).
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'hsb.csv.bz2')
    return data
