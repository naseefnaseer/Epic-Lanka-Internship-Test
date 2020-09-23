import uuid

from app.main import db
from app.main.model.department import Department

def create_dept(data):
    dept = Department.query.filter_by(dept = data['dept_name'].first())
    if not dept:
        new_dept = Department(
            id = str(uuid.uuid4()),
            dept_name = data['dept_name'],
            dept_address = data['dept_address']
        )
        

def get_all_department():
    return Department.query.all()

def get_department(id):
    return Department.query.

