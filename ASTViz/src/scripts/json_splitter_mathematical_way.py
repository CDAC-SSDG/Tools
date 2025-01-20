#!/usr/bin/python3
"""
    Uses a mathematical approach to make dynamic json split files

    Logic:
            Do this till number of nodes reached is max_node_value
            {
                If no_of_child > threshold_value, then
                    split the children in groups till every group has threshold_value
                else:
                    continue down one of the child and repeat the process
            }
"""
import os
import json
import sys


class JSONSplitter:
    def __init__(self, max_value, min_value, directory):
        # self.threshold_value = t_value
        # self.acceptable_error = e_value
        # self.node_counter = 0
        self.output_directory = directory
        self.no_of_node_ahead = 0
        self.max_nodes = max_value
        self.min_nodes = min_value

    # Function to create split json
    def create_split(self, node, counter):
        # TODO: ADD CODE FOR CREATING SPLIT VERSIONS OF FILES - done
        if 'node_id' in node.keys():
            filename = node['node_id'].strip() + "-" + node['node_name'].strip()
        else:
            filename = "NO_ID-" + node['node_name'].strip()
        filename = self.suggest_filename(filename)
        print(f"\033[93m Created splitfile \033[96m{filename}\033[93m with \033[96m{counter}\033[93m nodes\033[0m")
        with open(filename, "w") as fp:
            json.dump(node, fp, sort_keys=False, indent=2)
        # self.node_counter = 1

    # Function to scope ahead
    def scope_ahead(self, node):
        if 'child' in node.keys():
            if type(node['child']) is dict:
                self.scope_ahead(node['child'])
            if type(node['child']) is list:
                for child in node['child']:
                    self.scope_ahead(child)
        self.no_of_node_ahead += 1

    # Function to make decision on subtree formation
    def make_decision(self, current_counter):
        parameter = self.no_of_node_ahead + current_counter
        if parameter > self.max_nodes:
            return True
        if self.min_nodes <= current_counter <= self.max_nodes:
            return True
        # TODO: ADD MORE CONDITIONS LIKE ERROR THRESHOLD FOR DIFFERENT RESULTS
        return False

    # Function to suggest a filename
    def suggest_filename(self, filename):
        if os.path.isfile(self.output_directory + filename + "-0.json"):
            for f in range(9999):
                if not os.path.isfile(self.output_directory + filename + f"-{f}.json"):
                    return self.output_directory + filename + f"-{f}.json"
        else:
            return self.output_directory + filename + "-0.json"

    # Function to traverse a tree
    def traverse_tree(self, node):
        counter = 0
        if 'node_id' in node.keys():
            partial_node = {"node_name": node['node_name'], "node_id": node['node_id']}
        else:
            partial_node = {"node_name": node['node_name']}
        if 'metadata' in node.keys():
            partial_node['metadata'] = node['metadata']

        if 'child' in node.keys():
            if type(node['child']) is dict:
                partial_node['child'], return_counter = self.traverse_tree(node['child'])
                counter += return_counter
                if self.make_decision(counter):
                    self.create_split(partial_node, counter)
                    counter = 0
            if type(node['child']) is list:
                partial_node['child'] = []
                for itr in range(len(node['child'])):
                    temp_node, return_counter = self.traverse_tree(node['child'][itr])
                    counter += return_counter
                    partial_node['child'].append(temp_node)
                    if itr != len(node['child'])-1:
                        self.scope_ahead(node['child'][itr+1])
                        if self.make_decision(counter):
                            self.create_split(partial_node, counter)
                            partial_node['child'] = []
                            counter = 0
                    self.no_of_node_ahead = 0

        counter += 1
        return partial_node, counter


# check if output directory exists if not then create one
def check_for_output_dir(directory):
    if not os.path.isdir(directory):
        print("\033[93m Directory not found! \n Creating directory: ", directory, "\033[0m")
        os.mkdir(directory)


# load the json file
def load_json_file(filename):
    print("\033[93m Loading file: ", filename, "\033[0m\n")
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data


# Function to display script help message
def display_help_message():
    print("\033[1:31m Usage :")
    print("\t python3 json_splitter_mathematical_way.py <input_json_file> <output_directory> <max_nodes> <min_nodes>")
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        display_help_message()

    # set variables
    input_json_filename = sys.argv[1]
    output_directory = sys.argv[2]
    threshold_value = int(sys.argv[3])
    acceptable_error = int(sys.argv[4])

    print("\033[1m\033[34m", end="")
    print("=========================")
    print(" Script parameters: ")
    print("=========================")
    print("\033[0m\033[3m\033[3;36m", end="")
    print(f" Input json file: {input_json_filename}")
    print(f" Output directory: {output_directory}")
    print(f" Maximum number of nodes: {threshold_value}")
    print(f" Minimum number of nodes: {acceptable_error}\033[0m\n")

    # start with the process
    check_for_output_dir(output_directory)
    json_data = load_json_file(input_json_filename)
    obj = JSONSplitter(threshold_value, acceptable_error, output_directory)

    if type(json_data) is list:
        for part in json_data:
            return_node, temp_counter = obj.traverse_tree(part)
            obj.create_split(return_node, temp_counter)
    else:
        return_node, temp_counter = obj.traverse_tree(json_data)
        obj.create_split(return_node, temp_counter)

    print("\033[92m \nPROCESS COMPLETED!\033[0m")
