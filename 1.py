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


def parse_food(input_str):
    parts = input_str.split('"')[1:]
    name = parts[0].replace('"', '')
    parts = parts[1].split(' ')
    start_date = datetime.strptime(parts[1], "%Y.%m.%d")
    end_date = datetime.strptime(parts[2], "%Y.%m.%d")
    price = float(parts[3])

    return {"name": name, "start_date": start_date, "end_date": end_date, "price": price}


with open('1.txt', 'r', encoding='utf-8') as file1:

    print("Данные из 1.txt:")
    for i in file1:
        print(parse_input(i))


with open('2.txt', 'r', encoding='utf-8') as file:

    print("Данные из 2.txt:")
    for i in file:
        print(parse_product(i))


with open('3.txt', 'r', encoding='utf-8') as file:

    print("Данные из 3.txt:")
    for i in file:
        print(parse_food(i))