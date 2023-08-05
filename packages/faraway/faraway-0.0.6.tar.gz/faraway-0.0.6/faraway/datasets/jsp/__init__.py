DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'jsp.csv.bz2')
    return data
