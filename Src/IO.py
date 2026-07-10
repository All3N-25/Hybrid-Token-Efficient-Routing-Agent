"""
Read Inputs On ./Input/Tasks.json
Write Outputs On ./Output/Results.json
"""

import json
import os

def readTask():
    input_path = os.environ.get("INPUT_PATH", "../input/tasks.json")
    try:
        with open(input_path, encoding="utf-8") as file:
            tasks = json.load(file)

            if not isinstance(tasks, list):
                raise ValueError("Input must be a JSON array")

            for index, task in enumerate(tasks):
                if not isinstance(task, dict):
                    raise ValueError(f"Task {index} must be an object")

                for field in ("task_id", "prompt"):
                    if not isinstance(task.get(field), str) or not task[field].strip():
                        raise ValueError(f"Task {index} requires a non-empty {field}")
                    
            return tasks
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        return []
    except ValueError as ve:
        print(f"Error: {ve}")
        return []

def writeResult(results):
    output_path = os.environ.get("OUTPUT_PATH", "../output/results.json")
    with open(output_path, 'w', encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
