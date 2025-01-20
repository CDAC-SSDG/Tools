#!/usr/bin/python3
"""
    This script is used for finding the path from the root node to a particular node
"""

import sys
import json


# Function to display help message
def display_help_message():
    print(" \033[92m Usage:")
    print("\t\033[96m python3 node_path_finder.py <full_ast.json> <node_name> <node_id>")
    print("\n\033[93m Note:\033[0m <node_name> & <node_id> are case insensitive")
    exit(0)


# Function to load json file
def load_json(filename):
    print("\033[93m Loading json: \033[92m", filename, "\033[0m")
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data


class SearchNode:
    def __init__(self, s_name, s_id):
        self.search_item = s_name + "-" + s_id
        self.path = []
        self.path_found = False
        print(f" \033[93mSearching for \033[92m{self.search_item}")

    # Function to recurse Tree
    def recurse_tree(self, node):
        # add node to path
        if 'node_id' in node.keys():
            path_item = node['node_name'].strip() + "-" + node['node_id'].strip()
        else:
            path_item = node['node_name'].strip() + "-" + "0x00"
        self.path.append(path_item)

        # check if item found
        if self.search_item == path_item.lower():
            self.pretty_print_path()

        if "child" in node.keys():
            if type(node['child']) is dict:
                self.recurse_tree(node['child'])
            if type(node['child']) is list:
                for i in range(len(node['child'])):
                    self.recurse_tree(node['child'][i])

        # remove node from path
        self.path.pop()

    # Function to pretty print path
    def pretty_print_path(self):
        print("\033[93m Node found!")
        for item in self.path:
            print(f" \033[93m--> \033[96m{item}", end="")
        print("\n\033[0m")
        self.path_found = True


if __name__ == '__main__':
    if len(sys.argv) != 4:
        display_help_message()

    json_filename = sys.argv[1].strip()
    search_node_name = sys.argv[2].strip().lower()
    search_node_id = sys.argv[3].strip().lower()

    json_data = load_json(json_filename)
    obj = SearchNode(search_node_name, search_node_id)
    if type(json_data) is list:
        for f in json_data:
            obj.recurse_tree(f)
    if type(json_data) is dict:
        obj.recurse_tree(json_data)

    if not obj.path_found:
        print(f"\033[91m Node {search_node_name} with id {search_node_id} not found in", end=" ")
        print("\033[92m{json_filename}\033[91m!\033[0m")
    print(" Script complete!")
