import urllib.request
from bs4 import BeautifulSoup
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = 'https://hotline.ua/sport/elektrovelosipedy/'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_page_count(html):
    soup = BeautifulSoup(html, features="html.parser")
    pagination = soup.find("div", class_="pages-list cell-sm")
    return int(pagination.find_all("a")[-1].text)


def save_to_csv(items, path):
    with open(path, "w") as csvfile:
        writter = csv.writer(csvfile)
        writter.writerow(("Title", "Price"))

        for item in items:
            writter.writerow((item["title"]+", "+item["price"]).split(","))


def parse(html):
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find('ul', class_="products-list cell-list")
    try:
        rows = table.find_all('li', class_="product-item")

        item_list = []

        for row in rows:
            try:
                item_list.append({
                        "title": row.find("div", class_="item-info").p.a.text.strip(),
                        "price": row.find(
                            "div", class_="item-price stick-bottom").find(
                            "span", class_="value").text.strip().replace(u'\xa0', u''),

                    })
            except AttributeError:
                pass

        return item_list
    except:
        print("**"*40 + "\n" + "**"*40)


def main():
    base_page = parse(get_html(BASE_URL))

    page_count = get_page_count(get_html(BASE_URL))
    print("Всего найдено страниц: {}".format(page_count))

    total_item_list = []
    total_item_list += base_page
    for page in range(1, page_count):
        print("Парсинг {}%".format(int(page / page_count * 100)))
        print("Страница {}".format(page))
        total_item_list.extend(parse(get_html(BASE_URL + "?p={}".format(page))))

    save_to_csv(total_item_list, "items.csv")


if __name__ == "__main__":
    main()
