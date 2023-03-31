from pydantic import BaseModel
from sql_driver import SQLDriver
from typing import Optional


class Task(BaseModel):  # Dataclass
    id: int
    name: str
    priority: int
    status_id: int
    project_id: int
    begin_date: str
    end_date: str


class Project(BaseModel):  # Dataclass
    id: int
    name: str
    begin_date: str
    end_date: str


class TaskManager:
    driver: SQLDriver

    def __init__(self, driver: Optional[SQLDriver] = None):
        self.driver = driver or SQLDriver()
        self.define_table()

    def define_table(self):
        """Executes the raw ddl statements to define the database structure."""

        # Tasks table
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id integer PRIMARY KEY,
                name text NOT NULL,
                priority integer,
                status_id integer NOT NULL,
                project_id integer NOT NULL,
                begin_date text NOT NULL,
                end_date text NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );
            """
        )

    def get_tasks(self) -> list[Task]:
        """Gets all tasks.

        Returns:
            list[Task]: The list of tasks.
        """
        sql = "SELECT * FROM tasks"
        self.driver.execute_raw(sql)
        tuples = self.driver.cursor.fetchall()
        return [
            Task(**{field: row[i] for i, field in enumerate(Task.__fields__.keys())})
            for row in tuples
        ]

    def get_task(self, task_id: int) -> Task:
        """Gets a task.

        Args:
            task_id (int): The id of the task to get.

        Returns:
            Task: The task.
        """
        sql = "SELECT * FROM tasks WHERE id = :task_id"
        self.driver.execute_statement(sql, {"task_id": task_id})
        tuple = self.driver.cursor.fetchall()
        return Task(
            **{field: tuple[0][i] for i, field in enumerate(Task.__fields__.keys())}
        )

    def create_task(self, task: Task):
        """Creates a task.

        Args:
            task (Task): The task to create.
        """
        params = task.dict()
        params.pop("id")
        self.driver.execute_statement(
            """
            INSERT INTO tasks (name, priority, status_id, project_id, begin_date, end_date)
            VALUES (:name, :priority, :status_id, :project_id, :begin_date, :end_date)
            """,
            params=params,
        )

    def update_task(self, task: Task):
        """Updates a task.

        Args:
            task (Task): The task to update.
        """
        self.driver.execute_statement(
            """
            UPDATE tasks
            SET name = :name,
                priority = :priority,
                status_id = :status_id,
                project_id = :project_id,
                begin_date = :begin_date,
                end_date = :end_date
            WHERE id = :id
            """,
            task.dict(),
        )

    def delete_task(self, task_id: int):
        """Deletes a task.

        Args:
            task_id (int): The id of the task to delete.
        """
        self.driver.execute_statement(
            """
            DELETE FROM tasks
            WHERE id = :task_id
            """,
            {"task_id": task_id},
        )
