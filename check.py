import time
import webbrowser
import CheckerFunctions as CF

# Взять урлы из файла urls и проверить каждый. В конце открыть блокнот со списком ошибок если они имеются
if __name__ == '__main__':
    urls = open('urls.txt', 'r')
    changes = []
    bad_responses = []

    for url in urls:
        url = url.strip()
        new_data = CF.get_url_data(url)
        if type(new_data) == dict:
            changes.extend(CF.changes_checker(new_data, url))
        else:
            bad_responses.append(new_data)

        time.sleep(0.2)

    if len(changes) > 0 or len(bad_responses) > 0:
        errors = open('errors.txt', 'w', encoding='utf-8')
        for change in changes:
            errors.write(change + '\n')
        if bad_responses:
            errors.write('Страницы не 200: \n')
            for i in bad_responses:
                errors.write(i + '\n')
        errors.close()
        webbrowser.open("errors.txt")
        print('Есть изменения, смотри errors.txt')
    else:
        print('Проверка закончена. Изменений не обнаружено')
