# kanalservis_test_task
Тестовое задание для kanalservis. Ссылка на таблицу: https://docs.google.com/spreadsheets/d/1BkcYdJamiszwryvC_tPxWOesEXu_ieooWoFheiVDp6A/edit#gid=0.<br><br>
**КЛЮЧ ОТ GOOGLE API И ТОКЕН ДЛЯ ТЕЛЕГРАМ БОТА В РЕПОЗИТОРИЙ Я НЕ ЗАГРУЗИЛ, ПОТОМУ ЧТО ЭТО НЕ БЕЗОПАСНО 
(к тому же в тестовом задани об этом ничего не написано)**

## Запуск проекта: конфиг
В корневой директории проекта есть файл config.py. Рассмотрим как получить требуемые для программы токены, ключи и т.д.:
1. **CREDENTIALS_FILE_NAME** - ключ, созданный в Google API. В эту переменную нужно указать название файла ключа.
   > Файл ключа должен находиться в корневой директории проекта. **APIs & Services > Credentials > Выбрать сервисный 
   > аккаунт или создать новый > KEYS > ADD KEY > CREATE NEW KEY > JSON**
2. **SPREADSHEET_ID** - ID spreadsheet'а, который будет редактироваться. 
   > В таблицу с данным ID нужно добавить (с правом на редактирование) созданный в Google API сервисный аккаунт. 
   > Пример ID **1BkcYdJamiszwryvC_tPxWOesEXu_ieooWoFheiVDp6A** в ссылке на таблицу: 
   > docs.google.com/spreadsheets/d/**1BkcYdJamiszwryvC_tPxWOesEXu_ieooWoFheiVDp6A**/edit#gid=0
3. **PG_USER**, **DB_NAME**, **PG_PASSWORD**, **PG_HOST**, **PG_PORT** - данные для подключения к СУБД PostgreSQL.
   > Данный проект создавался с PostgreSQL версии 14.4
4. **PARSING_RANGE** - сколько строк за раз (за один запрос к API) будет парситься с указанного spreadsheet'а.
5. **SHEET_MONITORING_DELAY** - задержка (в секундах) между парсингами spreadsheet'а.
6. **DELIVERY_MONITORING_DELAY**  - задержка (в секундах) между проверками на выполненные заказы для отправки уведомлений в телеграм.
7. **TELEGRAM_API_TOKEN** - токен для телеграм бота, получать в https://t.me/BotFather.


## Запуск проекта: скрипты
1. Убедитесь, что PostgreSQL сервер включён и данные для подключения указаны верно.
2. Исполнить скрипт **main.py**. Это запустит процесс мониторинга таблицы и рассылки уведомлений о выполненных заказах.
3. Исполнить **telegram_bot/bot.py**. Это запустит телеграм бота.
> Также можно отдельно запустить мониторинг таблицы (**monitoring/spreadsheets.py**) и рассылку уведомлений 
> (**monitoring/notifications.py**)
