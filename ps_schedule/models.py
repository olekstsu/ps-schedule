from datetime import date, time

class ScheduleParameters:
    """Параметри для класу Schedule. Заповнюйте ці параметри так само як би ви заповнювали форму у ПС-Розклад.\n
    
    Example:
        ```python
        ScheduleParameters(group="ІП-24-1К") # Розклад для групи ІП-24-1К
        ScheduleParameters(teacher="Іванов Іван Іванович") # Розклад для викладача
        ```
    
    Args:
        faculty (int): Ідентифікатор факультету (у ПС-Розклад, ідентифікатор представляє собою порядковий номер у dropdown "Оберіть факультет", записується як "1001 (1), 1011 (11) і т.д.).
        teacher (str): ПІБ викладача. (Пишеться прямо рядком як у ПС-Розклад вибираєте викладача,).
        course (int): Номер курсу. (Необов'язковий параметр, якщо вказано групу).
        group (str): Назва групи. (Шифр групи відповідно до вашого навчального закладу)
        sdate (date): Дата початку розкладу. (Необов'язковий параметр, розклад за замовчуванням за поточний тиждень).
        edate (date): Дата кінця розкладу. (Необов'язковий параметр, розклад за замовчуванням за поточний тиждень).
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
    """Клас для збереження інформації про пару. Містить номер пари, час початку та кінця, а також опис пари."""
    def __init__(self, number: int, start_time: time, end_time: time, description: list[str], links: list[str] = []):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.links = links

    def get_dict(self) -> dict:
        return {
            "number": self.number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description
        }
        
class ScheduleTable:
    """Клас для збереження розкладу на певний день. Містить дату та список пар на цей день."""
    def __init__(self, date: date, lessons: list[Lesson]):
        self.date = date
        self.lessons = lessons

    def get_dict(self) -> dict:
        return {
            "date": self.date,
            "lessons": [lesson.get_dict() for lesson in self.lessons]
        }

