import requests
from bs4 import BeautifulSoup

HOST = "https://povar.ru"
URL = HOST
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}


def get_html(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Ошибка при загрузке страницы: {e}")
        return None


def parse_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    menu = soup.find("div", id="floatingMenu")
    if not menu:
        print("❌ Блок floatingMenu не найден!")
        return []

    result = []
    children = [el for el in menu.children if getattr(el, "name", None)]

    i = 0
    while i < len(children):
        elem = children[i]

        if elem.name == "a" and "fmHead" in elem.get("class", []):
            category_name = elem.get_text(strip=True)
            category_link = HOST + elem.get("href")

            subcategories = []
            # искать следующий div с подкатегориями
            j = i + 1
            while j < len(children):
                sub_block = children[j]
                if sub_block.name == "div" and sub_block.find("a", class_="fmItem"):
                    for sub in sub_block.find_all("a", class_="fmItem"):
                        sub_name = sub.get_text(strip=True)
                        sub_link = HOST + sub.get("href")
                        subcategories.append({"name": sub_name, "link": sub_link})
                    break
                elif sub_block.name == "a" and "fmHead" in sub_block.get("class", []):
                    break  # следующий раздел, выходим
                j += 1

            result.append({
                "category": category_name,
                "link": category_link,
                "subcategories": subcategories
            })
            i = j  # перескочить к следующей категории
        else:
            i += 1

    return result


def main():
    html = get_html(URL)
    if html:
        categories = parse_categories(html)
        for cat in categories:
            print(f"\n📂 {cat['category']} — {cat['link']}")
            for sub in cat['subcategories']:
                print(f"   └ 📄 {sub['name']} — {sub['link']}")
    else:
        print("❌ Не удалось загрузить HTML.")


if __name__ == "__main__":
    main()
