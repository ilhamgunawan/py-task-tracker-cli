from typing import Optional
import json
import pathlib

class TaskTracker:
    tasks: list[dict] = []
    __last_created_id: int = 0
    __json_path = "tasks.json"

    def __init__(self) -> None:
        if self.__is_json_exist():
            self.__restore_from_json()
        else:
            self.__save_to_json()

    def create_task(self, description: str) -> None:
        new_task = {
            "id": self.__last_created_id + 1,
            "description": description,
            "status": "todo"
        }
        self.tasks.append(new_task)
        self.__last_created_id = self.__last_created_id + 1
        self.__save_to_json()
        print(f"Task added successfully (ID: {new_task["id"]}).")

    def update_task(self, __id: int, __description: Optional[str], __status: Optional[str]) -> None:
        index = 0
        while index < len(self.tasks):
            task = self.tasks[index]
            if task["id"] == __id:
                if __description is not None:
                    task["description"] = __description
                if __status is not None:
                    task["status"] = __status
                self.__save_to_json()
                return
            else:
                index = index + 1
        self.__task_not_found_notification(__id, "Update failed.")

    def delete_task(self, __id: int) -> None:
        index = 0
        while index < len(self.tasks):
            if self.tasks[index]["id"] == __id:
                self.tasks.pop(index)
                self.__save_to_json()
                return
            else:
                index = index + 1
        self.__task_not_found_notification(__id, "Delete failed.")

    def list_all_tasks(self) -> None:
        print("ID; Description; Status")
        if len(self.tasks) == 0:
            print("Task list empty.")
        else:
            for task in self.tasks:
                self.__print_task(task)

    def list_by_status(self, __status: str) -> None:
        print("ID; Description; Status")
        count = 0
        for task in self.tasks:
            if task["status"] == __status:
                self.__print_task(task)
                count = count + 1
        if count == 0:
            print(f"There is no {__status} task found.")

    def __is_json_exist(self) -> bool :
        return pathlib.Path(self.__json_path).exists()

    def __save_to_json(self) -> None:
        out_file = open(self.__json_path, 'w')
        out_file.write(json.dumps({
            "tasks": self.tasks,
            "last_created_id": self.__last_created_id
        }, indent=4))

    def __restore_from_json(self):
        file = open(self.__json_path, "r")
        content = json.load(file)
        self.tasks = content["tasks"]
        self.__last_created_id = content["last_created_id"]

    @staticmethod
    def __print_task(__task: dict) -> None:
        print(f"{__task["id"]}; {__task["description"]}; {__task["status"]}")

    @staticmethod
    def __task_not_found_notification(__id: int, __message: Optional[str]) -> None:
        message = f"Task not found (ID: {__id})"
        if __message is not None:
            message = f"{message}: {__message}"
        print(message)