from IO import readTask, writeResult
from Classifier import classify_prompt
from Src.DataClass.Task import Task

if __name__ == "__main__":
    print("Simple Hybrid Token Routing Agent is running.")
    print("Reading tasks...")

    tasks = readTask()

    if not tasks:
        print("No tasks to process.")
        exit()

    for task in tasks:
        prompt = task.get("prompt", "")
        classification = classify_prompt(prompt)
        classified_task = Task(
            task_id=task.get("task_id"),
            prompt=prompt,
            categories=classification["categories"],
            complexity=classification["complexity"]
            )
