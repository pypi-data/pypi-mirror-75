DESCR = """
Corrosion loss in Cu-Ni alloys

Description

Data consist of thirteen specimens of 90/10 Cu-Ni alloys with varying iron content in percent. The specimens were submerged in sea water for 60 days and the weight loss due to corrosion was recorded in units of milligrams per square decimeter per day.

This dataframe contains the following columns

Fe
Iron content in percent

loss
Weight loss in mg per square decimeter per day

Source

"Applied Regression Analysis" by N. Draper and H. Smith, Wiley, 1998
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'corrosion.csv.bz2')
    return data
