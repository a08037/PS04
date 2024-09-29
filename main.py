from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def search_wikipedia(query):
    # Инициализируем браузер
    browser = webdriver.Chrome()

    # Переходим на главную страницу Википедии с запросом
    base_url = "https://ru.wikipedia.org/wiki/"
    search_url = f"{base_url}{query}"
    browser.get(search_url)

    time.sleep(3)  # Подождем, пока страница загрузится

    return browser


def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")

    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:")
        print(paragraph.text)
        if input(
                "\nНажмите Enter, чтобы перейти к следующему параграфу или введите 'stop' для выхода: ").lower() == 'stop':
            break


def list_related_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, "a[href^='/wiki/']")

    print("\nСвязанные статьи:")
    related_links = {}
    for i, link in enumerate(links[:10]):
        link_text = link.text
        href = link.get_attribute('href')
        if link_text:  # Не выводим пустые ссылки
            related_links[i + 1] = href
            print(f"{i + 1}: {link_text}")

    return related_links


def main():
    query = input("Введите запрос для поиска на Википедии: ")
    browser = search_wikipedia(query)

    while True:
        print("\nВыберите действие:")
        print("1: Листать параграфы текущей статьи")
        print("2: Перейти на одну из связанных страниц")
        print("3: Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == '1':
            list_paragraphs(browser)
        elif choice == '2':
            related_links = list_related_links(browser)
            if related_links:
                selected = int(input("\nВведите номер статьи для перехода: "))
                if selected in related_links:
                    browser.get(related_links[selected])
                    time.sleep(3)
                else:
                    print("Неправильный выбор. Попробуйте снова.")
            else:
                print("Нет связанных страниц.")
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    browser.quit()


if __name__ == "__main__":
    main()
