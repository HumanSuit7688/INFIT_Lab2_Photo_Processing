from datetime import datetime
from pathlib import Path

from PIL import Image

from image_filters import match_colors, median_filter


MEDIA_DIR = Path(__file__).resolve().parent / "Lab2_Media"
INPUT_DIR = MEDIA_DIR / "data" / "input"
REFERENCE_PATH = MEDIA_DIR / "data" / "reference.jpg"
RESULT_PATH = MEDIA_DIR / "data" / "output" / "result.jpg"
HISTORY_PATH = MEDIA_DIR / "logs" / "history.txt"
FILTER_NAMES = "Медианный фильтр, цветокоррекция по шаблону"


def load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return image.convert("RGB")


def append_history(filename: str, status: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Файл: {filename} | Фильтр: {FILTER_NAMES} | Статус: {status}\n"
    try:
        with HISTORY_PATH.open("a", encoding="UTF-8") as history:
            history.write(entry)
    except OSError as error:
        print(f"Ошибка записи в журнал: {error}")


def main() -> None:
    filename = input("Введите имя изображения: ").strip()
    if not filename or filename in {".", ".."} or any(char in filename for char in "/\\:"):
        print("Ошибка: Введите имя файла из папки data/input")
        return

    try:
        source = load_rgb(INPUT_DIR / filename)
        reference = load_rgb(REFERENCE_PATH)
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        return
    except PermissionError as error:
        blocked_file = Path(error.filename).name if error.filename else filename
        print(f"Ошибка: Нет прав на чтение файла {blocked_file}. Обратитесь к администратору")
        append_history(filename, "Ошибка доступа")
        return
    except OSError as error:
        print(f"Ошибка чтения изображения: {error}")
        return

    filtered = median_filter(source)
    result = match_colors(filtered, reference)
    try:
        result.save(RESULT_PATH)
    except OSError as error:
        print(f"Ошибка сохранения результата: {error}")
        return

    append_history(filename, "Успешно")
    print(f"Результат сохранён: {RESULT_PATH}")


if __name__ == "__main__":
    main()
