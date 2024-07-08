import mysql.connector as sql
import pandas as pd
from sqlalchemy import create_engine
import configparser
import urllib.parse


config = configparser.ConfigParser()

config.read('db.ini')

username = config['main']['username']
password = config['main']['password']

# Load your dataframe
df = pd.read_csv('pokemon.csv')

# Connect to MySQL
db = sql.connect(
    host="localhost",
    user=username,
    passwd=password,
)



cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon")

# Function to map pandas dtypes to MySQL data types
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    else:
        return "VARCHAR(255)"

# Generate the CREATE TABLE statement
table_name = "pokemon"
create_table_query = f"CREATE TABLE IF NOT EXISTS pokemon.{table_name} (id INT AUTO_INCREMENT PRIMARY KEY, "

for column in df.columns:
    col_type = map_dtype(df[column].dtype)
    create_table_query += f"{column} {col_type}, "

# Remove the last comma and space, then add closing parenthesis
create_table_query = create_table_query.rstrip(", ") + ");"

cursor.execute(create_table_query)


url_friendly_psswrd = urllib.parse.quote_plus(password)
engine = create_engine(f'mysql+mysqlconnector://{username}:{url_friendly_psswrd}@localhost:3306/pokemon')

# Write the dataframe to the MySQL table
df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

db.commit()

# Close the connection
cursor.close()
db.close()
