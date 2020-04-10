""" Preprocessing module

Filters out small nodes and weak links not to overload graph visualization
"""

import sys
import itertools
import pickle
import json


def process(raw_tags_path, del_nodes_count=0, del_links_count=0, lower=True):

    with open(raw_tags_path, 'rb') as f:
        tags_list = pickle.load(f)

    if lower:
        tags_list = [[i.lower() for i in line] for line in tags_list]

    print(len(tags_list))
    # processing tags
    flattened_list = [i for line in tags_list for i in line]

    # filtering by occurrences count and counting words occurrences
    nodes_dict = {i: flattened_list.count(i) for i in set(flattened_list) if flattened_list.count(i) >= del_nodes_count}
    print(nodes_dict)

    # tags connection dict initialization
    formatted_tags = {(tag1, tag2): 0 for tag1, tag2 in itertools.permutations(set(nodes_dict.keys()), 2)}

    # count tags connection
    for line in tags_list:
        for tag1, tag2 in itertools.permutations(line, 2):
            if (tag1, tag2) in formatted_tags.keys():
                formatted_tags[(tag1, tag2)] += 1

    # filtering data with small number of links
    for k, v in formatted_tags.copy().items():
        if v < del_links_count:
            del formatted_tags[k]

    for k, v in formatted_tags.items():
        print(k, v)

    nodes = []
    links = []

    for pair, count in formatted_tags.items():
        links.append({"source": pair[0], "target": pair[1], "value": count})

    max_count = max(list(nodes_dict.values()))
    count_step = max_count // 7
    for node, count in nodes_dict.items():

        nodes.append({"id": node, "group": count // count_step, "popularity": count})

    data_to_dump = {"nodes": nodes, "links": links}

    print(data_to_dump)

    # rename file to use it
    phrase = raw_tags_path.split('_')[-1][:-4]
    with open(f'./data/proc-tags_{phrase}.json', 'w') as f:
        json.dump(data_to_dump, f)

    return formatted_tags


if __name__ == '__main__':
    raw_tags_path = sys.argv[1]
    process(raw_tags_path, del_nodes_count=0, del_links_count=0)