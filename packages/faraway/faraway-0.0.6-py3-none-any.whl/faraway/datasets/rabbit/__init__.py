DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'rabbit.csv.bz2')
    return data
