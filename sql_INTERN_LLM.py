# Import libraries
import sqlite3

# # Connect to database
conn=sqlite3.connect("Customer.db")
cursors=conn.cursor()

# # Creating Table
# cursors.execute("""
# Create table if not exists USERS(
#     user_id Integer,
#     name text,
#     city text
# )
# """)

# cursors.execute("""
# Create table if not exists PRODUCTS(
#     product_id integer,
#     product_name text,
#     price integer
# )
# """)

# cursors.execute("""
# create table if not exists ORDERS(
#     order_id integer,
#     customer_ref integer,
#     product_ref integer,
#     quantity integer
# )
# """)

# print("Table created successfully")

# # Insert values

# cursors.execute("Insert into USERS values(1,'Ali','Delhi')")
# cursors.execute("Insert into USERS values(2,'sara','Mumbai') ")

# cursors.execute("Insert into PRODUCTS values(101,'Mobile',50000)")
# cursors.execute("Insert into PRODUCTS values(102,'Laptop',70000)")

# cursors.execute("Insert into ORDERS values(1,1,101,5)")
# cursors.execute("Insert into ORDERS values(2,2,102,4)")

# print("Data Inserted successfully")

# data=cursors.execute('''select * from USERS''')
# for row in data:
#     print(row)
    
# conn.commit()
# conn.close()

# # SYSTEM PROMPT

system_prompt="""
You are an SQL expert.

# Database schema:

USERS(user_id,name,city)
PRODUCTS(product_id,product_name,price)
ORDERS(order_id,customer_ref,product_ref,quantity)

Rules:
1. Generate only SQLite SQL.
2. Use only these tables and columns.
3.Return SQL inside [SQL] and [/SQL].
4.Correct the query if error occurs.
"""
print(system_prompt)

#user question                    # converting english word into SQL query
user_question='show all product name and prices'
print(user_question)

# LLM Response
response="""
[SQL]
select product_name,price
from products;
[/SQL]
"""
print(response)


# Extract SQL                 # re--- regular expression
import re
match=re.search(r"\[SQL\](.*?)\[/SQL\]",response,re.DOTALL)

sql_query=match.group(1).strip()
print(sql_query)

# Execute SQL
cursors.execute(sql_query)
result=cursors.fetchall()
print(result)

# Error handling       # no product_cost so use try and except
response="""
[SQL]
select product_cost from products;      
[/SQL]
"""
print(response)

# no such product_cost is exist

# Try and except
print(sql_query)
try:
    cursors.execute(sql_query)
    result=cursors.fetchall()
    print(result)
    
except sqlite3.Error as e:
    print(e)


response="""
[SQL]
select price from products;
[/SQL]"""
print(response)


# The price of product is printed using fetchall
cursors.execute("SELECT price FROM products")
print(cursors.fetchall())



