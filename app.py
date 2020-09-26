from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/epicDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DB
db = SQLAlchemy(app)


#Init ma
ma = Marshmallow(app)

# Department Class/ Model
class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dept_name = db.Column(db.String(50), unique = True)
    dept_address = db.Column(db.String(200), nullable = False)
    
    def __init__(self, dept_name, dept_address):
        self.dept_name = dept_name
        self.dept_address = dept_address

# Dept Schema
class DeptSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dept_name', 'dept_address')

#Init Dept Schema
dept_schema = DeptSchema()
depts_schema = DeptSchema(many = True)


# Create Department
@app.route('/department', methods=['POST'])
def add_dept():
    dept_name = request.json['dept_name']
    dept_address = request.json['dept_address']

    new_dept = Department(dept_name, dept_address)

    db.session.add(new_dept)
    db.session.commit()

    return dept_schema.jsonify(new_dept)

# Get all Department
@app.route("/department", methods = ['GET'])
def get_departments():
    all_departments = Department.query.all()
    result = depts_schema.dump(all_departments)
    return jsonify(result)

# Get one Department using id
@app.route("/department/<id>", methods = ['GET'])
def get_department(id):
    department = Department.query.get(id)
    return dept_schema.jsonify(department)

# Update Department
@app.route('/department/update/<id>', methods=['PUT'])
def update_dept(id):
    department = Department.query.get(id)

    dept_name = request.json['dept_name']
    dept_address = request.json['dept_address']

    department.dept_name = dept_name
    department.dept_address = dept_address

    db.session.commit()

    return dept_schema.jsonify(department)

# Delete Department
@app.route("/department/<id>", methods = ['DELETE'])
def delete_department(id):
    department = Department.query.get(id)
    db.session.delete(department)
    db.session.commit()
    return dept_schema.jsonify(department)

# Employee Class/ Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    emp_name = db.Column(db.String(50), nullable = False)
    emp_address = db.Column(db.String(200), nullable = False)
    designation = db.Column(db.String(50), nullable = False)
    dob = db.Column(db.String(8), nullable = False)
    telephone = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    dept_id = db.Column(db.Integer)

    def __init__(self, emp_name, emp_address, designation, dob, telephone, email, dept_id):
        self.emp_name = emp_name
        self.emp_address = emp_address
        self.designation = designation
        self.dob = dob
        self.telephone = telephone
        self.email = email
        self.dept_id = dept_id

# Emp Schema
class EmpSchema(ma.Schema):
    class Meta:
        fields = ('id', 'emp_name', 'emp_address', 'designation', 'dob', 'telephone', 'email', 'dept_id')

#Init Emp Schema
emp_schema = EmpSchema()
emps_schema = EmpSchema(many = True)

# Create Employee
@app.route('/employee', methods=['POST'])
def add_emp():
    emp_name = request.json['emp_name']
    emp_address = request.json['emp_address']
    designation = request.json['designation']
    dob = request.json['dob']
    telephone = request.json['telephone']
    email = request.json['email']
    dept_id = request.json['dept_id']

    print("**************************************")
    dep = Department.query.get(dept_id)
    result = dept_schema.dump(dep)
    print(result)
    if (dep == None):
        return jsonify({"Msg": "Invalid Department ID"})
    print("**************************************")


    new_emp = Employee(emp_name, emp_address, designation, dob, telephone, email, dept_id)

    db.session.add(new_emp)
    db.session.commit()

    return emp_schema.jsonify(new_emp)

# Get all Employees
@app.route("/employee", methods = ['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = emps_schema.dump(all_employees)
    print("________________________")
    print(result)
    print("________________________")

    return jsonify(result)

# Get employee using id
@app.route("/employee/<id>", methods = ['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if (employee == None):
        return jsonify({"Msg": "Employee not found with id " + id})

    return emp_schema.jsonify(employee)

# Update Employee
@app.route('/employee/update/<id>', methods=['PUT'])
def update_emp(id):
    employee = Employee.query.get(id)

    if (employee == None):
        return jsonify({"Msg": "Employee not found with id " + id})
    
    print("----------------------------------------------------------")

    if (not request.json['emp_name']):
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")

    print("----------------------------------------------------------")

    emp_name = request.json['emp_name']
    emp_address = request.json['emp_address']
    designation = request.json['designation']
    dob = request.json['dob']
    telephone = request.json['telephone']
    email = request.json['email']
    dept_id = request.json['dept_id']

    employee.emp_name = emp_name
    employee.emp_address = emp_address
    employee.designation = designation
    employee.dob = dob
    employee.telephone = telephone
    employee.email = email
    employee.dept_id = dept_id

    db.session.commit()

    return emp_schema.jsonify(employee)

# Delete Employee record
@app.route("/employee/<id>", methods = ['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return emp_schema.jsonify(employee)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
 