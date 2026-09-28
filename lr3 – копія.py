import uuid
from dataclasses import dataclass
from enum import Enum

# Завдання 1: UML-моделювання (Реалізація переліків та структур для зв'язків)
class Priority(Enum):
    LOW = "Низький"
    MEDIUM = "Середній"
    HIGH = "Високий"

class Status(Enum):
    TODO = "До виконання"
    IN_PROGRESS = "В процесі"
    DONE = "Виконано"

@dataclass
class Employee:
    name: str
    position: str

# Завдання 2: Наслідування (Базовий клас)
class Task:
    def __init__(self, title: str, base_time: int, priority: Priority, assignee: Employee = None):
        self._id = str(uuid.uuid4())[:8]
        self.title = title
        self.base_time = base_time
        self.priority = priority
        self.status = Status.TODO
        self.assignee = assignee

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Назва завдання не може бути порожньою!")
        self._title = value.strip()

    @property
    def base_time(self) -> int:
        return self._base_time

    @base_time.setter
    def base_time(self, value: int):
        if value <= 0:
            raise ValueError("Базовий час має бути більше 0!")
        self._base_time = value

    def calculate_time(self) -> int:
        return self.base_time

    def get_info(self) -> str:
        assignee_name = self.assignee.name if self.assignee else "Не призначено"
        return f"[{self._id}] {self.title} | {self.priority.value} | Виконавець: {assignee_name} | Час: {self.calculate_time()} год."

# Завдання 2 та 3: Наслідування та Поліморфізм (Класи-нащадки)
class DevelopmentTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, assignee: Employee, language: str):
        super().__init__(title, base_time, priority, assignee)
        self.language = language

    def get_info(self) -> str:
        return super().get_info() + f" | Мова: {self.language}"

class BugTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, assignee: Employee, severity: int):
        # Завдання 5: Архітектурний краш-тест
        if severity < 1:
            raise ValueError("Рівень критичності багу не може бути меншим за 1!")
        super().__init__(title, base_time, priority, assignee)
        self.severity = severity

    def calculate_time(self) -> int:
        return self.base_time * self.severity

    def get_info(self) -> str:
        return super().get_info() + f" | Баг (Критичність x{self.severity})"

class TestingTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, assignee: Employee, setup_time: int):
        super().__init__(title, base_time, priority, assignee)
        self.setup_time = setup_time

    def calculate_time(self) -> int:
        return self.base_time + self.setup_time

    def get_info(self) -> str:
        return super().get_info() + f" | Тестування (+{self.setup_time} год. налаштування)"

# Завдання 4: Композиція (Клас-менеджер)
class ProjectManager:
    def __init__(self):
        self._tasks = []

    def add_task(self, task: Task):
        self._tasks.append(task)
        print(f"Додано до проєкту: {task.title}")

    def show_all(self):
        print("\nВсі завдання проєкту:")
        for t in self._tasks:
            print(t.get_info())

# Блок демонстрації
if __name__ == "__main__":
    manager = ProjectManager()
    emp1 = Employee("Іван", "Backend Dev")
    emp2 = Employee("Олена", "QA Engineer")
    
    try:
        t1 = DevelopmentTask("Створити API авторизації", 10, Priority.HIGH, emp1, "Python")
        t2 = TestingTask("Інтеграційне тестування API", 4, Priority.MEDIUM, emp2, 2)
        t3 = BugTask("Помилка 500 при логіні", 3, Priority.HIGH, emp1, 3)

        manager.add_task(t1)
        manager.add_task(t2)
        manager.add_task(t3)

        manager.show_all()

        print("\n[Краш-тест] Спроба створити баг з нульовою критичністю...")
        t4 = BugTask("Мінорний візуальний баг", 2, Priority.LOW, emp1, 0)
        
    except ValueError as e:
        print(f"[ValueError перехоплено]: {e}")
    except Exception as e:
        print(f"[Помилка]: {e}")