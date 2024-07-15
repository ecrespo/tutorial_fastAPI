import hashlib
import io

import pandas as pd
from fastapi import UploadFile, HTTPException, File

from utils.LoggerSingleton import logger
from utils.ValidationCSVFile import validation_content


def load_file(file: UploadFile) -> pd.DataFrame:
    contents = file.file.read()
    # Validate that the file is a CSV or XLSX file
    if not file.filename.endswith((".csv", ".xlsx")):
        logger.info("El archivo debe ser un CSV o XLSX")
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV o XLSX")

    # Validate that the file is not empty
    if len(contents) == 0:
        logger.info("El archivo esta vacio")
        raise HTTPException(status_code=400, detail="El archivo esta vacio")

    filename = file.filename

    # Process the file based on its type
    if file.filename.endswith(".csv"):
        contents = contents.decode("utf-8")
        md5file = validation_content(contents, excel=False)
        data = io.StringIO(contents)
        df = pd.read_csv(data, sep=",")
    else:
        md5file = hashlib.md5(contents).hexdigest()
        data = io.BytesIO(contents)
        df = pd.read_excel(data, sheet_name=0)

    return df.to_dict(orient="records"), md5file, filename

