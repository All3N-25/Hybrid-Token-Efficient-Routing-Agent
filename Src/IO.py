"""
Read Inputs On ./Input/Tasks.json
Write Outputs On ./Output/Results.json
"""

import json

def readTask():
    try:
        with open("./input/tasks.json", encoding="utf-8") as file:
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
        print("Error: Input file './input/tasks.json' not found.")
        return []
    except ValueError as ve:
        print(f"Error: {ve}")
        return []

def writeResult(results):
    with open('./output/results.json', 'w', encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)