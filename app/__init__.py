from flask import Flask
import pymysql
from pymysql.constants import CLIENT
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL connection
conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_NAME'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    client_flag=CLIENT.MULTI_STATEMENTS     # allows execution of multiple sql statements (for schema)
)

# Execute schema.sql
schema = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
with open(schema, 'r') as f:
    schema_script = f.read()

with conn.cursor() as cursor:
    cursor.execute(schema_script)

# Import routes
from . import routes
