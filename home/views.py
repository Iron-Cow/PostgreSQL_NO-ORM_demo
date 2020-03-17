from django.shortcuts import render, redirect
from django.db import connection


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



def index(request):
    data = dict()
    if request.method == 'GET':
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM home_gender")
            genders = dictfetchall(cursor)


            cursor.execute("""
            SELECT home_human.id as id, home_human.name as name, home_human.age as age, home_gender.name as gender_name
            FROM home_human
            LEFT JOIN home_gender
            ON home_human.gender_id = home_gender.id
            """)

            humans = dictfetchall(cursor)

            print(genders)
            print(humans)
            data["genders"] = genders
            data["humans"] = humans
        return render(request, 'index.html', data)
    elif request.method == 'POST':
        name = request.POST.get('human_name')
        age = request.POST.get('human_age')
        gender = request.POST.get('human_gender')
        print(name, age, gender)
        with connection.cursor() as cursor:

            cursor.execute(f"""
                        INSERT INTO home_human(name, age, gender_id)
                        VALUES ('{name}', {age}, 
                        (select id from home_gender where name = '{gender}'))
                        """)

        return redirect("/")


def delete_human(request, human_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            DELETE FROM home_human WHERE home_human.id = {human_id}; 
        """)
    return redirect("/")


def update_human(request, human_id):
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
        print(human)

        return render(request, 'human_change.html', data)
    if request.method == 'POST':
        name = request.POST.get('human_name')
        age = request.POST.get('human_age')
        gender = request.POST.get('human_gender')
        return render(request, 'human_change.html', data)

        print(name, age, gender)
        with connection.cursor() as cursor:
            cursor.execute(f"""
                                INSERT INTO home_human(name, age, gender_id)
                                VALUES ('{name}', {age}, 
                                (select id from home_gender where name = '{gender}'))
                                """)
