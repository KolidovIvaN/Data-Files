import json
from datetime import datetime


# Чтение данных из файла .json
def read_json_file(file_json):
    with open(file_json, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return data


# Чтение данных из файла .txt
def read_txt_file(file_txt):
    results = {}
    with open(file_txt, 'r') as file:
        for line in file:
            line = line.strip().split()
            if len(line) >= 3:
                number = line[0]
                action = line[1]
                time_str = line[2]
                time = datetime.strptime(time_str, '%H:%M:%S,%f')

                if number not in results:
                    results[number] = {'нагрудный номер': number}
                if action == 'start':
                    results[number]['время старта'] = time
                elif action == 'finish':
                    results[number]['время финиша'] = time

    results_data = [data for data in results.values() if 'время старта' in data and 'время финиша' in data]
    return results_data


# Вывод таблицы с данными в консоль; формирование файла .json
def print_results_table(athletes_file, results_file, output_file):
    athletes_data = read_json_file(athletes_file)
    results_data = read_txt_file(results_file)

    results_data.sort(key=lambda x: (x['время финиша'] - x['время старта']))

    print(
        "{:<15} {:<20} {:<15} {:<15} {:<15}".format("Занятое место", "Нагрудный номер", "Имя", "Фамилия", "Результат"))

    # Создание таблицы данных, вывод в консоль; формирование файла .json
    final_results = {}
    for i, result in enumerate(results_data, start=1):
        athlete_info = athletes_data.get(str(result['нагрудный номер']), {})
        time_diff = (result['время финиша'] - result['время старта'])
        seconds = time_diff.total_seconds()
        minutes = seconds // 60
        seconds %= 60
        microseconds = time_diff.microseconds
        time_diff_str = f"{int(minutes):02}:{int(seconds):02},{microseconds:03}"
        print("{:<15} {:<20} {:<15} {:<15} {:<15}".format(i, result['нагрудный номер'], athlete_info.get('Surname', ''),
                                                          athlete_info.get('Name', ''),
                                                          time_diff_str))
        # Формирование файла .json
        final_results[str(i)] = {
            "Нагрудный номер": result['нагрудный номер'],
            "Имя": athlete_info.get('Surname', ''),
            "Фамилия": athlete_info.get('Name', ''),
            "Результат": time_diff_str
        }

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(final_results, json_file, ensure_ascii=False, indent=4)


# Использование функции
athletes_json_file = 'competitors2.json'
results_txt_file = 'results_RUN.txt'
output_json_file = ' final_results.json'
print_results_table(athletes_json_file, results_txt_file, output_json_file)
