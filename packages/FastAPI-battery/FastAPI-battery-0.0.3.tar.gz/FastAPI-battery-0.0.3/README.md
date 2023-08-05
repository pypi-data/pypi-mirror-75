Usage:

from fastapi import FastAPI
from fastapi_battery import install_battery

app = FastAPI()
install_battery(app)




Required ENV:

DATABASE_URL
DATABASE_SCHEMA
SPYC_LOGIN_URL_ENTRY
SPYC_LOGIN_URL_VERIFY
FASTAPI_SECRET_KEY
CORS_ORIGINS
GMAIL_ACCOUNT
GMAIL_APP_PASSWORD
ENABLE_SQLTAP
