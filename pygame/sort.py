"""Lexicographic sort order for leaves in a tree

This is currently being implemented directly in tskit under
[this issue](https://github.com/tskit-dev/tskit/issues/389). Once that is in
a release version of tskit, we may no longer need this file.
"""
import msprime

def helper(tree, node):
    children = tree.children(node)
    if len(children) == 0:
        return node, [node]
    if len(children) != 2:
        print("That's very interesting, node " + str(node) + " has " + len(children) + " children")
    # List comprehension for elegance
    children_return_values = [helper(tree, child) for child in children]
    children_return_values.sort()
    # print(children_return_values)
    min_lexi = []
    for element in children_return_values:
        min_lexi.extend(element[1])
    return children_return_values[0][0], min_lexi

def minlex(tree):
    """Given a tree, return a list of samples producing this tree that has
    minimum lexicographic order.
    """
    return helper(tree, tree.root)[1]

if __name__ == "__main__":
    # Great parameters! Save them
    ts = msprime.simulate(sample_size=10, length=1e6, random_seed=1,
        mutation_rate=1e-8, recombination_rate=1e-6)
    # ts.dump('example.trees')

    # ts = msprime.simulate(sample_size=20, length=1e8, random_seed=1,
    #     mutation_rate=1.65e-8, recombination_rate=1.2e-8)
    # ts.dump('example20.trees')

    print(ts.draw_text())

    for tree in ts.trees():
        print(minlex(tree))
