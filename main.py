from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from model import UserCreate, UserResponse, Token
from auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user_by_email,
    get_current_user
)
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
import database_model
from model import getEmployees, addEmployee, getCustomers, addCustomers, addContracts, addShifts, getShifts, getIncidents, addIncidents, getAttendance, addAttendance
from database_model import Users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://manpower-management-app-frontend.vercel.app"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

database_model.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()

user_dependency = Annotated[Users, Depends(get_current_user)]

@app.get("/")
def welcome():
    return "Welcome to Manpwer-app"

@app.get("/employees")
def fetch_employees(current_user: user_dependency, db: Session = Depends(get_db)): # here Session means "db is expected to be a SQLAlchemy Session object."
                    #Depends here means "Before calling this route, execute get_db() and inject whatever it yields into db."
    db_employees = db.query(database_model.Employees).all()
    return db_employees

@app.get("/employees/{id}")
def get_one_employee(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    emp = db.query(database_model.Employees).filter(database_model.Employees.emp_id==id).first()
    if emp:
        return emp
    return "Employee not found"

@app.post("/employees")
def add_employee(current_user: user_dependency,emp: addEmployee, db: Session = Depends(get_db)):
    db_emp = database_model.Employees(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.put("/employees/{id}")
def edit_employees(current_user: user_dependency,id: int, emp: addEmployee, db: Session = Depends(get_db)):
    db_emp = db.query(database_model.Employees).filter(database_model.Employees.emp_id==id).first()
    if db_emp:
        db_emp.name = emp.name
        db_emp.age = emp.age
        db_emp.mobile_number = emp.mobile_number
        db.commit()
        return db_emp
    return "Employee not found"

@app.delete("/employees/{id}")
def delete_employee(current_user: user_dependency,id: int, db: Session=Depends(get_db)):
    db_drop_emp = db.query(database_model.Employees).filter(database_model.Employees.emp_id==id).first()
    if db_drop_emp:
        db.delete(db_drop_emp)
        db.commit()
        return "Employee deleted successfully"
    return "Employee not found"

@app.get("/customers")
def get_customers(current_user: user_dependency,db: Session = Depends(get_db)):
    db_customers = db.query(database_model.Customers).all()
    return db_customers

@app.get("/customers/{id}")
def get_one_customer(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_cust = db.query(database_model.Customers).filter(database_model.Customers.customer_id==id).first()
    if db_cust:
        return db_cust
    return "Customer not found"

@app.delete("/customers/{id}")
def drop_customers(current_user: user_dependency,id: int,db: Session = Depends(get_db)):
    db_cust = db.query(database_model.Customers).filter(database_model.Customers.customer_id==id).first()
    if not db_cust:
        raise HTTPException(status_code=404, detail="Customer not found");
    try:
        db.delete(db_cust)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = 409,
            detail="Cannot delete customer: existing contracts reference this costumer."
        )
    return{"ok" : True}

@app.post("/customers")
def add_customers(current_user: user_dependency,cust: addCustomers,db: Session = Depends(get_db)):
    db_cust = database_model.Customers(**cust.model_dump())
    db.add(db_cust)
    db.commit()
    db.refresh(db_cust)
    return db_cust

@app.put("/customers/{cust_id}")
def edit_customers(current_user: user_dependency,cust_id: int, cust: addCustomers, db: Session = Depends(get_db)):
    db_cust = db.query(database_model.Customers).filter(database_model.Customers.customer_id==cust_id).first()
    if db_cust:
        db_cust.customer_name = cust.customer_name
        db_cust.address = cust.address
        db.commit()
        return db_cust
    return "Customer not found"

@app.get("/contracts")
def get_contracts(current_user: user_dependency,db: Session = Depends(get_db)):
    db_contracts = db.query(database_model.Contracts).all()
    return db_contracts

@app.get("/contracts/{id}")
def get_one_contract(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_cont = db.query(database_model.Contracts).filter(database_model.Contracts.contract_id==id).first()
    if db_cont:
        return db_cont
    return "Contract not found"

@app.post("/contracts")
def add_contracts(current_user: user_dependency,contract: addContracts,db: Session = Depends(get_db)):
    db_cont = database_model.Contracts(**contract.model_dump())
    db.add(db_cont)
    db.commit()
    db.refresh(db_cont)
    return db_cont

@app.put("/contracts/{cont_id}")
def edit_contracts(current_user: user_dependency,cont_id: int, cont: addContracts,db: Session = Depends(get_db)):
    db_cont = db.query(database_model.Contracts).filter(database_model.Contracts.contract_id==cont_id).first()
    if db_cont:
        db_cont.emp_id = cont.emp_id
        db_cont.customer_id = cont.customer_id
        db_cont.contract_type = cont.contract_type
        db_cont.monthly_salary = cont.monthly_salary
        db_cont.start_date = cont.start_date
        db_cont.end_date = cont.end_date
        db.commit()
        return db_cont
    return "Contract not found"

@app.delete("/contracts/{id}")
def delete_contracts(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_cont = db.query(database_model.Contracts).filter(database_model.Contracts.contract_id==id).first()
    if db_cont:
        db.delete(db_cont)
        db.commit()
        return "Contract deleted successfully"
    return "Contract not found"

@app.get("/shifts")
def get_shifts(current_user: user_dependency,db: Session = Depends(get_db)):
    db_shifts = db.query(database_model.Shifts).all()
    return db_shifts

@app.get("/shifts/{id}")
def get_one_shift(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_shft = db.query(database_model.Shifts).filter(database_model.Shifts.shift_id==id).first()
    if db_shft:
        return db_shft
    return "Shift not found"

@app.post("/shifts")
def add_shift(current_user: user_dependency,shift_info: addShifts, db: Session = Depends(get_db)):
    db_shift = database_model.Shifts(**shift_info.model_dump())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@app.put("/shifts/{shift_id}")
def edit_shift(current_user: user_dependency,shift_id: int, shift_info: addShifts, db: Session = Depends(get_db)):
    db_shift = db.query(database_model.Shifts).filter(database_model.Shifts.shift_id==shift_id).first()
    if db_shift:
        db_shift.contract_id = shift_info.contract_id
        db_shift.shift_date = shift_info.shift_date
        db_shift.start_time = shift_info.start_time
        db_shift.end_time = shift_info.end_time
        db_shift.shift_hours = shift_info.shift_hours
        db_shift.shift_pay = shift_info.shift_pay
        db.commit()
        return db_shift
    return "Shift not found"

@app.delete("/shifts/{shift_id}")
def delete_shift(current_user: user_dependency,shift_id: int, db: Session = Depends(get_db)):
    db_shift = db.query(database_model.Shifts).filter(database_model.Shifts.shift_id==shift_id).first()
    if db_shift:
        db.delete(db_shift)
        db.commit()
        return "Shift deleted successfully"
    return "Shift not found" 

@app.get("/attendance")
def get_attendance(current_user: user_dependency,db: Session = Depends(get_db)):
    db_attendance = db.query(database_model.Attendance).all()
    return db_attendance

@app.get("/attendance/{id}")
def get_one_attendance(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_att = db.query(database_model.Attendance).filter(database_model.Attendance.attendance_id==id).first()
    if db_att:
        return db_att
    return "Attendance not found"

@app.post("/attendance")
def add_attendance(current_user: user_dependency,att: addAttendance, db: Session = Depends(get_db)):
    db_att = database_model.Attendance(**att.model_dump())
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

@app.put("/attendance/{att_id}")
def edit_attendance(current_user: user_dependency,att_id: int, att_info: addAttendance, db: Session = Depends(get_db)):
    db_att = db.query(database_model.Attendance).filter(database_model.Attendance.attendance_id == att_id).first()
    if db_att:
        db_att.shift_id = att_info.shift_id
        db_att.check_in = att_info.check_in
        db_att.status = att_info.status
        db.commit()
        return db_att
    return "Attendance id not found" 

@app.delete("/attendance/{att_id}")
def delete_attendance(current_user: user_dependency,att_id: int, db: Session = Depends((get_db))):
    db_att = db.query(database_model.Attendance).filter(database_model.Attendance.attendance_id == att_id).first()
    if db_att:
        db.delete(db_att)
        db.commit()
        return "Attendance deleted successfully"
    return "Attendance ID not found"

@app.get("/incidents")
def get_incidents(current_user: user_dependency,db: Session = Depends(get_db)):
    db_incidents = db.query(database_model.Incidents).all()
    return db_incidents

@app.get("/incidents/{id}")
def get_one_incident(current_user: user_dependency,id: int, db: Session = Depends(get_db)):
    db_inc = db.query(database_model.Incidents).filter(database_model.Incidents.incident_id==id).first()
    if db_inc:
        return db_inc
    return "Incident not found"

@app.post("/incidents")
def add_incident(current_user: user_dependency,incident: addIncidents, db: Session = Depends(get_db)):
    db_inc = database_model.Incidents(**incident.model_dump())
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)
    return db_inc

@app.put("/incidents/{inc_id}")
def edit_incident(current_user: user_dependency,inc_id: int, inc: addIncidents, db: Session = Depends(get_db)):
    db_inc = db.query(database_model.Incidents).filter(database_model.Incidents.incident_id==inc_id).first()
    if db_inc:
        db_inc.emp_id = inc.emp_id
        db_inc.customer_id = inc.customer_id
        db_inc.description = inc.description
        db_inc.loss_amount = inc.loss_amount
        db_inc.incident_date = inc.incident_date
        db.commit()
        return db_inc
    return "Incident not found" 

@app.delete("/incidents/{inc_id}")
def delete_incident(current_user: user_dependency,inc_id: int, db:Session = Depends(get_db)):
    db_inc = db.query(database_model.Incidents).filter(database_model.Incidents.incident_id==inc_id).first()
    if db_inc:
        db.delete(db_inc)
        db.commit()
        return "Incident deleted successfully"
    return "Incident not found"

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = database_model.Users(
        email = user.email,
        hashed_password = hashed_password,
        full_name = user.full_name,
        role = user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model = Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}