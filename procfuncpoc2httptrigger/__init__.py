#Author: Karl Saycon 06/2/22
#Python HTTP Function App to call and get file from SQL Stored Proc

import pandas as pd
from sqlalchemy import create_engine
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from procfuncpoc2httptrigger import config as cfg
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    input = req.params.get('basehp')
    logging.info('connection is ok')
    logging.info(cfg.engine_azure.table_names())

    if not input:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input = req_body.get('basehp')

    if input:
        parameterIn = input
        logging.info(type(parameterIn))

        try:

            query = ("exec getPokemonBaseHP @basehp=" + "'" + parameterIn + "'")
            poke_df = pd.read_sql_query(query,cfg.connection)
            logging.info(poke_df)
            pokecsv = poke_df.to_csv(index=False, encoding = "utf-8")
            logging.info(pokecsv)

            connection_string= cfg.GetBlobKeySecret
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client_main = blob_service_client.get_container_client('blobpokecsv')
            try:
                container_client_main.create_container()
                container_client_main.get_container_properties()
            except Exception as ex:
                logging.info("Container already exists")
            file = "sqlproc_pokemondata_basehp_"+input+"-" + cfg.stringtime + ".csv"
            blobmain = container_client_main.get_blob_client(file)
            blobmain.upload_blob(pokecsv)
            logging.info(f"Blob trigger executed!")
            
            cfg.connection.close()
        finally:
            cfg.connection.close()
        return func.HttpResponse(f"Pokemon Base HP = {input}. Data Frame Loaded to CSV. Uploaded the file to the blob storage successfully!")

    else:
        return func.HttpResponse(
             "Trigger Requests Parameter based on the Pokemon's Base HP e.g <api>?basehp=<value> for the Pokemon.",
             status_code=200
        )
