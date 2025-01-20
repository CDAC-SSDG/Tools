#!/usr/bin/python3

"""
    THIS PYTHON SCRIPT IS USED FOR CREATING JSON FORMAT OF AST OBTAINED FROM CLANG++
"""

import sys
import json
import re

is_previous_sibling = False


# Display help message
def display_help():
    print("Usage:")
    print("\t python3 json_creator.py <ast_file> <json_file_output>")
    print("\n Options available: \t (--help/-h)")
    exit(0)


# Reads the ast file line by line
def read_ast_file(filename):
    print("\t Reading AST data")
    with open(filename, "r") as f:
        data = f.readlines()
    return data


# Print the AST data read
def display_ast_file(ast_file_data):
    print(ast_file_data)


# Parse metadata
def parse_metadata(statement):
    metadata = "NO DATA PRESENT"
    regex_object = re.search("<<.*[a-z0-9]>", statement)
    if regex_object is not None:
        metadata = statement[regex_object.start():regex_object.end()]
        return metadata, regex_object.end()

    regex_object = re.search("<.*> ", statement)
    if regex_object is not None:
        metadata = statement[regex_object.start():regex_object.end() - 1]
        return metadata, regex_object.end()
    search_object = re.search("0x[0-9a-f]+ ", statement)
    if search_object is None:
        return metadata, re.search("[A-Za-z]+\s*", statement).end()
    return metadata, search_object.end()


# Recurse over the ast file data to create json
def recurse_line(statements, line_number, is_current_sibling=False):
    partial_dict = {}
    siblings = []
    visited_line_number = line_number
    statement = statements[line_number].strip("\n")

    # If regex matches it is the program root else other stuff
    if re.search("^[A-Za-z]", statement) is not None:
        partial_dict["node_name"] = statement.split()[0]
    else:
        index_range = re.search("[A-Za-z]+\s*", statement)
        partial_dict["node_name"] = statement[index_range.start():index_range.end()].strip()

    # Special case for handling current <<<NULL>>> node
    if partial_dict["node_name"] == "NULL":
        partial_dict["node_name"] = "<<<NULL>>>"
        while visited_line_number+1 < len(statements):
            index_next_statement = re.search("[A-Za-z]", statements[visited_line_number + 1]).start()
            if statements[visited_line_number + 1][index_next_statement:index_next_statement + 4] == "NULL":
                index_next_statement -= 3
            index_current_statement = re.search("<<<NULL", statements[line_number]).start()
            if index_next_statement > index_current_statement:
                print("ERROR: Found a NULL statement with child which shouldn't be possible!")
                print("line number: ", visited_line_number+1)
                partial_dict["child"], visited_line_number = recurse_line(statements, visited_line_number + 1, False)
            elif index_next_statement == index_current_statement:
                if is_current_sibling:
                    return partial_dict, visited_line_number
                if len(siblings) < 2:
                    siblings = [partial_dict]
                partial_dict, visited_line_number = recurse_line(statements, visited_line_number + 1, True)
                siblings.append(partial_dict)
                partial_dict = siblings
            else:
                return partial_dict, visited_line_number
        return partial_dict, visited_line_number

    index_range = re.search("0x[0-9a-f]+ ", statement)
    if index_range is not None:
        partial_dict["node_id"] = statement[index_range.start():index_range.end()-1]
    else:
        partial_dict["node_id"] = "NODE ID NOT FOUND"
    return_value = parse_metadata(statement)
    partial_dict["metadata"] = return_value[0]

    # In case some AST data is left it's added
    if len(statement) - int(return_value[1]) > 0:
        partial_dict["extra_data"] = statement[int(return_value[1]):]

    # Start the recursion monster here

    while visited_line_number+1 < len(statements):
        index_next_statement = re.search("[A-Za-z]", statements[visited_line_number + 1]).start()
        # If NULL found next line adjust the cursor head
        if statements[visited_line_number+1][index_next_statement:index_next_statement+4] == "NULL":
            index_next_statement -= 3
        index_current_statement = re.search("[A-Za-z]", statements[line_number]).start()
        if index_next_statement > index_current_statement:
            partial_dict["child"], visited_line_number = recurse_line(statements, visited_line_number + 1, False)
        elif index_next_statement == index_current_statement:
            if is_current_sibling:
                return partial_dict, visited_line_number
            if len(siblings) < 2:
                siblings = [partial_dict]
            partial_dict, visited_line_number = recurse_line(statements, visited_line_number + 1, True)
            siblings.append(partial_dict)
            partial_dict = siblings
        else:
            return partial_dict, visited_line_number
    return partial_dict, visited_line_number


# Display json formed
def display_json(json_data):
    print("JSON CREATED")
    print(json.dumps(json_data, sort_keys=False, indent=2))


# Write the json data obtained in a file
def write_json_file(filename, json_data):
    with open(filename, "w") as f:
        json.dump(json_data, f, sort_keys=False, indent=2)
    print(f"\t {filename} CREATED WITH JSON DATA")


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        display_help()

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    print(f"SCRIPT LOGS \n\t Input file: {input_filename} \t Output file: {output_filename}")

    ast_data = read_ast_file(input_filename)
    # display_ast_file(ast_data)
    print("\tCreating JSON from AST")
    json_data, visited_line = recurse_line(ast_data, 0, False)
    # json_data = create_json_data(ast_data)
    write_json_file(output_filename, json_data)
    # display_json(json_data)
