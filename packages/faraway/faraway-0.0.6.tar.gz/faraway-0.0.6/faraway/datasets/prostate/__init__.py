DESCR = """
Prostate cancer surgery

Description:

     The ‘prostate’ data frame has 97 rows and 9 columns. A study on 97
     men with prostate cancer who were due to receive a radical
     prostatectomy.

Variables:

     This data frame contains the following columns:

     ‘lcavol’ log(cancer volume)

     ‘lweight’ log(prostate weight)

     ‘age’ age

     ‘lbph’ log(benign prostatic hyperplasia amount)

     ‘svi’ seminal vesicle invasion

     ‘lcp’ log(capsular penetration)

     ‘gleason’ Gleason score

     ‘pgg45’ percentage Gleason scores 4 or 5

     ‘lpsa’ log(prostate specific antigen)

Source:

     Andrews DF and Herzberg AM (1985): Data. New York: Springer-Verlag
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'prostate.csv.bz2')
    return data
