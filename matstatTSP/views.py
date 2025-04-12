from django.shortcuts import render
from django.core.cache import cache
from . import tasks_work


def index(request):
    return render(request, "index.html")


def matstat_tasks(request):
    return display_tasks(request, "matstat")


def TSP_tasks(request):
    return display_tasks(request, "TSP")


def display_tasks(request, task_type):
    tasks = tasks_work.get_tasks(task_type)
    context = {
        'tasks': tasks
    }
    return render(request, f'{task_type}_tasks.html', context)


def matstat_answers(request):
    return process_answers(request, "matstat")


def TSP_answers(request):
    return process_answers(request, "TSP")


def process_answers(request, task_type):
    if request.method == "POST":
        tasks = tasks_work.get_tasks(task_type)
        correct_answers = 0
        all_valid = True
        results = []
        for task in tasks:
            user_answer = request.POST.get(f'answer_{task["ind"]}')
            if user_answer in ["1", "2", "3", "4"]:  
                if user_answer == task["correct"]:
                    correct_answers += 1
                    corr = True
                else:
                    corr = False
                rsl = {
                    "ind": task["ind"],
                    "question": task["question"],
                    "user_answer_num": user_answer,
                    "user_answer_text": task["choices"][int(user_answer)-1],
                    "correct_answer_num": task["correct"],
                    "correct_answer_text": task["choices"][int(task["correct"])-1],
                    "correct": corr
                       }
                results.append(rsl)
            else:
                all_valid = False
                results.append(None)

        # Если все ответы корректные, то выводим результаты
        if all_valid:
            total_tasks = len(tasks)
            score_percentage = f"{(correct_answers / total_tasks) * 100:.2f}" if total_tasks else "0"

            context = {
                "results": results,
                "total_tasks": total_tasks,
                "correct_answers": correct_answers,
                "score_percentage": score_percentage,
                "success": True
            }
            return render(request, f"{task_type}_answers.html", context)

        else:
            # Если есть некорректные ответы, выводим ошибку и перенаправляем обратно
            context = {
                "success": False
            }
            return render(request, f"{task_type}_answers.html", context)

    # Если запрос не POST
    return render(request, f"{task_type}_tasks.html")


def add_tasks(request):
    return render(request, "add_tasks.html")


def send_tasks(request):
    if request.method == "POST":
        task_type = request.POST.get('task_type')
        task_question = request.POST.get("task_question")
        answer_1 = request.POST.get("answer_1")
        answer_2 = request.POST.get("answer_2")
        answer_3 = request.POST.get("answer_3")
        answer_4 = request.POST.get("answer_4")
        correct_answer = request.POST.get("correct_answer")

        answers = [answer_1, answer_2, answer_3, answer_4]

        if not task_question or not all([answer_1, answer_2, answer_3, answer_4]) or not correct_answer:
            context = {
                "message": "Ошибка. Не все поля заполнены"
            }
            return render(request, 'send_tasks.html', context)

        try:
            tasks_work.write_task(task_question, answers, correct_answer, task_type)
            # Если задача успешно записана
            context = {
                "message": "Задача успешно добавлена!"
            }
        except Exception as e:
            # Если произошла ошибка при записи
            context = {
                "message": "Ошибка. Не удалось добавить задачу"
            }

        # Рендерим страницу с результатами
        return render(request, 'send_tasks.html', context)

    # Если запрос не POST, перенаправляем на форму добавления задачи
    return add_tasks(request)