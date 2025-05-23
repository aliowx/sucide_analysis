from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None



# Properties to receive via API on creation 

class UserCreate(UserBase):
    password: str 
    Username: str   
    
    
    
# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None
    
    
class UserInDBBase(UserBase):
    id: int | None = None
    model_config =  ConfigDict(from_attributes=True)
    
    

# Additional properties to return via API
class User(UserInDBBase):...



# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str 
    
    
    
    
class UserIn(BaseModel):
    email: EmailStr
    password: str
    
    
    
    
class LoginUser(BaseModel):
    email: EmailStr
    password: str