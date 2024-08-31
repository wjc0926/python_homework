import csv
import re
import pymysql

# 数据库连接配置，请根据实际情况填写
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'house_data',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 连接到数据库
connection = pymysql.connect(**db_config)
try:
    with connection.cursor() as cursor:

        # 创建houses表的SQL语句
        create_table_query = """
                CREATE TABLE IF NOT EXISTS houses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    house_title VARCHAR(255),
                    link VARCHAR(255),
                    unit_type VARCHAR(255),
                    area DECIMAL(10, 2),
                    house_facing VARCHAR(50),
                    decoration_form VARCHAR(50),
                    district_name VARCHAR(255),
                    address VARCHAR(255),
                    attention_count INT,
                    total_price DECIMAL(15, 2),
                    unit_price DECIMAL(10, 2),
                    picture_path VARCHAR(255)
                )
                """

        # 执行创建表的SQL语句
        cursor.execute(create_table_query)
        connection.commit()

        csv_file_path = 'D:\\csdn_example-vgg16\\vgg16\\PaChong\\lianjiacraw-master\\src\\main\\houses.csv'
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header

            for row in reader:
                # Extract attention count
                attention_text = row[8]
                attention_match = re.match(r'^(\d+)人关注', attention_text)
                attention_count = int(attention_match.group(1)) if attention_match else None

                # Extract area
                area_text = row[3]
                area_match = re.match(r'^(\d+(\.\d+)?)平米$', area_text)
                area = float(area_match.group(1)) if area_match else None

                # # 直接使用row[9]作为total_price，假设第九列已经是正确格式的数值
                # total_price = float(row[9].replace(',', '')) if row[9] else None

                # 对unit_price进行清理，移除逗号和非数字字符
                unit_price_text = row[10].replace(',', '').replace('元/平', '')
                unit_price = float(unit_price_text) if unit_price_text.isdigit() or (
                            unit_price_text.find('.') != -1 and unit_price_text.replace('.', '', 1).isdigit()) else None

                # 注意更新data_to_insert中的unit_price值
                data_to_insert = (
                    row[0], row[1], row[2], area, row[4], row[5], row[6], row[7],
                    attention_count, row[9], unit_price, row[11])
                # Insert query
                insert_query = """
                INSERT INTO houses 
                (house_title, link, unit_type, area, house_facing, decoration_form, district_name, address, attention_count, total_price, unit_price, picture_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_query, data_to_insert)

    connection.commit()
except Exception as e:
    print(f"An error occurred during data insertion: {e}")
    connection.rollback()
finally:
    connection.close()
    print("Database operation completed.")