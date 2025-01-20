#!/usr/bin/python3

"""
    This script is used to verify the json that has been created from AST by json_creator.py
"""

import sys
import re


# Display help message
def display_help_message():
    print("Usage:")
    print("\t python3 json_verifier.py <ast_file> <json_file>")
    print("\n Options available: \t (--help/-h)")
    exit(0)


# Get list of all id's in JSON
def get_json_file_id(filename):
    print("JSON FILE: ", filename, end="\t Found ")
    compile_object = re.compile("node_id\": \"0x[0-9a-f]+")
    list_json_id = []
    with open(filename, "r") as f:
        json_data = f.readlines()
    for line in json_data:
        if re.search(compile_object, line) is not None:
            search_object = re.search("0x[0-9a-f]+", line)
            list_json_id.append(line[search_object.start():search_object.end()])
    print(f"{len(list_json_id)} id's in JSON")
    return list_json_id, len(list_json_id)


# Get list of all ids in AST
def get_ast_file_id(filename):
    print("AST FILE: ", filename, end="\t Found ")
    id_list = []
    with open(filename, "r") as f:
        file_datalines = f.readlines()
    for line in file_datalines:
        search_object = re.search("0x[0-9a-f]+", line)
        if search_object is not None:
            id_list.append(line[search_object.start():search_object.end()])
    print(f"{len(id_list)} id's in AST")
    return id_list, len(id_list)


# Search & Compare the object id list
def compare_ids(ast_id_list, json_id_list):
    print(" ==== Comparing ID list ====")
    for ast_id in ast_id_list:
        if ast_id not in json_id_list:
            print(f"ID: {ast_id} found in AST but not JSON")
            return False
    return True


# Compare object id list using 1-1 matching method
def compare_ids2(ast_id_list, json_id_list):
    print(" ==== Comparing ID's one on one ====")
    for i in range(len(ast_id_list)):
        if ast_id_list[i] != json_id_list[i]:
            print(f"ERROR: \t AST ID: {ast_id_list[i]} matched with JSON ID: {json_id_list[i]}")
            return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        display_help_message()

    ast_filename = sys.argv[1]
    json_filename = sys.argv[2]

    list_of_ast_id, len_ast = get_ast_file_id(ast_filename)
    list_of_json_id, len_json = get_json_file_id(json_filename)

    if len_ast != len_json:
        print(f"{len_ast - len_json} id's missing")
        exit(0)

    if compare_ids2(list_of_ast_id, list_of_json_id):
        print(" JSON id's verified with AST")

    # if compare_ids(list_of_ast_id, list_of_json_id):
    #     print(" JSON id's verified with AST")

    print("\t Script complete!")
