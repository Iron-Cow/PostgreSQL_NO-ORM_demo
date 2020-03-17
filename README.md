Hello.

I decided to practice with pure SQL and created test Django app without ORM with PostgreSQL.
It contains workout with 2 tables:
* human genders (id, name, age, gender)
* humans (id, name)

Humans table depends on genders via foreign keys.
As db I use fre Postgres Elephant SQL (https://customer.elephantsql.com/)

To replicate the project:
* git clone https://github.com/Iron-Cow/PostgreSQL_NO-ORM_demo.git
* activate your virtual env : 

    python3.8 -m venv venv
    source venv/bin/activate
    
* pip install -r requirements.txt
* setup your db data in settings.py