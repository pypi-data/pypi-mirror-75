DESCR = """
Ankylosing Spondylitis

Description:

     Data from Royal Mineral Hospital in Bath. AS is a chronic form of
     arthritis. A study conducted to determine whether daily stretching
     of the hip tissues would improve mobility.  39 ``typical'' AS
     patients were randomly allocated to control (standard treatment)
     group or the treatment group in a 1:2 ratio.  Responses were
     flexion and rotation angles at the hip measured in degrees. Larger
     numbers indicate more flexibility.

Variables:

     A data frame with 78 observations on the following 7 variables.

     ‘fbef’ flexion angle before

     ‘faft’ flexion angle after

     ‘rbef’ rotation angle before

     ‘raft’ rotation angle after

     ‘grp’ treatment group - a factor with levels ‘control’ ‘treat’

     ‘side’ side of the body - a factor with levels ‘right’ ‘left’

     ‘person’ id for the individual

Source:
     Chatfield C. (1995) Problem Solving: A Statistician's Guide, 2ed
     Chapman Hall.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'hips.csv.bz2')
    return data
