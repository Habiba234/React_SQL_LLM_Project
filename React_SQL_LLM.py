# from google import genai
# from google import genai

# client = genai.Client(api_key="AQ.Ab8RN6JZYmpzY7iGdtyTXID0U0qelf7Fhwsg7iHSajY76vEgKQ")

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Hello"
# )

# print(response.text)

import sqlite3
from google import genai
import re

# Connect Database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Gemini Client
client = genai.Client(
    api_key="AQ.Ab8RN6JZYmpzY7iGdtyTXID0U0qelf7Fhwsg7iHSajY76vEgKQ"
)

# System Prompt
SCHEMA = """
You are a SQL expert.

Database Schema:

Table: users
Columns:
- user_id INTEGER PRIMARY KEY
- full_name TEXT
- email TEXT

Table: products
Columns:
- product_id INTEGER PRIMARY KEY
- product_name TEXT
- unit_price REAL

Table: orders
Columns:
- order_id INTEGER PRIMARY KEY
- customer_ref INTEGER
- product_ref INTEGER
- quantity INTEGER

Table: reviews
Columns:
- review_id INTEGER PRIMARY KEY
- customer_ref INTEGER
- product_ref INTEGER
- rating INTEGER

Rules:
1. Generate only SQLite SQL.
2. Use only the tables and columns above.
3. Do not invent table names.
4. Do not invent column names.
5. Return only SQL wrapped in:

[SQL]
SELECT ...
[/SQL]
"""

# User Question
question = input("\nAsk your question: ")

# Prompt Gemini
prompt = f"""
{SCHEMA}

User Question:
{question}
"""

# Generate SQL using Gemini
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nGemini Response:")
    print(response.text)

except Exception as e:
    print("\nGemini API Error:")
    print(e)
    conn.close()
    exit()

# Extract SQL from response
match = re.search(
    r"\[SQL\](.*?)\[/SQL\]",
    response.text,
    re.DOTALL
)

if not match:
    print("\nNo SQL query found.")
    conn.close()
    exit()

sql_query = match.group(1).strip()

print("\nGenerated SQL:")
print(sql_query)

# Execute SQL query
try:
    cursor.execute(sql_query)

    rows = cursor.fetchall()

    print("\nOutput:")

    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found.")

except sqlite3.Error as e:
    print("\nSQL Error:")
    print(e)

# Close connection
conn.close()