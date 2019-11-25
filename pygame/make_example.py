import tskit

if __name__ == "__main__":
    tables = tskit.TableCollection(sequence_length=10)
    node_samples = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    node_heights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    edges = [
        [10, 1, 0, 5],
        [10, 9, 0, 5],
        [11, 1, 5, 10],
        [11, 5, 5, 10],
        [12, 4, 0, 10],
        [12, 5, 0, 5],
        [12, 11, 5, 10],
        [13, 8, 0, 10],
        [13, 9, 5, 10],
        [13, 10, 0, 5],
        [14, 3, 0, 10],
        [14, 12, 0, 10],
        [15, 7, 0, 10],
        [15, 13, 0, 10],
        [16, 2, 0, 10],
        [16, 14, 0, 10],
        [17, 6, 0, 10],
        [17, 15, 0, 10],
        [18, 0, 0, 10],
        [18, 16, 0, 10],
        [19, 17, 0, 10],
        [19, 18, 0, 10]
    ]
    for i in range(len(node_samples)):
        sample = tskit.NODE_IS_SAMPLE if node_samples[i] else not tskit.NODE_IS_SAMPLE
        tables.nodes.add_row(flags=sample, time=node_heights[i])
    for edge in edges:
        tables.edges.add_row(left=edge[2], right=edge[3], parent=edge[0], child=edge[1])

    # We need to sort the edges in order of increasing parent height
    # tables.sort()
    ts = tables.tree_sequence()
    print(ts.draw_text())
    ts.dump('example.trees')
