#!/usr/bin/python3
# @Time    : 2021/4/10 11:17 下午
# @Author  : WangXin
import os

from flask import Flask
from flask_cors import CORS
from flask import request
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins
from cors_utils import TabrResource

username = "root"
password = "123456"
host = "localhost"
dbname = "testcase"
options = "charset=utf8mb4"

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{dbname}?{options}'
app.config['testcase'] = []
db = SQLAlchemy(app)


def after_request(response):
    # JS前端跨域支持
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


app.after_request(after_request)


class TestCase(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    file_name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=True)
    content = db.Column(db.String(5000), unique=False, nullable=False)
    report = db.relationship("Report", backref="test_case", lazy=True)

    def as_dict(self):
        return {"name": self.name, "file_name": self.file_name, "description": self.description,
                "content": self.content}

    def __repr__(self):
        return '<TestCase %r>' % self.file_name


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), unique=False, nullable=True)
    dir = db.Column(db.String(300), unique=False, nullable=False)
    testcase_id = db.Column(db.String(80), db.ForeignKey("test_case.name"), nullable=False)

    def __repr__(self):
        return '<Report %r>' % self.description


class TestCaseDB(TabrResource):
    def get(self):
        if 'id' in request.args:
            # 从用例库中找对应的用例
            for i in app.config["testcase"]:
                # 返回用例
                if i["id"] == int(request.args["id"]):
                    return i
        else:
            return app.config["testcase"]

    def post(self):
        """
        存储用例
        :return:
        """
        if "file" in request.files and "name" in request.form:
            f = request.files["file"]
            name = request.form['name']
            file_name = f.filename
            content = f.read()
            testcase = TestCase(name=name, file_name=file_name, content=content)
            db.session.add(testcase)
            db.session.commit()
            return {"result": "ok", "errcode": "200"}
        else:
            testcase = TestCase(**request.json)
            db.session.add(testcase)
            db.session.commit()
            return {"result": "ok", "errcode": "200"}

        # 返回不同的状态码，和默认的错误页
        abort(404)

    def put(self):
        """
        更新用例
        :return:
        """
        if "name" in request.json:
            testcase = TestCase.query.filter_by(name=request.json.get('name')).first()
            testcase.content = request.json.get("content")
            testcase.description = request.json.get("description")
            testcase.file_name = request.json.get("file_name")
            db.session.commit()
            return {"errcode": 0, "content": "OK"}



class TestCaseStore(TabrResource):

    def post(self):
        if "file" in request.files and "name" in request.form:
            f = request.files["file"]
            name = request.form["name"]
            file_name = f.filename
            connect = f.read()
            db.session.add(TestCase(name=name, file_name=file_name, connect=connect))
            db.session.commit()
            return "ok"
        abort(404)


class TestCaseRun(TabrResource):

    def get(self):
        """
        run
        :return:
        """
        if "name" in request.args:
            name = request.args["name"]
            data = TestCase.query.filter_by(name=name).first()
            return data.connect


class TestCaseGet(TabrResource):

    def get(self):
        """
        根据name查询测试用例,无name则查询所有用例
        :return:
        """
        if "name" in request.args:
            name = request.args["name"]
            data = TestCase.query.filter_by(name=name).first()
            return data.content
        return {"errcode": 0, "body": [i.as_dict() for i in TestCase.query.all()]}


@app.route("/run", methods=["get"])
def run():
    if "name" in request.args:
        name = request.args["name"]
        data = TestCase.query.filter_by(name=name).first()
        J = Jenkins("http://localhost:8080/", username="admin", password="123456", useCrumb=True)
        print(J.keys())
        r = J["TestPlatform"].invoke(build_params={"name": name, "file_name": data.file_name})
        if r.is_queued() or r.is_running():
            r.block_until_complete()

        build = r.get_build()
        print(build)
        return "ok"
    abort(404)


@app.route("/report_upload", methods=["post"])
def report_upload():
    if "file" in request.files and "name" in request.form:
        DIR = r"/Users/xinximo/"
        f = request.files["file"]
        name = request.form['name']
        file_name = f.filename
        dir = os.path.join(DIR, file_name)
        f.save(dir)
        report = Report(dir=dir, testcase_id=name)
        db.session.add(report)
        db.session.commit()
        return "OK"
    abort(404)


class Login(TabrResource):
    def post(self):
        print(request.json)
        if "wx" in request.json.get("account") and "123456" == request.json.get("password"):
            return {"msg": "OK"}
        else:
            return {"msg": "ERROR"}


api.add_resource(TestCaseDB, '/testcase', endpoint='get_case')
api.add_resource(TestCaseStore, '/testcase_store')
api.add_resource(TestCaseRun, '/testcase_run')
api.add_resource(TestCaseGet, '/get_testcase')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
    # db.drop_all()
    # db.create_all()
