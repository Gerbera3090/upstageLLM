import os
import oracledb
from .config import get_setting
settings = get_setting()
# username=os.environ["DB_USER"]
# password=os.environ["DB_PASSWORD"]
# dsn=os.environ["DSN"]
username=settings.DB_USER
password=settings.DB_PASSWORD
dsn=settings.DSN



con = oracledb.connect(user=username, password=password, dsn=dsn)

try: 
    conn23c = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Connection successful!", conn23c.version)
except Exception as e:
    print("Connection failed!")
