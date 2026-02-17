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
        schedule = []

        for table in tables:
            _date = datetime.strptime(table.find_previous("h4").contents[0].text.strip(), "%d.%m.%Y").date()
            lessons = list()
            
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                number = int(cols[0].text.strip())
                stime, etime = [datetime.strptime(t.strip(), "%H:%M").time() for t in cols[1].stripped_strings]
                description = cols[2].text.strip()

                lesson = Lesson(number=number, start_time=stime, end_time=etime, description=description)
                lessons.append(lesson)

            day_schedule = ScheduleTable(date=_date, lessons=lessons)
            schedule.append(day_schedule)
        return schedule


    