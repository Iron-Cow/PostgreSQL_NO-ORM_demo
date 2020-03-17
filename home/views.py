from django.shortcuts import render, redirect
from django.db import connection


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def basic_df_setup(request):
    """Function for check, if all required DBs created"""
    with connection.cursor() as cursor:
        cursor.execute(f"""
        SELECT
           *
        FROM
           pg_catalog.pg_tables
        where tablename in ('home_human', 'home_gender')
        """)
        tables_raw = dictfetchall(cursor)
    tables = [(i['tablename']) for i in tables_raw]
    if sorted(tables) != sorted(['home_human', 'home_gender']):  # Here is manual placement of table names
        print('not fine')
        return redirect("/basic_setup")
    print('fine')
    return None


def index(request):
    """Main page of test website. Show created humans, available form for new humans"""
    check = basic_df_setup(request)
    if check:
        return check

    data = dict()
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM home_gender")
            genders = dictfetchall(cursor)
            data["genders"] = genders

            cursor.execute("""
            SELECT home_human.id as id, home_human.name as name, home_human.age as age, home_gender.name as gender_name
            FROM home_human
            LEFT JOIN home_gender
            ON home_human.gender_id = home_gender.id
            """)

            humans = dictfetchall(cursor)

            data["humans"] = humans
        return render(request, 'index.html', data)

    elif request.method == 'POST':
        name = request.POST.get('human_name')
        age = request.POST.get('human_age')
        gender = request.POST.get('human_gender')
        with connection.cursor() as cursor:
            cursor.execute(f"""
                        INSERT INTO home_human(name, age, gender_id)
                        VALUES ('{name}', {age}, 
                        (select id from home_gender where name = '{gender}'))
                        """)
        return redirect("/")


def delete_human(request, human_id: int):
    '''Procedure to delete human by id'''
    with connection.cursor() as cursor:
        cursor.execute(f"""
            DELETE FROM home_human WHERE home_human.id = {human_id}; 
        """)
    return redirect("/")


def update_human(request, human_id):
    '''Part of CRUD human. Dedicated page'''
    data = dict()
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM home_gender")
            genders = dictfetchall(cursor)

            human = cursor.execute(f"""
                select * from 
                (SELECT home_human.id as id, home_human.name as name, home_human.age as age, home_gender.name as gender_name
                FROM home_human
                LEFT JOIN home_gender
                ON home_human.gender_id = home_gender.id) as querry
                where querry.id = {human_id}
                    """)
            human = dictfetchall(cursor)
        data["genders"] = genders
        data["human"] = human[0]
        return render(request, 'human_change.html', data)
    if request.method == 'POST':
        name = request.POST.get('human_name')
        age = request.POST.get('human_age')
        gender = request.POST.get('human_gender')
        with connection.cursor() as cursor:
            cursor.execute(f""" 
                            UPDATE home_human
                            SET name = '{name}', age = {age}, 
                                gender_id = (select id from home_gender where name = '{gender}')
                            WHERE id = {human_id} 
                            """)
        return redirect("/")


def basic_setup(request):
    """Page formed to setup db tables, which not crated yet"""
    data = dict()
    with connection.cursor() as cursor:
        cursor.execute(f"""
           SELECT * 
           FROM pg_catalog.pg_tables
           WHERE tablename in ('home_human', 'home_gender')
           """)
        tables_raw = dictfetchall(cursor)
    tables = [(i['tablename']) for i in tables_raw]
    sample = sorted(['home_human', 'home_gender'])

    if sorted(tables) != sample:
        missing_tables = []

        for table in sample:
            if table not in tables:
                missing_tables.append(table)

        data['missing_tables'] = missing_tables
    return render(request, 'no_tables.html', data)


def create_home_gender(request):
    """Creates create_home_gender table in the db"""
    with connection.cursor() as cursor:
        cursor.execute(f"""
           CREATE TABLE home_gender (
            id serial primary key,
            name varchar(255)
            );
            INSERT INTO home_gender(name) VALUES ('male');
            INSERT INTO home_gender(name) VALUES ('female');
            INSERT INTO home_gender(name) VALUES ('other');
            ;""")
    return redirect("/")


def create_home_human(request):
    """Creates create_home_human table in the db"""
    with connection.cursor() as cursor:
        cursor.execute(f"""
           CREATE TABLE home_human (
            id serial primary key,
            name varchar(255),
            age integer,
            gender_id integer REFERENCES home_gender(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """)
    return redirect("/")

