# User Management service

## How to receive a simple request data from gateway
- create the `app/main.py` file

```
from fastapi import FastAPI,Depends, HTTPException, Response, Request
from typing import Dict
from fastapi import APIRouter,Depends,status,File,UploadFile,BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import (select,insert,update,delete,join,and_, or_ )
from app.validation.emp_m import EmpSchemaIn,EmpSchemaOut,Status422Response,Status400Response
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.model_functions.emp_m import save_new_empm,update_image_empm, get_emp_by_id
from app.exception.custom_exception import CustomException
from app.config.message import empm_message
from app.config.logconfig import loglogger
import os
from typing import Annotated
from app.validation.emp_m import EmpSchemaOut
from app.core.auth import getCurrentActiveEmp
from datetime import datetime
from app.config.jinja2_config import jinjatemplates
from weasyprint import HTML
from app.config.loadenv import envconst

app = FastAPI()

@app.post("/a1")
def a1(data: Dict):
    return {"message":"ddddd","data":data}


@app.post("/a2")
def a2(data: Dict):
    return {"status":True,"code":200,"data":[data["empm"]]}

```
