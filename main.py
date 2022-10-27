import psycopg2

with psycopg2.connect(database="homework_2", user="postgres", password="Catrin.Sin.13") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_numbers;
        """)
        cur.execute("""
        DROP TABLE personal_information;
        """)


        # 1. Функция, создающая структуру БД (таблицы)
        def create_db(connection):
            connection.cursor().execute("""
            CREATE TABLE IF NOT EXISTS personal_information(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                second_name VARCHAR(40) NOT NULL,
                email VARCHAR(80) UNIQUE NOT NULL      
                );
            """)
            connection.cursor().execute("""
            CREATE TABLE IF NOT EXISTS phone_numbers(
                id SERIAL PRIMARY KEY,
                personal_id INTEGER REFERENCES personal_information(id),
                telephon_number VARCHAR(11) 
                );
            """)
            connection.commit()


        # 2. Функция, позволяющая добавить нового клиента
        def add_client(connection, first_name, second_name, email, telephon_number=None):
            connection.cursor().execute(""" 
            INSERT INTO personal_information(first_name, second_name, email)
            VALUES( %s, %s, %s);
            """, (first_name, second_name, email))
            connection.cursor().execute(""" 
            INSERT INTO phone_numbers(telephon_number)
            VALUES(%s);
            """, (telephon_number,))
            connection.commit()


        # 3. Функция, позволяющая добавить телефон для существующего клиента
        def add_phone_number(connection, personal_id, telephon_number=None):
            connection.cursor().execute(""" 
            INSERT INTO phone_numbers(personal_id, telephon_number)
            VALUES( %s, %s);
            """, (personal_id, telephon_number))
            connection.commit()


        # 4. Функция, позволяющая изменить данные о клиенте
        def change_client(connection, first_name, second_name, email, id, telephon_number=None):
            connection.cursor().execute(""" 
            UPDATE personal_information SET first_name=%s, second_name=%s, email=%s WHERE id=%s;
            """, (first_name, second_name, email, id))
            connection.cursor().execute(""" 
            UPDATE phone_numbers SET telephon_number=%s  WHERE id=%s;
            """, (telephon_number, id))
            connection.commit()


        # 5. Функция, позволяющая удалить телефон для существующего клиента
        def del_phone_number(connection, personal_id, telephon_number):
            connection.cursor().execute("""
            DELETE FROM phone_numbers WHERE personal_id=%s AND telephon_number=%s;
            """, (personal_id, telephon_number))
            connection.commit()


        # 6. Функция, позволяющая удалить существующего клиента
        def del_client(connection, personal_id):
            connection.cursor().execute("""
            DELETE FROM phone_numbers WHERE personal_id=%s;
            """, (personal_id,))
            connection.cursor().execute("""
            DELETE FROM personal_information WHERE id=%s;
            """, (personal_id,))
            # connection.cursor().execute("""
            # SELECT * FROM personal_information;
            # """)
            connection.commit()


        # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
        def find_client(connection, first_name=None, second_name=None, email=None, telephon_number=None):
            connection.cursor().execute(""" 
            SELECT first_name, second_name, email, telephon_number FROM personal_information
            JOIN phone_numbers ON personal_information.id=phone_numbers.personal_id
            WHERE first_name=%s OR second_name=%s OR email=%s OR telephon_number=%s
            """, (first_name, second_name, email, telephon_number))
            print(connection.cursor().fetchall())


        create_db(conn)
        add_client(conn, 'Лев', 'Толстой', 'lev.tolstoy@yandex.ru', '9123456789')
        add_client(conn, 'Стивен', 'Кинг', 'stiv.king@gmail.com', '9164958231')
        add_client(conn, 'Анна', 'Гранде', 'grand.ann@gmail.com', '9562495785')
        add_phone_number(conn, 1, '98563562451')
        change_client(conn, 'Иван', 'Бунин', 'bunin.iv@ya.ru', 1, '9563214568')
        del_phone_number(conn, 1, '9563214568')
        del_client(conn, 1)
        find_client(conn, first_name='Анна')


conn.close()

