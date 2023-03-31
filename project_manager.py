from pydantic import BaseModel
from sql_driver import SQLDriver
from typing import Optional, List


class Project(BaseModel):  # Dataclass
    id: int
    name: str
    begin_date: str
    end_date: str


class ProjectManager:
    def __init__(self, driver: Optional[SQLDriver] = None):
        self.driver = driver or SQLDriver()
        self.define_table()

    def define_table(self):
        """Executes the raw ddl statements to define the database structure."""

        # Projects table
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id integer PRIMARY KEY,
                name text NOT NULL,
                begin_date text NOT NULL,
                end_date text NOT NULL
            );
            """
        )

    def get_projects(self) -> list[Project]:
        """Gets all projects.

        Returns:
            list[Project]: The list of projects.
        """
        sql = "SELECT * FROM projects"
        self.driver.execute_raw(sql)
        tuples = self.driver.cursor.fetchall()
        return [
            Project(
                **{field: row[i] for i, field in enumerate(Project.__fields__.keys())}
            )
            for row in tuples
        ]

    def get_project(self, project_id: int) -> Project:
        """Gets a project.

        Args:
            project_id (int): The id of the project to get.
        """
        sql = "SELECT * FROM projects WHERE id = :project_id"
        self.driver.execute_statement(sql, {"project_id": project_id})
        tuple = self.driver.cursor.fetchall()
        return Project(
            **{field: tuple[0][i] for i, field in enumerate(Project.__fields__.keys())}
        )

    def create_project(self, project: Project):
        """Creates a project.

        Args:
            project (Project): The project to create.
        """
        params = project.dict()
        params.pop("id")
        self.driver.execute_statement(
            """
            INSERT INTO projects (name, begin_date, end_date)
            VALUES (:name, :begin_date, :end_date)
            """,
            params=params,
        )

    def update_project(self, project: Project):
        """Updates a project.

        Args:
            project (Project): The project to update.
        """
        self.driver.execute_statement(
            """
            UPDATE projects
            SET name = :name,
                begin_date = :begin_date,
                end_date = :end_date
            WHERE id = :id
            """,
            project.dict(),
        )

    def delete_project(self, project_id: int):
        """Deletes a project.

        Args:
            project_id (int): The id of the project to delete.
        """
        self.driver.execute_statement(
            """
            DELETE FROM projects
            WHERE id = :project_id
            """,
            {"project_id": project_id},
        )
