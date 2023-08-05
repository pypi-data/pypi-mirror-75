DESCR = """
Diabetes survey on Pima Indians

Description

The National Institute of Diabetes and Digestive and Kidney Diseases conducted a study on 768 adult female Pima Indians living near Phoenix.

Usage

data(pima)
Format

The dataset contains the following variables

pregnant
Number of times pregnant

glucose
Plasma glucose concentration at 2 hours in an oral glucose tolerance test

diastolic
Diastolic blood pressure (mm Hg)

triceps
Triceps skin fold thickness (mm)

insulin
2-Hour serum insulin (mu U/ml)

bmi
Body mass index (weight in kg/(height in metres squared))

diabetes
Diabetes pedigree function

age
Age (years)

test
test whether the patient shows signs of diabetes (coded 0 if negative, 1 if positive)

Source

The data may be obtained from UCI Repository of machine learning databases at http://archive.ics.uci.edu/ml/
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'pima.csv.bz2')
    return data
