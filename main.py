import psycopg2
# 1. Функция, создающая структуру БД (таблицы)
def create_db(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_information(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        second_name VARCHAR(40) NOT NULL,
        email VARCHAR(80) UNIQUE NOT NULL      
        );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phone_numbers(
        id SERIAL PRIMARY KEY,
        personal_id INTEGER REFERENCES personal_information(id),
        telephon_number VARCHAR(11) 
        );
    """)


# 2. Функция, позволяющая добавить нового клиента
def add_client(cursor, first_name, second_name, email, telephon_number=None):
    cursor.execute(""" 
    INSERT INTO personal_information(first_name, second_name, email)
    VALUES( %s, %s, %s);
    """, (first_name, second_name, email))
    cursor.execute(""" 
    INSERT INTO phone_numbers(telephon_number)
    VALUES(%s);
    """, (telephon_number,))


# 3. Функция, позволяющая добавить телефон для существующего клиента
def add_phone_number(cursor, personal_id, telephon_number=None):
    cursor.execute(""" 
    INSERT INTO phone_numbers(personal_id, telephon_number)
    VALUES( %s, %s);
    """, (personal_id, telephon_number))

# 4. Функция, позволяющая изменить данные о клиенте
def change_client(cursor, id, first_name=None, second_name=None, email=None, telephon_number=None):
    cursor.execute(""" 
    UPDATE personal_information SET first_name=%s, second_name=%s, email=%s WHERE id=%s;
    """, (first_name, second_name, email, id))
    cursor.execute(""" 
    UPDATE phone_numbers SET telephon_number=%s  WHERE id=%s;
    """, (telephon_number, id))

# 5. Функция, позволяющая удалить телефон для существующего клиента
def del_phone_number(cursor, personal_id, telephon_number):
    cursor.execute("""
    DELETE FROM phone_numbers WHERE personal_id=%s AND telephon_number=%s;
    """, (personal_id, telephon_number))

# 6. Функция, позволяющая удалить существующего клиента
def del_client(cursor, personal_id):
   cursor.execute("""
   DELETE FROM phone_numbers WHERE personal_id=%s;
   """, (personal_id,))
   cursor.execute("""
   DELETE FROM personal_information WHERE id=%s;
   """, (personal_id,))

# 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(cursor, first_name=None, second_name=None, email=None, telephon_number=None):
    cursor.execute(""" 
    SELECT first_name, second_name, email, telephon_number FROM personal_information
    JOIN phone_numbers ON personal_information.id=phone_numbers.personal_id
    WHERE first_name=%s OR second_name=%s OR email=%s OR telephon_number=%s
    """, (first_name, second_name, email, telephon_number))
    return cursor.fetchall()

with psycopg2.connect(database="homework_2", user="postgres", password="Catrin.Sin.13") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_numbers;
        """)
        cur.execute("""
        DROP TABLE personal_information;
        """)

        create_db(cur)
        add_client(cur, 'Лев', 'Толстой', 'lev.tolstoy@yandex.ru', '9123456789')
        add_client(cur, 'Стивен', 'Кинг', 'stiv.king@gmail.com', '9164958231')
        add_client(cur, 'Анна', 'Гранде', 'grand.ann@gmail.com', '9562495785')
        add_phone_number(cur, 1, '98563562451')
        change_client(cur, 1, 'Иван', 'Бунин', 'bunin.iv@ya.ru', '9563214568')
        del_phone_number(cur, 1, '9563214568')
        del_client(cur, 1)
        print(find_client(cur, first_name='Анна'))


conn.close()

