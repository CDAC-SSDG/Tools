# README
This directory contains the files for searching a specific node within the AST, creating and verifying the AST. 

---



## json_creator.py
Creates a JSON file from the Clang's textual AST

**Usage:** 
```bash
python3 json_creator.py <ast_file> <json_file_output>
```

> [!Important]
> The script requires an AST file generated by the Clang's *-ast-dump* flag along with the path/name for the output json file

---

## json_verifier.py
Verifies the JSON generated.

**Usage:** 
```bash
python3 json_verifier.py <ast_file> <json_file>
```
> [!Important]
> The script requires an AST file generated by the clang along with the JSON file generated by the creator script

---

## json_splitter_mathematical_way.py
Splits the generated json into smaller chunks for rendering on the web page.

**Usage:** 
```bash
python3 json_splitter_mathematical_way.py <input_json_file> <output_directory> <max_nodes> <min_nodes>
```

> [!Important]
> The script requires the generated JSON file as a input along with an output directory to keep the splits. It also requires number of minimum & maximum nodes to be displayed on a web page.

> [!Note]
> If the rendering of web page takes time, decrease the number of *<max_node>* till rendering speed is satisfactory.

---

## node_path_finder.py
Finds the path to a specific node. Especially usefull in case of a node is buried deep inside the tree.

**Usage:**
```bash
python3 node_path_finder.py <full_ast.json> <node_name> <node_id>
```

> [!Important]
> This script reqruies the JSON file along with the node name and id to be searched for


