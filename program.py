from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# Глобальные переменные для хранения данных пользователя
user_data = {}

# Функция для отправки сообщений в Telegram
def send_log(message):
    if 'chat_id' in user_data:
        bot.sendMessage(user_data['chat_id'], message)

# Функция для логирования и отправки сообщений
def log_and_print(message):
    print(message)
    send_log(message)

def login(username, password, follow_count, likes_min, likes_max, location_url):
    # Указываем путь к chromedriver
    service = Service(r"C:\Users\Вероника\Desktop\secret\instagram_bot-master\chromedriver\chromedriver.exe")

    # Инициализация браузера Chrome
    browser = webdriver.Chrome(service=service)
    log_and_print("Инициализация браузера Chrome")

    try:
        # Шаг 1: Открываем Instagram
        log_and_print("Открываем Instagram...")
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        # Шаг 2: Вводим логин
        log_and_print("Вводим логин...")
        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(2)

        # Шаг 3: Вводим пароль
        log_and_print("Вводим пароль...")
        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)

        # Шаг 4: Отправляем форму
        log_and_print("Отправляем форму логина...")
        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

        for _ in range(follow_count):
            # Шаг 5: Открываем указанную ссылку
            log_and_print("Открываем указанную ссылку...")
            browser.get(location_url)
            time.sleep(20)  # Задержка 20 секунд, чтобы вся страница загрузилась

            # Шаг 6: Получаем все посты на странице
            log_and_print("Получаем все посты на странице...")
            posts = []
            attempts = 0

            while attempts < 3:
                try:
                    posts = WebDriverWait(browser, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//article//a'))
                    )
                    if posts:
                        break
                except Exception as e:
                    log_and_print(f"Попытка {attempts+1} не удалась: {e}")
                    log_and_print("Перезагружаем страницу...")
                    browser.refresh()
                    time.sleep(10)  # Задержка после перезагрузки страницы
                    attempts += 1

            if len(posts) >= 13:
                # Кликаем на 13-й пост
                log_and_print("Кликаем на 13-й пост...")
                posts[12].click()
                time.sleep(10)  # Дополнительная задержка 10 секунд после клика

                # Шаг 7: Используем JavaScript для извлечения никнейма пользователя
                log_and_print("Ищу никнейм пользователя...")
                try:
                    user_name_element = browser.find_element(By.CSS_SELECTOR, 'header a')
                    user_name = user_name_element.get_attribute('href').split('/')[-2]
                    profile_url = f"https://www.instagram.com/{user_name}/"

                    # Проверка URL профиля
                    if profile_url and user_name:
                        log_and_print(f"Открываем профиль пользователя по ссылке: {profile_url}")
                        browser.get(profile_url)
                        time.sleep(12)  # Задержка для загрузки страницы профиля

                        # Шаг 8: Получаем первый пост на странице профиля с использованием JavaScript
                        log_and_print("Получаем первый пост на странице профиля с использованием JavaScript...")
                        script = """
                        var classSelectors = '.x1i10hfl, .xjbqb8w, .x1ejq31n, .xd10rxx, .x1sy0etr, .x17r0tee, .x972fbf, .xcfux6l, .x1qhh985, .xm0m39n, .x9f619, .x1ypdohk, .xt0psk2, .xe8uvvx, .xdj266r, .x11i5rnm, .xat24cr, .x1mh8g0r, .xexx8yu, .x4uap5, .x18d9i69, .xkhd6sd, .x16tdsg8, .x1hl2dhg, .xggy1nq, .x1a2a7pz, ._a6hd';
                        var elements = document.querySelectorAll(classSelectors);
                        if (elements.length === 0) {
                            return 'Нет элементов с указанными классами.';
                        }
                        for (var i = 0; i < elements.length; i++) {
                            var el = elements[i];
                            var link = el.querySelector('a[href^="/p/"]');
                            if (link) {
                                return link.getAttribute('href');
                            }
                        }
                        return 'Ссылка на пост не найдена.';
                        """
                        first_post_href = browser.execute_script(script)
                        if first_post_href.startswith('/p/'):
                            first_post_url = f"https://www.instagram.com{first_post_href}"
                            log_and_print(f"Открываем первый пост: {first_post_url}")
                            post_element = browser.find_element(By.XPATH, f"//a[@href='{first_post_href}']")
                            browser.execute_script("arguments[0].click();", post_element)
                            time.sleep(10)  # Задержка для загрузки поста

                        # Определяем случайное количество лайков от likes_min до likes_max
                        likes = random.randint(likes_min, likes_max)

                        for _ in range(likes):
                            try:
                                # Заменяем действие на выполнение JavaScript для клика по кнопке лайка
                                log_and_print("Нажимаем на кнопку 'Нравится' с помощью JavaScript...")
                                browser.execute_script(
                                    'document.querySelector(\'svg[aria-label="Нравится"]\').parentElement.click();'
                                )
                                time.sleep(2)  # Задержка между лайками

                                # Переход к следующему посту
                                next_button = WebDriverWait(browser, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, '._abl-'))
                                )
                                browser.execute_script("arguments[0].click();", next_button)
                                time.sleep(2)  # Задержка перед следующим постом

                            except Exception as e:
                                log_and_print(f"Ошибка при попытке поставить лайк: {e}")

                        # Шаг 11: Переходим по ссылке профиля и нажимаем "Подписаться"
                        log_and_print("Переходим по ссылке профиля и ищем кнопку 'Подписаться'...")
                        browser.get(profile_url)
                        time.sleep(12)  # Задержка для загрузки страницы профиля

                        try:
                            # Попробуем найти кнопку по CSS-селектору
                            follow_button = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button'))
                            )
                            follow_button_text = follow_button.text.lower()

                            if 'follow' in follow_button_text or 'подписаться' in follow_button_text:
                                log_and_print("Нажимаем на кнопку 'Подписаться'...")
                                follow_button.click()
                            else:
                                log_and_print("Кнопка 'Подписаться' не найдена.")
                        except Exception as e:
                            log_and_print(f"Не удалось найти кнопку 'Подписаться': {e}")

                    else:
                        log_and_print(f"Получен некорректный URL профиля: {profile_url}")
                except Exception as e:
                    log_and_print(f"Не удалось найти никнейм пользователя: {e}")

            else:
                log_and_print("Недостаточно постов на странице.")
                break

            # Шаг 12: Включаем режим ожидания на 10 секунд
            log_and_print("Режим ожидания на 10 секунд...")
            time.sleep(10)

    except Exception as ex:
        log_and_print(f"Ошибка: {ex}")
    finally:
        browser.quit()
        log_and_print("Закрытие браузера.")

