from flask import Flask,redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_restless import APIManager

SQLITE_WIN_PATH = 'sqlite:///C:\\Users\\Vlad\\PycharmProjects\\untitled1\\results.db'
POSTGRES_PATH = 'postgresql://vlad:12345@localhost:5432/results'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_PATH
db = SQLAlchemy(app)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    type = db.Column(db.Unicode)
    region = db.Column(db.Unicode)
    area = db.Column(db.Unicode)
    # Other data
    has_extra_data = db.Column(db.Boolean)

    has_comp_class = db.Column(db.Boolean)
    comp_classes = db.Column(db.Integer)

    computers = db.Column(db.Integer)
    working_computers = db.Column(db.Integer)

    has_internet = db.Column(db.Boolean)
    internet_type = db.Column(db.Unicode)
    internet_speed = db.Column(db.Unicode)

    informatics_teachers = db.Column(db.Integer)

    def __init__(self, name, type, region, area,
                 extra=None, has_class=None, classes=None, pc=None, work_pc=None,
                 has_int=None, int_type=None, int_speed=None, teachers=None):

        self.name = name
        self.type = type
        self.region = region
        self.area = area

        if extra:
            self.has_extra_data = True
            self.has_comp_class = has_class
            self.comp_classes = classes
            self.computers = pc
            self.working_computers = work_pc
            self.has_internet = has_int
            self.internet_type = int_type
            self.internet_speed = int_speed
            self.informatics_teachers = teachers
    # results = db.relationship('Result', backref='school')

    def location(self):
        return self.region + ', ' + self.area

    def extra(self):
        if self.has_extra_data:
            return dict(has_comp_class=self.has_comp_class,
                        comp_classes =self.comp_classes,
                        computers=self.computers,
                        working_computers=self.working_computers,
                        has_internet=self.has_internet,
                        internet_type=self.internet_type,
                        internet_speed=self.internet_speed,
                        informatics_teachers=self.informatics_teachers)
        else:
            return None


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship('School', backref='results')
    year = db.Column(db.Integer)
    subject = db.Column(db.Unicode)
    students = db.Column(db.Integer)
    val0 = db.Column(db.Float)
    val1 = db.Column(db.Float)
    val2 = db.Column(db.Float)
    val3 = db.Column(db.Float)
    val4 = db.Column(db.Float)
    val5 = db.Column(db.Float)
    val6 = db.Column(db.Float)
    val7 = db.Column(db.Float)
    val8 = db.Column(db.Float)
    val9 = db.Column(db.Float)

    def __init__(self,school, year, subject, students, val0, val1, val2, val3, val4, val5, val6, val7, val8, val9):
        self.school = school
        self.year = year
        self.subject = subject
        self.students = int(float(students))
        self.val0 = val0
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
        self.val5 = val5
        self.val6 = val6
        self.val7 = val7
        self.val8 = val8
        self.val9 = val9

    def scores(self):
        return [self.val0,
                self.val1,
                self.val2,
                self.val3,
                self.val4,
                self.val5,
                self.val6,
                self.val7,
                self.val8,
                self.val9]

    def abs_scores(self):
        return [int(self.students/100*self.val0),
                int(self.students/100*self.val1),
                int(self.students/100*self.val2),
                int(self.students/100*self.val3),
                int(self.students/100*self.val4),
                int(self.students/100*self.val5),
                int(self.students/100*self.val6),
                int(self.students/100*self.val7),
                int(self.students/100*self.val8),
                int(self.students/100*self.val9)]


@app.route('/')
def index():
    return redirect('/api/simple/results?q={"filters":[{"name":"school","op":"has","val":{"name":"area","op":"ilike","val":"%район%"}}]}')


if __name__ == '__main__':

    mr_manager = APIManager(app, flask_sqlalchemy_db=db)

    simple_methods = ['abs_scores', 'scores', 'school.location', 'school.extra']
    simple_columns = ['year', 'subject', 'students', 'school', 'school.name', 'school.type', 'school_id']

    mr_manager.create_api(Result, url_prefix='/api/all',
                          collection_name='results', methods=['GET'],
                          # include_methods=simple_methods,
                          # include_columns=simple_columns,
                          #exclude_columns=['school'],
                          results_per_page=10000,
                          max_results_per_page=10000,
                          # exclude_columns=['id', 'school.id', 'school_id'],
                          # preprocessors={'GET_MANY':[]},
                          # postprocessors={'GET_MANY':[]}
                          )

    mr_manager.create_api(Result, url_prefix='/api/v2',
                          collection_name='results', methods=['GET'],
                          include_methods=simple_methods,
                          # include_columns=simple_columns,
                          results_per_page = 20,
                          # max_results_per_page = 100,
                          # allow_functions = True,
                          exclude_columns=['id', 'school.id', 'school_id', 'school.area', 'school.region',
                                            'school.has_extra_data', 'school.has_comp_class','school.comp_classes',
                                            'school.computers','school.working_computers',
                                            'school.has_internet','school.internet_type',
                                            'school.internet_speed','school.informatics_teachers',
                                             'val0','val1','val2','val3','val4','val5','val6','val7', 'val8','val9'],
                          # preprocessors={'GET_MANY':[]},
                          # postprocessors={'GET_MANY':[]}
                          )

    app.run()