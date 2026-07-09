from IO import readTask, writeResult
from Classifier import classify_prompt


if __name__ == "__main__":
    print("Simple Hybrid Token Routing Agent is running.")
    print("Reading tasks...")

    tasks = readTask()

    if tasks:
        print(f"Total tasks read: {len(tasks)}")
        results = []
        for task in tasks:
            prompt = task.get("prompt", "")
            classification = classify_prompt(prompt)
            results.append({
                "task_id": task.get("task_id"),
                "category": classification["category"],
                "difficulty": classification["difficulty"]
            })
        writeResult(results)
        print("Results written to ./Output/Results.json"
        )

