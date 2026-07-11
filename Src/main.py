from IO import readTask, writeResult
from Classifier import classify_prompt
from DataClass.Task import Task
from Model import fireworks, local


FIREWORKS_CATEGORIES = {
    "Mathematical Reasoning",
    "Code Debugging",
    "Logical / Deductive Reasoning",
    "Code Generation",
}


def answer_task(task: Task) -> str:
    if task.complexity == "Complex" or FIREWORKS_CATEGORIES.intersection(task.categories):
        return fireworks.generate(task.prompt, task.categories)
    if task.complexity == "Simple":
        return local.generate(task.prompt)
    raise ValueError(f"Unknown complexity: {task.complexity}")

if __name__ == "__main__":
    print("Simple Hybrid Token Routing Agent is running.")
    print("Reading tasks...")

    tasks = readTask()

    if not tasks:
        print("No tasks to process.")
        exit()

    results = []

    for task in tasks:
        prompt = task.get("prompt", "")
        classification = classify_prompt(prompt)
        classified_task = Task(
            task_id=task.get("task_id"),
            prompt=prompt,
            categories=classification["categories"],
            complexity=classification["complexity"]
        )
        # print(
        #     f"Task ID: {classified_task.task_id}, "
        #     f"Categories: {classified_task.categories}, "
        #     f"Complexity: {classified_task.complexity}"
        # )
        results.append({
            "task_id": classified_task.task_id,
            "answer": answer_task(classified_task),
        })

    writeResult(results)
    print(fireworks.fireworks_tokens_used)
