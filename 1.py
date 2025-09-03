from datetime import datetime


def parse_product(input_str):
    parts = input_str.split('"')[1:]
    name = parts[0].replace('"', '')
    price = float(parts[1])
    provider = parts[2].replace('"', '')
    return {'name': name, 'price': price, 'provider': provider}


def parse_input(input_str):
    parts = input_str.split('"')
    date_str = parts[0].strip().split()
    date_str = str(date_str[0])
    product_name = parts[1]
    quantity = int(parts[2])
    date = datetime.strptime(date_str, "%Y.%m.%d")
    return {"Дата": date.strftime('%Y.%m.%d'), "Название": product_name, "Количество": quantity}


try:
    with open('1.txt', 'r', encoding='utf-8') as file1:

        print("Данные из 1.txt:")
        for i in file1:
            print(parse_input(i))

    with open('2.txt', 'r', encoding='utf-8') as file2:

        print("Данные из 1.txt:")
        for i in file2:
            print(parse_product(i))


except FileNotFoundError as e:
    print(f"Ошибка: Файл не найден - {e}")
except Exception as e:
    print(f"Произошла ошибка при чтении файлов: {e}")