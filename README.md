# SEO_changes_checker
Данный скрипт парсит страницы, указанные в Urls.txt и собирает с них данные:

•	Ответ сервера;

•	Тег title;

•	Метатег description;

•	Тег h1;

•	Тег canonical;

•	Метатег meta name robots;

•	Заголовок ответа сервера x-robots-tag.


При повторном запуске сравнивает данные с предыдущими, и если они изменились, записывает их в файл errors.txt.

Как пользоваться:
Устанавливаем библиотеки:
requests, bs4, lxml

Записываем в Urls.txt список URL для мониторинга.
Запускаем скрипт check.py.

Для настройки автоматического запуска скрипта по расписанию в Windows, создайте bat файл и воспользуйтесь планировщиком заданий - https://remontka.pro/windows-task-scheduler/.
