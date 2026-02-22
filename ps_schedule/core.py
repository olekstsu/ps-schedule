import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .models import ScheduleParameters, ScheduleTable, Lesson

class Schedule:
    """Клас розкладу з ПС-Розклад.
    
    Args:
        domain (str): Домен ПС-Деканат (наприклад "https://dekanat.nung.edu.ua/", посилання може відрізнятись для вашого навчального закладу).
        params (ScheduleParameters): Параметри для отримання розкладу.
    """
    def __init__(self, domain: str, params: ScheduleParameters):
        self._url = f"{domain}/cgi-bin/timetable.cgi"

        response = requests.post(self._url, data=params.get_dict())
        response.encoding = "windows-1251"

        self.schedule = self.__parse(response.text)

    def get(self) -> list[ScheduleTable]:
        """Повертає розклад у вигляді списку об'єктів ScheduleTable."""
        return self.schedule

    def __parse(self, html: str) -> list[ScheduleTable]:
        """Парсинг розкладу з ПС-Розклад."""
        bs = BeautifulSoup(html, "html5lib")
        tables = bs.find_all("table", class_="table")
        schedule = list()

        for table in tables:
            _date = datetime.strptime(table.find_previous("h4").contents[0].text.strip(), "%d.%m.%Y").date()
            lessons = list()
            
            for row in table.find_all("tr"):
                number, time, description = row.find_all("td")

                # Номер пари
                f_number = int(number.text.strip())
                # Початок та кінець пари
                f_stime, f_etime = [datetime.strptime(t.strip(), "%H:%M").time() for t in time.stripped_strings]
                # Опис (список строк у колонці)
                f_description = list(description.stripped_strings)
                # Всі посилання з строки
                f_links = [a.get("href") for a in description.find_all("a") if a.get("href")]

                lesson = Lesson(number=f_number, start_time=f_stime, end_time=f_etime, description=f_description, links=f_links)
                lessons.append(lesson)

            day_schedule = ScheduleTable(date=_date, lessons=lessons)
            schedule.append(day_schedule)
        return schedule


    