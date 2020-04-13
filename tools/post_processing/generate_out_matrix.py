"""Generate stats"""

from lmpy import Matrix, TreeWrapper

from biotaphy.analyses.pam_stats.site_statistics import (
    calculate_tree_site_statistics)


# .............................................................................
def main():
    pam_fn = 'C:/Users/cj/Desktop/ryan_v3/pam.lmm'
    tree_fn = 'C:/Users/cj/Desktop/ryan_v3/squid_tree.nex'
    out_fn = 'C:/Users/cj/Desktop/ryan_v3/tree_mtx.lmm'

    with open(pam_fn, 'rb') as in_file:
        pam = Matrix.load_flo(in_file)
    tree = TreeWrapper.get(path=tree_fn, schema='nexus')
    tree_mtx = calculate_tree_site_statistics(pam, tree)
    with open(out_fn, 'wb') as out_file:
        tree_mtx.save(out_file)
    print(tree_mtx.max(axis=1))
    print(tree_mtx.max(axis=0))


# .............................................................................
if __name__ == '__main__':
    main()
