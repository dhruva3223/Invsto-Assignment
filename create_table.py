import psycopg2

# Database connection
conn = psycopg2.connect(
    database="invsto",
    user="me",
    password="test",
    host="localhost",
    port="5432")

# Cursor
cur = conn.cursor()

# Query to create a table
query1 = '''CREATE TABLE ticker_symbol(
    datetime DATE,
    close FLOAT,
    high FLOAT,
    low FLOAT,
    open FLOAT,
    volume INT,
    instrument  VARCHAR(8));'''

cur.execute(query1, conn)
print("Table created successfully")

# Query to Copy csv data to database
query2 = '''COPY ticker_symbol(datetime,close,high,low,open,volume,instrument)
FROM '/tmp/HINDALCO.csv'
DELIMITER ','
CSV HEADER;'''

cur.execute(query2)
conn.commit()
conn.close()
cur.close()
print("Data inserted successfully")