DESCR = """
Yields of oat varieties planted in blocks

Description

Data from an experiment to compare 8 varieties of oats. The growing area was heterogeneous and so was grouped into 5 blocks. Each variety was sown once within each block and the yield in grams per 16ft row was recorded.


The dataset contains the following variables

grams
Yield in grams per 16ft row

block
Blocks I to V

variety
Variety 1 to 8

Source

"Statistical Theory in Research" by R. Anderson and T. Bancroft, McGraw Hill,1952


"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'oatvar.csv.bz2')
    return data
