from task_manager import TaskManager, Task
from project_manager import ProjectManager, Project

task_manager = TaskManager()
project_manager = ProjectManager()


def main():

    # Create a task
    task = Task(
        id=1,
        name="Task 1",
        priority=1,
        status_id=1,
        project_id=1,
        begin_date="2021-01-01",
        end_date="2021-01-01",
    )

    # Add the task to the task manager
    task_manager.create_task(task)

    # Here we can see that it is added
    tasks = task_manager.get_tasks()

    print(task_manager.get_task(1))

    # Here we update the task
    task.name = "Task 2"
    task_manager.update_task(task)

    # Here we can see that it is updated
    print(task_manager.get_task(1))

    # Here we delete all the tasks
    for task in tasks:
        task_manager.delete_task(task.id)

    # Here we can see that there are no tasks
    print(tasks)

    # Create a project
    project = Project(
        id=1,
        name="Project 1",
        begin_date="2021-01-01",
        end_date="2021-01-01",
    )

    # Add the project to the task manager
    project_manager.create_project(project)

    # Here we can see that it is added
    projects = project_manager.get_projects()

    print(project_manager.get_project(1))

    # Here we update the project
    project.name = "Project 2"
    project_manager.update_project(project)

    # Here we can see that it is updated
    print(project_manager.get_project(1))

    # Here we delete all the projects
    for project in projects:
        project_manager.delete_project(project.id)

    # Here we can see that there are no projects
    print(projects)


if __name__ == "__main__":
    main()