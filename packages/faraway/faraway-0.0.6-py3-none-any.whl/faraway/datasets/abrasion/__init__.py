DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'abrasion.csv.bz2')
    return data
