DESCR = """
     Life expectancy, doctors and televisions collected on 38 countries
     in 1993

Variables:

     ‘life’ Life expectancy in years

     ‘tv’ Number of people per television set

     ‘doctor’ Number of people per doctor

Source:

     Unknown, data for illustration purposes only

"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'tvdoctor.csv.bz2')
    return data
