import requests
from bs4 import BeautifulSoup
import csv

HOST = "https://povar.ru"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


# def get_content(html):
#     soup = BeautifulSoup(html, "html.parser")
#     container = soup.find("div", class_="recipe_list")
#     if not container:
#         print("❌ Контейнер recipe_list не найден!")
#         return []
#
#     items = container.find_all("div", class_="recipe")
#     recipes = []
#
#     for item in items:
#         title_tag = item.find("a", class_="listRecipieTitle")
#         img_tag = item.find("img")
#         if not (title_tag and img_tag):
#             continue
#
#         title = title_tag.get_text(strip=True)
#         link = HOST + title_tag.get("href")
#         image = img_tag.get("src")
#
#         recipes.append({
#             "title": title,
#             "link": link,
#             "image": image
#         })
#
#     return recipes

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="recipe_list")
    if not container:
        print("❌ Контейнер recipe_list не найден!")
        return []

    items = container.find_all("div", class_="recipe")
    recipes = []

    for item in items:
        title_tag = item.find("a", class_="listRecipieTitle")
        thumb_span = item.find("span", class_="a thumb hashString")
        img_tag = thumb_span.find("img") if thumb_span else None

        if not title_tag or not img_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = HOST + title_tag.get("href")
        image = img_tag.get("src")

        recipes.append({
            "title": title,
            "link": link,
            "image": image
        })

    return recipes


def save_to_csv(items, filename):
    with open(filename, "w", newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Название рецепта", "Ссылка", "Изображение"])
        for item in items:
            writer.writerow([item["title"], item["link"], item["image"]])


def parser():
    category = input("Введите категорию (например, salaty, supy, zakuski): ").strip()
    pages = int(input("Сколько страниц пропарсить? ").strip())
    url_template = f"{HOST}/list/{category}/"

    all_recipes = []

    for page in range(1, pages + 1):
        url = url_template if page == 1 else f"{url_template}page{page}/"
        print(f"Парсинг: {url}")
        html = get_html(url)
        if html.status_code == 200:
            recipes = get_content(html.text)
            if not recipes:
                print("Нет рецептов на этой странице. Останов.")
                break
            all_recipes.extend(recipes)
        else:
            print(f"Ошибка при запросе страницы {page}")
            break

    if all_recipes:
        filename = f"{category}_recipes.csv"
        save_to_csv(all_recipes, filename)
        print(f"✅ Сохранено {len(all_recipes)} рецептов в файл: {filename}")
    else:
        print("❌ Ничего не спарсилось.")


if __name__ == "__main__":
    parser()
