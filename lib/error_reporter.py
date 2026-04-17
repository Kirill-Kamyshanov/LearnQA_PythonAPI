import datetime
import os
from requests import Response

class ErrorReporter:
    file_name = f"error_reports/report_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"
    error_number = 0

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
            new_data = f'Всего упало {cls.error_number} тестов:\n' +  ''.join(filtered_lines)


        with open(cls.file_name, 'w', encoding='utf-8') as error_report_file:
            error_report_file.write(new_data)



