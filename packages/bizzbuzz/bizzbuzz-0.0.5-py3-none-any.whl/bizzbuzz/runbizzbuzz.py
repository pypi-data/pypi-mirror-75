import os

def main():
    os.system("python manage.py migrate && python manage.py populate_db && python manage.py runserver")

if __name__ == '__main__':
    main()