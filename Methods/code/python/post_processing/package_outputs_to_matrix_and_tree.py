"""Convert package outputs to lmpy.Matirx and TreeWrapper
"""
import json
import numpy as np
from lmpy import Matrix, TreeWrapper


# .............................................................................
def get_squidded_tree(tree_fn, tree_schema, squid_json):
    tree = TreeWrapper.get(path=tree_fn, schema=tree_schema)
    json_data_lines = []
    with open(squid_json) as in_file:
        first_line = True
        for line in in_file:
            if first_line:
                first_line = False
            else:
                json_data_lines.append(line)
    squid_list_json = json.loads(''.join(json_data_lines))
    squid_dict = {i['scientific_name'].replace('_', ' '): i['header'] for i in squid_list_json}
    tree.annotate_tree_tips('squid', squid_dict)
    return tree


# .............................................................................
def get_matrix(csv_fn):
    squids = []
    row_headers = []
    #data = None
    data = []
    with open(csv_fn) as in_file:
        header = True
        for line in in_file:
            if header:
                header = False
                squids = line.strip().split(',')[3:]
                #data = np.zeros(())
            else:
                parts = line.strip().split(',')
                row_headers.append(tuple([float(i) for i in parts[0:3]]))
                data.append([int(i) for i in parts[3:]])
    #print(len(row_headers))
    #print(len(squids))
    #259200
    #print(squids)
    mtx = Matrix(
        np.array(data, dtype=np.int0), headers={'0': row_headers, '1': squids})
    return mtx


# .............................................................................
if __name__ == '__main__':
    tree = get_squidded_tree(
        'C:/Users/cj/Desktop/ryan_v3/gridset/tree.nex', 'nexus',
        'C:/Users/cj/Desktop/ryan_v3/package/squidLookup.json')
    tree.write(
        path='C:/Users/cj/Desktop/ryan_v3/squid_tree.nex', schema='nexus')
    pam = get_matrix('C:/Users/cj/Desktop/ryan_v3/gridset/matrix/pam_583.csv')
    with open('C:/Users/cj/Desktop/ryan_v3/pam.lmm', 'wb') as out_file:
        pam.save(out_file)
