from fastapi import APIRouter,Depends,status,File,UploadFile,BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import (select,insert,update,delete,join,and_, or_ )
from app.validation.emp_m import EmpSchemaIn,EmpSchemaOut,Status422Response,Status400Response,InEmpDetail
from fastapi.responses import JSONResponse, ORJSONResponse
from app.database.model_functions.emp_m import (save_new_empm,update_image_empm, get_emp_by_id, get_data_by_email)
from app.exception.custom_exception import CustomException
from app.config.message import empm_message
from app.config.logconfig import loglogger
import os
from typing import Annotated
from app.validation.emp_m import EmpSchemaOut
#from app.core.auth import getCurrentActiveEmp
from datetime import datetime
from app.config.jinja2_config import jinjatemplates
from weasyprint import HTML
from app.config.loadenv import envconst
from typing import Dict
# from app.config.fastapi_mail_config import send_email, mailconf

router = APIRouter()

@router.post("/a3")
def a3(data: Dict):
    return {"message":"uuuuuuuuuu","data":data}

@router.post("/get-emp-details",name="getempdetails")
def getEmpDetails(emp:InEmpDetail, db:Session = Depends(get_db)):
    try:
        empObj = get_data_by_email(db=db, email=emp.email)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        datadict = {}
        datadict['id'] = empObj.id
        datadict['emp_name'] = empObj.emp_name
        datadict['email'] = empObj.email
        datadict['status'] = empObj.status
        datadict['mobile'] = empObj.mobile
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":empm_message.SAVE_SUCCESS,
            "data":datalist
        }
        response_data = EmpSchemaOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":"Type:"+str(type(e))+", Message:"+str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response

@router.post(
    "/emp-m-save",
    response_model=EmpSchemaOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response}
    },
    name="empmsave"
    )
def empSave(empm: EmpSchemaIn, db:Session = Depends(get_db)):
    # I keep duplicate_email_checker function outside of try block because duplicate_email_checker function raise an exception. If duplicate_email_checker keep inside function then Exception class will except it because Exception is parrent class.
    # Main point is raise keyword use the outside of try block.
    EmpSchemaIn.duplicate_email_checker(db,empm.email)
    try:
        insertedData = save_new_empm(db=db, empm=empm)
        http_status_code = status.HTTP_200_OK
        datalist = list()
        
        datadict = {}
        datadict['id'] = insertedData.id
        datadict['emp_name'] = insertedData.emp_name
        datadict['email'] = insertedData.email
        datadict['status'] = insertedData.status
        datadict['mobile'] = insertedData.mobile
        datalist.append(datadict)
        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":empm_message.SAVE_SUCCESS,
            "data":datalist
        }
        response_data = EmpSchemaOut(**response_dict) 
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.dict()))
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":"Type:"+str(type(e))+", Message:"+str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response
