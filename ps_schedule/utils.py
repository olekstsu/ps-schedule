import requests
from bs4 import BeautifulSoup

def get_faculty_id(domain: str, faculty_name: str) -> int | None:
    """Функція для отримання ідентифікатора факультету за його назвою. Ідентифікатор потрібен для заповнення параметрів розкладу та пошуку.

    Args:
        `domain` (`str`): Домен ПС-Деканат (наприклад "https://dekanat.nung.edu.ua/", посилання може відрізнятись для вашого навчального закладу).
        `faculty_name` (`str`): Назва факультету, для якого потрібно отримати ідентифікатор.
    
    Returns:
        `int` | `None`: Повертає ідентифікатор факультету або `None` якщо факультет не знайдено.
    """
    url = f"{domain}/cgi-bin/timetable.cgi"

    response = requests.post(url)
    response.encoding = "windows-1251"

    bs = BeautifulSoup(response.text, "html5lib")
    select = bs.find("select", id="faculty")
    options = select.find_all("option")

    return next((int(op.get("value")) for op in options if op.getText() == faculty_name), None)


def get_faculties(domain: str) -> dict[int, str]:
    """Функція для отримання словника факультетів у ПС-Деканат.

    Args:
        `domain` (`str`): Домен ПС-Деканат (наприклад "https://dekanat.nung.edu.ua/", посилання може відрізнятись для вашого навчального закладу).
    
    Returns:
        `dict[int, str]`: Словник факультетів у ПС-Деканат. Ключами є ідентифікатори факультетів, а значеннями - їх назви.
    """
    url = f"{domain}/cgi-bin/timetable.cgi"

    response = requests.post(url)
    response.encoding = "windows-1251"

    bs = BeautifulSoup(response.text, "html5lib")
    select = bs.find("select", id="faculty")
    options = select.find_all("option")

    return {int(op.get("value")): op.getText() for op in options if op.get("value") != "0"}