# Функции для Telegram-бота
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    # Убедитесь, что данные пользователя для данного чата существуют
    if chat_id not in user_data:
        user_data[chat_id] = {'state': None}

    state = user_data[chat_id].get('state')

    if command == '/start':
        bot.sendMessage(chat_id, "Добро пожаловать! Используйте /add_account для добавления аккаунта или /manage_accounts для управления аккаунтами.")
    elif command == '/add_account':
        bot.sendMessage(chat_id, "Введите логин:")
        user_data[chat_id]['state'] = 'get_login'
    elif state == 'get_login':
        user_data[chat_id]['username'] = command
        bot.sendMessage(chat_id, "Введите пароль:")
        user_data[chat_id]['state'] = 'get_password'
    elif state == 'get_password':
        user_data[chat_id]['password'] = command
        bot.sendMessage(chat_id, "Введите количество подписок:")
        user_data[chat_id]['state'] = 'get_follow_count'
    elif state == 'get_follow_count':
        user_data[chat_id]['follow_count'] = int(command)
        bot.sendMessage(chat_id, "Введите минимальное количество лайков:")
        user_data[chat_id]['state'] = 'get_likes_min'
    elif state == 'get_likes_min':
        user_data[chat_id]['likes_min'] = int(command)
        bot.sendMessage(chat_id, "Введите максимальное количество лайков:")
        user_data[chat_id]['state'] = 'get_likes_max'
    elif state == 'get_likes_max':
        user_data[chat_id]['likes_max'] = int(command)
        bot.sendMessage(chat_id, "Выберите локацию:\nЛондон /london\nДобавить новую /new_location")
        user_data[chat_id]['state'] = 'get_location'
    elif state == 'get_location':
        if command == '/london':
            user_data[chat_id]['location_url'] = 'https://www.instagram.com/explore/locations/217273440/london/'
            log_and_print("Локация установлена: Лондон")
            log_and_print("Запускаем процесс...")
            login(
                user_data[chat_id]['username'],
                user_data[chat_id]['password'],
                user_data[chat_id]['follow_count'],
                user_data[chat_id]['likes_min'],
                user_data[chat_id]['likes_max'],
                user_data[chat_id]['location_url']
            )
            bot.sendMessage(chat_id, "Процесс завершен.")
            user_data[chat_id].clear()  # Очистить данные пользователя после завершения
        elif command == '/new_location':
            bot.sendMessage(chat_id, "Введите URL новой локации:")
            user_data[chat_id]['state'] = 'get_new_location'
        else:
            bot.sendMessage(chat_id, "Некорректная команда. Выберите локацию:\nЛондон /london\nДобавить новую /new_location")
    elif state == 'get_new_location':
        user_data[chat_id]['location_url'] = command
        log_and_print("Локация установлена: " + user_data[chat_id]['location_url'])
        log_and_print("Запускаем процесс...")
        login(
            user_data[chat_id]['username'],
            user_data[chat_id]['password'],
            user_data[chat_id]['follow_count'],
            user_data[chat_id]['likes_min'],
            user_data[chat_id]['likes_max'],
            user_data[chat_id]['location_url']
        )
        bot.sendMessage(chat_id, "Процесс завершен.")
        user_data[chat_id].clear()  # Очистить данные пользователя после завершения


# Инициализация Telegram-бота
bot = telepot.Bot('7422029006:AAFXOYAo8zaGszr1yVkfNp3jWQPGvUUf-KA')
MessageLoop(bot, handle).run_as_thread()
log_and_print("Бот запущен. Ожидание сообщений...")

# Запуск бота
while True:
    time.sleep(10)
