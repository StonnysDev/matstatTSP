import json


def write_task(new_task_condition, answers, right_answer, taskType):
    task_data = {
        "question": new_task_condition.strip(),
        "choices": [a.strip() for a in answers],
        "correct": right_answer
    }
    filename = './data/matstat_tasks.txt' if taskType == 'matstat' else './data/TSP_tasks.txt'
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task_data, ensure_ascii=False) + '\n')


def get_tasks(taskType):
    filename = './data/matstat_tasks.txt' if taskType == 'matstat' else './data/TSP_tasks.txt'
    tasks = []
    ind = 1
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        task = json.loads(line)
                        task["ind"] = ind
                        ind += 1
                        tasks.append(task)
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        pass
    return tasks