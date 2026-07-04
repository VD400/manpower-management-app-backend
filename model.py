from pydantic import BaseModel, EmailStr
from decimal import Decimal
from datetime import date, time, datetime
from typing import Optional

class getEmployees(BaseModel):
    emp_id: int
    name: str
    age: Optional[int] = None
    mobile_number: Optional[str] = None

class addEmployee(BaseModel):
    name: str
    age: Optional[int] = None
    mobile_number: Optional[str] = None

class getCustomers(BaseModel):
    customer_id: int
    customer_name: Optional[str] = None
    address: Optional[str] = None

class addCustomers(BaseModel):
    customer_name: Optional[str] = None
    address: Optional[str] = None

class getContracts(BaseModel):
    contract_id: int
    emp_id: Optional[int] = None
    customer_id: Optional[int] = None
    contract_type: Optional[str] = None
    monthly_salary: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class addContracts(BaseModel):
    emp_id: Optional[int] = None
    customer_id: Optional[int] = None
    contract_type: Optional[str] = None
    monthly_salary: Optional[Decimal  ] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class getShifts(BaseModel):
    shift_id: int
    contract_id: Optional[int] = None
    shift_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    shift_hours: Optional[int] = None
    shift_pay: Optional[Decimal] = None

class addShifts(BaseModel):
    contract_id: Optional[int] = None
    shift_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    shift_hours: Optional[int] = None
    shift_pay: Optional[Decimal] = None

class getAttendance(BaseModel):
    attendance_id: int
    shift_id: Optional[int] = None
    check_in: Optional[datetime] = None
    status: Optional[str] = None

class addAttendance(BaseModel):
    shift_id: Optional[int] = None
    check_in: Optional[datetime] = None
    status: Optional[str] = None

class getIncidents(BaseModel):
    incident_id: int
    emp_id: Optional[int] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    loss_amount: Optional[Decimal] = None
    incident_date: Optional[date] = None

class addIncidents(BaseModel):
    emp_id: Optional[int] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    loss_amount: Optional[Decimal] = None
    incident_date: Optional[date] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "employee"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True
        