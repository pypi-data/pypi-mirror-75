DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'chredlin.csv.bz2')
    return data
