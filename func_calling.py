from google.genai import types
from config import WORKING_DIR
from functions.tools_schema import function_map, schemas

available_functions = types.Tool(
        function_declarations=[
            schemas["schema_get_files_info"],
            schemas["schema_get_file_content"],
            schemas["schema_write_file"],
            schemas["schema_run_python_file"]
        ]
    )

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name} ({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")  
          
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )