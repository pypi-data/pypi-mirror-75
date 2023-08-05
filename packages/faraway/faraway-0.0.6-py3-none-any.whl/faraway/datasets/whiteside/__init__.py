DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'whiteside.csv.bz2')
    return data
