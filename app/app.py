import io
from enum import Enum
from pydantic import BaseModel

from fastapi import (
    FastAPI,
    Path,
    Body,
    Form,
    File,
    UploadFile,
    HTTPException,
    Cookie,
    Query,
    Header,
    Response,
    Request
)
import pandas as pd
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from utils.FakeData import generate_fake_data_faker, generate_fake_data_mimesis, generate_fake_data
from utils.LoggerSingleton import logger
from utils.ProcessingFile import load_file


class TipoUsuarioEnum(str, Enum):
    ESTANDARD = "estandard"
    ADMIN = "admin"

class TipoGeneradorEnum(str, Enum):
    FAKER = "faker"
    MIMESIS = "mimesis"


class TipoArchivoEnum(str, Enum):
    #PDF = "pdf"
    CSV = "csv"
    XLSX = "xlsx"


class Usuario(BaseModel):
    nombre: str
    edad: int


class Compania(BaseModel):
    nombre: str

app = FastAPI()

@app.get("/hola")
def hola():
    return {"mensaje": "Hola, Mundo!"}


@app.get("/hello/{nombre}")
def hola_nombre(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}


@app.get("/hello/{name}/{age}")
def hello_name_age(name: str, age: int):
    return {"message": f"Hello, {name}! You are {age} years old."}


@app.get("/users/{tipo}/{_id}")
async def get_user(tipo: TipoUsuarioEnum, _id: int):
    return {"tipo": tipo, "_id": _id}


@app.get("/users/{_id}")
async def get_user(_id: int = Path(..., ge=1, lt=100)):
    return {"_id": _id}


@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}


@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license": license}


@app.post("/usuarios")
async def create_user(name: str = Body(...), age: int = Body(...)):
    return {"name": name, "age": age}


@app.post("/usuarios/dos")
async def crear_usuario(usuario: Usuario):
    return usuario


@app.post("/usuarios/uno")
async def crear_usuario2(usuario: Usuario, compania: Compania):
    return {"usuarior": usuario, "compania": compania}


@app.post("/usuarios/tres")
async def create_user(usuario: Usuario, prioridad: int = Body(..., ge=1, le=3)):
    return {"usuario": usuario, "prioridad": prioridad}


@app.post("/usuarios/cuatro")
async def create_user4(nombre: str = Form(...), edad: int = Form(...)):
    return {"nombre": nombre, "edad": edad}


@app.post("/files")
async def upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/files2")
async def upload_file2(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content_type": file.content_type}


@app.post("/files3")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        for file in files
    ]


@app.post("/generate_data", response_class=FileResponse)
async def generate_data(tipo_generador: TipoGeneradorEnum, cantidad: int, nombre_archivo: str, tipo_archivo: TipoArchivoEnum = TipoArchivoEnum.CSV):
    print(f"Tipo generador: {tipo_generador.value}, Cantidad: {cantidad} , nombre: {nombre_archivo}, tipo archivo: {tipo_archivo.value}\nGenerando datos...")
    data = generate_fake_data(cantidad, tipo_generador.value)

    df = pd.DataFrame(data)
    if tipo_archivo.value == "csv":
        filename = f"{nombre_archivo}.csv"
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    if tipo_archivo.value == "xlsx":
        filename = f"{nombre_archivo}.xlsx"
        stream = io.BytesIO()
        df.to_excel(stream, index=False, engine="openpyxl")
        wb = Workbook()
        ws = wb.active

        # Convert DataFrame to worksheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

            # Adjust the width of the columns
            for column in ws.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Save workbook to stream
        wb.save(stream)
        stream.seek(0)
        wb.close()
        # Prepare the response
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response


@app.post("/process_data")
async def process_data(file: UploadFile = File(...)):

    try:
        data, md5_file, filename = load_file(file)
        return {"data": data, "md5_file": md5_file, "filename": filename}
    except Exception as e:
        logger.error(f"There was an error uploading the file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"There was an error uploading the file: {str(e)}")


@app.get("/get_headers1")
async def get_headers1(hello: str = Header(...)):
    return {"hello": hello}


@app.get("/get_headers2")
async def get_header2(user_agent: str = Header(...)):
    return {"user_agent": user_agent}


@app.get("/get_cookie")
async def get_cookie(hello: str | None = Cookie(None)):
    return {"hello": hello}


@app.get("/get_url")
async def get_request_object(request: Request):
    return {"path": request.url.path}

@app.get("/ger_request_params")
async def get_request_params(request: Request):
    return {"query_params": request.query_params, "request_body": request.body, "headers": request.headers, "cookies": request.cookies}