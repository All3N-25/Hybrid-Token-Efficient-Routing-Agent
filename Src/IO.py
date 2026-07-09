"""
Read Inputs On ./Input/Tasks.json
Write Outputs On ./Output/Results.json
"""

import json

def readTask():
    with open('./Input/Tasks.json', 'r') as file:
        tasks = json.load(file)
    return tasks

def writeResult(results):
    with open('./Output/Results.json', 'w', encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

def writeResultToFile(results, filename):
    pass