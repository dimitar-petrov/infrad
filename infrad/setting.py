import os
from decouple import AutoConfig

config = AutoConfig(os.getcwd())

EPC = ( config("EPC_SERVER_HOST", cast=str), config("EPC_SERVER_PORT", cast=int) )
