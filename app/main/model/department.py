from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = "Department"

    id = db.Column(db.Integer, primary_key = True, autoIncrement = True )
    dept_name = db.Column(db.String(50), nullable = False)
    dept-address = db.Column(db.String(255), nullable = False)





