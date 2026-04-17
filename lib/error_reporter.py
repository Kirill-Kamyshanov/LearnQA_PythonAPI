import datetime
import os


class ErrorReporter:
    file_name = f"error_reports/report_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"
    error_number = 0
    # Списки для грамматического соответствия первой строки правилам русского языка. Чтобы глаз не резало у того кто читает отчёт
    l = [1, 21, 31, 41, 51, 61, 71, 81, 91]

    lo = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40,
        45, 46, 47, 48, 49, 50, 55, 56, 57, 58, 59, 60, 65, 66, 67, 68, 69, 70, 75, 76, 77, 78, 79, 80,
        85, 86, 87, 88, 89, 90, 95, 96, 97, 98, 99, 100]

    li = [2, 3, 4, 22, 23, 24, 32, 33, 34,  42, 43, 44,  52, 53, 54, 62, 63, 64, 72, 73, 74, 82, 83, 84,  92, 93, 94]

    @classmethod
    def _write_error_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as error_report_file:
            error_report_file.write(data)


    @classmethod
    def add_error(cls, step, waiting_result, actual_result):
        data_to_add = f'Всего упало {cls.error_number} тестов:\n'
        data_to_add += "\n"
        data_to_add += f'Тест {cls.error_number + 1}:\n'
        data_to_add += f'{os.environ.get('PYTEST_CURRENT_TEST')}\n'
        data_to_add += f'Шаг: {step}\n'
        data_to_add += f'Ожидаемый результат: {waiting_result}\n'
        data_to_add += f'Действительный результат: {actual_result}\n'
        data_to_add += "\n"
        cls.error_number += 1

        cls._write_error_to_file(data_to_add)
        cls._change_first_string()

    @classmethod
    def _change_first_string(cls):
        with open(cls.file_name, 'r', encoding='utf-8') as error_report_file:
            data = error_report_file.readlines()
            del data[0]
            filtered_lines = [line for line in data if not line.startswith('Всего')]
            if cls.error_number in cls.l:
                new_data = f'Всего упал {cls.error_number} тест:\n' +  ''.join(filtered_lines)
            elif cls.error_number in cls.lo:
                new_data = f'Всего упало {cls.error_number} тестов:\n' + ''.join(filtered_lines)
            elif cls.error_number in cls.li:
                new_data = f'Всего упали {cls.error_number} теста:\n' + ''.join(filtered_lines)


        with open(cls.file_name, 'w', encoding='utf-8') as error_report_file:
            error_report_file.write(new_data)



