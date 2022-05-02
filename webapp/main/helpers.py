from webapp import db

def prioritise_tasks(tasks):
    #Takes a timebox of tasks and orders tasks by status, existing priority
    #iterate through the tasks and assign values starting at 0
    to_do_tasks = [task for task in tasks if task.status == 'To Do']
    in_progress_tasks = [task for task in tasks if task.status == 'In Progress']
    done_tasks = [task for task in tasks if task.status == 'Done']
    to_do_tasks.sort(key=lambda x: x.priority)
    in_progress_tasks.sort(key=lambda x: x.priority)
    in_progress_tasks.sort(key=lambda x: x.priority)
    priority = 0
    for task in done_tasks:
        task.priority = priority
        priority += 1
    priority = 0
    for task in in_progress_tasks:
        task.priority = priority
        priority += 1
    priority = 0
    for task in to_do_tasks:
        task.priority = priority
        priority += 1
    tasks.sort(key=lambda x: (x.status, x.priority))
    priority = 0
    for task in tasks:
        task.priority = priority
        priority += 1
    db.session.add_all(tasks)
    db.session.commit()
    return tasks



def insert_task_at_priority(task, priority, tasks):
    for i in tasks:
        if i == task:
            i.priority = priority
        elif i.priority >= priority:
            if i .priority <= task.priority:
                i.priority += 1

    return tasks
