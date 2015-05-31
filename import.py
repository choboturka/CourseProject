__author__ = 'Vlad'
from server import db, School, Result
import os
import csv
import time

#region Constants
SUBJECTS = ['Українська мова та література',
            'Історія України',
            'Математика',
            'Фізика',
            'Хімія',
            'Біологія',
            'Географія',
            'Англійська мова',
            'Французька мова',
            'Німецька мова',
            'Іспанська мова',
            'Російська мова',
            'Всесвітня історія',
            'Світова література']

REGIONS = ['Автономна Республіка Крим',
           'Вінницька область',
           'Волинська область',
           'Дніпропетровська область',
           'Донецька область',
           'Житомирська область',
           'Закарпатська область',
           'Запорізька область',
           'Івано-Франківська область',
           'Київська область',
           'Кіровоградська область',
           'Луганська область',
           'Львівська область',
           'Миколаївська область',
           'Одеська область',
           'Полтавська область',
           'Рівненська область',
           'Сумська область',
           'Тернопільська область',
           'Харківська область',
           'Херсонська область',
           'Хмельницька область',
           'Черкаська область',
           'Чернівецька область',
           'Чернігівська область',
           # 'м.Київ',
           # 'м.Севастополь'
           ]

# YEAR = 2010
PATH = [r'E:\ZNO\ZNO2010',
        r'E:\ZNO\ZNO2011',
        r'E:\ZNO\ZNO2012',
        r'E:\ZNO\ZNO2013',
        r'E:\ZNO\ZNO2014']


EXTRA = [r'E:\ZNO\xls']
DEBUG = True
#endregion

def check_in(str, list):
    for i, e in enumerate(list):
        if e in str:
            return list[i]

def import_data(path):
    year = int(path[-4:])
    if DEBUG: print(year)
    for filename in os.listdir(path):
        if '.csv' in filename and ',' in filename:
            parts = filename[:-4].split(', ')
            subject = check_in(parts[0], SUBJECTS)
            reg_name = check_in(parts[0], REGIONS)
            area = parts[1]
            # get or create region
            with open(path + '\\' + filename) as csv_file:
                reader = csv.reader(csv_file, delimiter=',', quotechar='|')
                for row in reader:
                    school = School.query.filter_by(name=row[0]).first()
                    if not school:
                        school = School(row[0], row[1], reg_name, area, extra=False)
                    db.session.add(school)
                    #if DEBUG: print(school.name, school.type)
                    result = Result.query.filter_by(school=school, year=year, subject=subject).first()
                    if not result:
                        # print('none')
                        result = Result(school,year,subject,row[2],
                                        row[3],row[4],row[5],row[6],row[7],
                                        row[8],row[9],row[10],row[11],row[12])
                        # if DEBUG: print(result.school.name, result.subject, result.total_students)
                    db.session.add(result)
            db.session.commit()

if __name__ == '__main__':
    # db.create_all()
    for i in range(1,5):
        start_time = time.time()
        import_data(PATH[i])
        print("--- {0} minutes ---".format((time.time() - start_time)/60))
    # import_data(PATH[0])
    # pass







