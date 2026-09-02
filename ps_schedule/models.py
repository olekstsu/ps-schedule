import datetime
from datetime import date, time

from bs4 import Tag

class ScheduleParameters:
    """Параметри для класу `Schedule`. Заповнюйте ці параметри так само як би ви заповнювали форму у ПС-Розклад.
    
    Example:
        ```python
        ScheduleParameters(group="ІП-24-1К") # Розклад для групи ІП-24-1К
        ScheduleParameters(teacher="Іванов Іван Іванович") # Розклад для викладача
        ```
    
    Args:
        `faculty` (`int`): Ідентифікатор факультету (у ПС-Розклад, ідентифікатор можна дізнатись через код елемента випадаючого списку для вибору факультету). Можна отримати за допомогою функції `get_faculty_id()`.
        `teacher` (`str`): ПІБ викладача. (Пишеться прямо рядком як у ПС-Розклад, коли обираєте викладача).
        `course` (`int`): Номер курсу. (Необов'язковий параметр, якщо вказано групу).
        `group` (`str`): Назва групи. (Шифр групи відповідно до вашого навчального закладу)
        `sdate` (`date`): Дата початку розкладу. (Необов'язковий параметр, розклад за замовчуванням за поточний тиждень).
        `edate` (`date`): Дата кінця розкладу. (Необов'язковий параметр, розклад за замовчуванням за поточний тиждень).
    """
    def __init__(self, faculty: int = 0, teacher: str = None, course: int = 0, group: str = None, sdate: date = None, edate: date = None):
        self.params = {
            "faculty": faculty,
            "teacher": teacher.encode("windows-1251") if teacher else None,
            "course": course,
            "group": group.encode("windows-1251") if group else None,
            "sdate": sdate.strftime("%d.%m.%Y") if sdate else None,
            "edate": edate.strftime("%d.%m.%Y") if edate else None,
            "n": 700
        }

    def get_dict(self) -> dict:
        return self.params
    
class Lesson:
    """Представляє собою рядок з таблиці розкладу (`ScheduleTable`).

    Attributes:
        `number` (`int`): Порядковий номер пари у таблиці
        `start_time` (`time`): Час початку пари
        `end_time` (`time`): Час закінчення пари
        `description` (`list[str]`): Опис пари. Рядки у списку розбиті згідно з тим як ПС-Розклад переносить їх у рядку таблиці.
        `links` (`list[str]`): Список клікабельних посилань, прикріплених до розкладу.
    """

    number: int
    start_time: time
    end_time: time
    description: list[str]
    links: list[str]

    _raw_description: Tag

    def __init__(self, number: int, start_time: time, end_time: time, description: list[str], links: list[str] = []):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.links = links

    def get_raw_description(self) -> Tag:
        """Повертає об'єкт `bs4.Tag`, який містить HTML-розмітку колонки з описом пари у таблиці розкладу. Можна використовувати для ручного парсингу тегів."""
        return self._raw_description

    def get_dict(self) -> dict:
        return {
            "number": self.number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description
        }
        
class ScheduleTable:
    """Клас для збереження розкладу на певний день. Містить дату та список пар на цей день.

    Attributes:
        `date` (`date`): Дата до якої відноситься таблиця
        `lessons` (`list[Lesson]`): Список пар на цей день
    """

    date: datetime.date
    lessons: list[Lesson]

    def __init__(self, date: datetime.date, lessons: list[Lesson]):
        self.date = date
        self.lessons = lessons

    def get_dict(self) -> dict:
        return {
            "date": self.date,
            "lessons": [lesson.get_dict() for lesson in self.lessons]
        }

class SearchType:
    """Перелік типів для пошуку.

    Attributes:
        `TEACHER`: Шукати викладачів
        `GROUP`: Шукати групи
    """
    TEACHER = 141
    GROUP = 142

class SearchParameters:
    """Параметри для класу `Search`.

    Args:
        `type` (`SearchType`): Тип для пошуку.
        `query` (`str`): Запит за яким робити пошук.
        `faculty` (`int`): Ідентифікатор факультету. Можна отримати через функцію `get_faculty_id()`.
        `course` (`int`): Номер курсу. Необов'язковий параметр, якщо тип пошуку `SearchType.TEACHER`.
    """

    type: SearchType
    query: str
    faculty: int
    course: int

    def __init__(self, type: SearchType, query: str, faculty: int = 0, course: int = 0):
        self.type = type
        self.query = query
        self.faculty = faculty
        self.course = course

    def get_dict(self) -> dict:
        return {
            "lev": self.type,
            "faculty": self.faculty,
            "course": self.course,
            "query": self.query,
            "n": 701
        }