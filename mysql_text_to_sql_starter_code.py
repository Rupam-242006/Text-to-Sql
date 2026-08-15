import os
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Make sure your API key is set here!
os.environ["GROQ_API_KEY"] = "Your API Key"

def run_text_to_sql(user_question: str):
    """
    Takes a natural language question, generates MySQL, runs it, and returns the results.
    """
    
    # 1. Connect to the MySQL Database (Ensure your password is URL-encoded if it has special characters!)
    
    db_uri = "mysql+mysqlconnector://root:Rupam%4024@localhost:3306/ecommerce_db"
    db = SQLDatabase.from_uri(db_uri)

    # 2. Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # 3. Create the Text-to-SQL Chain
    template = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
    Return ONLY the raw SQL query. Do not wrap it in markdown backticks (```) and do not include any explanations.

    Here is the database schema:
    {schema}

    Question: {question}
    SQL Query:"""

    prompt = PromptTemplate.from_template(template)

    def get_schema(_):
        return db.get_table_info()

    chain = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

    # 4. Generate the SQL
    generated_sql = chain.invoke({"question": user_question}).strip()

    # Clean up formatting if necessary
    if generated_sql.startswith("```sql"):
        generated_sql = generated_sql[6:]
    elif generated_sql.startswith("```"):
        generated_sql = generated_sql[3:]
    if generated_sql.endswith("```"):
        generated_sql = generated_sql[:-3]
    generated_sql = generated_sql.strip()

    # 5. Execute the query
    try:
        # Run the query and get the results as a string representation of a list of tuples
        raw_results_str = db.run(generated_sql)
        
        # We need to parse this string back into a Python structure so the frontend can handle it easily.
        # Since db.run returns a string like "[('North America', Decimal('142500.00'))]", we'll do some basic cleanup.
        # In a production app, you might want to use SQLAlchemy directly to get structured rows.
        
        # For this prototype, we'll try to use `ast.literal_eval` safely if possible, or just pass the string if it's too complex.
        import ast
        import re
        
        # Basic cleanup: remove "Decimal(...)" wrappers from the string before parsing
        clean_results_str = re.sub(r"Decimal\('([^']+)'\)", r"\1", raw_results_str)
        
        try:
           parsed_results = ast.literal_eval(clean_results_str)
        except (ValueError, SyntaxError):
           # If parsing fails, fall back to the string
           parsed_results = raw_results_str
           
    except Exception as e:
        parsed_results = f"Error executing query: {e}"

    # Return a dictionary containing both the SQL and the data
    return {
        "sql_query": generated_sql,
        "data": parsed_results
    }

# This allows you to still test the script directly from the terminal
if __name__ == "__main__":
    question = "What was the total revenue grouped by region?"
    print(f"Testing terminal execution with question: '{question}'")
    result = run_text_to_sql(question)
    print(f"\nSQL: {result['sql_query']}")
    print(f"Data: {result['data']}")