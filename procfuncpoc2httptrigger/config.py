#Author: Karl Saycon 06/2/22
#Python HTTP Function App to call and get file from SQL Stored Proc

from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import datetime
import re
from sqlalchemy import create_engine
import urllib

#declare osenv path for local runs
TENANT_ID = env.get("AZURE_TENANT_ID", "")
CLIENT_ID = env.get("AZURE_CLIENT_ID", "")
CLIENT_SECRET = env.get("AZURE_CLIENT_SECRET", "")
KEYVAULT_NAME = env.get("AZURE_KEYVAULT_NAME", "")
KEYSECRET = env.get("KEYSECRET_NAME", "")
KEYSECRET2 = env.get("KEYSECRET_NAME2", "")
KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"
#initiatesecretkeyviacredentials
_credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
#initiatesecretkeyviasecrentclient
_sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
#getsallsecretkeys
GetBlobKeySecret = _sc.get_secret(KEYSECRET).value
GetBlobKeySecret2 = _sc.get_secret(KEYSECRET2).value

driverstr = urllib.parse.quote_plus(GetBlobKeySecret2)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(driverstr)

engine_azure = create_engine(conn_str,echo=True)
connection = engine_azure.raw_connection()

stringtime = re.sub("[-\.: ]","",str(datetime.datetime.now())) #getsthedatetimefo