import requests
from bs4 import BeautifulSoup

def get_faculty_id(domain: str, faculty_name: str) -> int:
    url = f"{domain}/cgi-bin/timetable.cgi"

    response = requests.post(url)
    response.encoding = "windows-1251"

    bs = BeautifulSoup(response.text, "html5lib")
    select = bs.find("select", id="faculty")
    options = select.find_all("option")

    return next((op.get("value") for op in options if op.getText() == faculty_name), None)
