# TODO: Update the main function to your needs or remove it.
from core import Schedule, ScheduleParameters

def main() -> None:
    s = Schedule(domain="https://dekanat.nung.edu.ua/", params=ScheduleParameters(group="ІП-24-1К"))
    f = open("output.txt", "w", encoding='utf-8')
    lines = list()
    for day in s.get():
        lines.append(f"===| {day.date} |===")
        for lesson in day.lessons:
            text = (
                lesson.description
                .replace("дистанційно", "")
                .replace("*", "")
                .replace("(в)", "")
                .replace("Військова підготовка", "")
                .strip()
            )
            
            # Видаляємо непотрібну інформацію з опису пари. Залишаємо тільки назву предмету.
            patterns = ["(Л)", "(Лаб)", "(Пр)"]
            slice_index = min((text.find(p)+len(p) for p in patterns if text.find(p) != -1), default=-1)
            if slice_index != 1:
                text = text[:slice_index].strip()

            lines.append(f"[{lesson.number}]: {text}")

    lines = [line + "\n" for line in lines]
    f.writelines(lines)
    f.close()

if __name__ == "__main__":
    main()
