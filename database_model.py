from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Numeric, Date, Time, DateTime, Text

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True,nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(50), default="employee")
    is_active = Column(Integer, default=1)

class Employees(Base):
    __tablename__ = "employees"
    emp_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    mobile_number = Column(String(10))

class Customers(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    address = Column(Text)

class Contracts(Base):
    __tablename__ = "contracts"
    contract_id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    contract_type = Column(String(30))
    monthly_salary = Column(Numeric(10,2))
    start_date = Column(Date)
    end_date = Column(Date)

class Shifts(Base):
    __tablename__ = 'shifts'
    shift_id = Column(Integer, primary_key = True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"))
    shift_date = Column(Date)
    start_time= Column(Time)
    end_time = Column(Time)
    shift_hours = Column(Integer)
    shift_pay = Column(Numeric(10,2))

class Attendance(Base):
    __tablename__ = "attendance"
    attendance_id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("shifts.shift_id"))
    check_in = Column(DateTime)
    status = Column(String)

class Incidents(Base):
    __tablename__ = "incidents"
    incident_id = Column(Integer, primary_key = True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    description = Column(Text)
    loss_amount = Column(Numeric(10,2))
    incident_date = Column(Date)


