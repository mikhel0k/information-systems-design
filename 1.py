from datetime import datetime


def parse_product(input_str):
    parts = input_str.split('"')[1:]
    name = parts[0].replace('"', '')
    price = float(parts[1])
    provider = parts[2].replace('"', '')
    return {'name': name, 'price': price, 'provider': provider}


def parse_delivery(input_str):
    parts = input_str.split('"')
    date_str = parts[0].strip().split()
    date_str = str(date_str[0])
    product_name = parts[1]
    quantity = int(parts[2])
    date = datetime.strptime(date_str, "%Y.%m.%d")
    return {"date": date.strftime('%Y.%m.%d'), "name": product_name, "count": quantity}


def parse_food(input_str):
    parts = input_str.split('"')[1:]
    name = parts[0].replace('"', '')
    parts = parts[1].split(' ')
    start_date = datetime.strptime(parts[1], "%Y.%m.%d")
    end_date = datetime.strptime(parts[2], "%Y.%m.%d")
    price = float(parts[3])

    return {"name": name, "start_date": start_date, "end_date": end_date, "price": price}


def parse_drinks(input_str):
    parts = input_str.split('"')[1:]
    name = parts[0].replace('"', '')
    parts = parts[1].split(' ')
    start_date = datetime.strptime(parts[1], "%Y.%m.%d")
    end_date = datetime.strptime(parts[2], "%Y.%m.%d")
    price = float(parts[3])
    volume = float(parts[4])

    return {"name": name, "start_date": start_date, "end_date": end_date, "price": price, "volume": volume}


def add_from_file(function, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        print(f"Данные из {file_name}:")
        for i in file:
            print(function(i))
        print()


add_from_file(parse_delivery, '1.txt')
add_from_file(parse_product, '2.txt')
add_from_file(parse_food, '3.txt')
add_from_file(parse_drinks, '4.txt')
