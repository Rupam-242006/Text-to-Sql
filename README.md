AI-Powered E-Commerce Data Assistant (Text-to-SQL)

An end-to-end AI data agent that allows non-technical users to query a MySQL database using natural language. Built with Python, LangChain, FastAPI, Groq (Llama 3), and Vanilla JS.
This project bridges the gap between natural language and complex database structures by dynamically translating plain English questions into syntactically correct, read-only MySQL queries, executing them, and rendering the results in a responsive ChatGPT-style web UI.

✨ Key Features

Natural Language Processing: Converts plain English into executed SQL queries using Llama 3.3.
Dynamic Schema Extraction: Automatically injects the live MySQL database schema into the LLM context, ensuring hallucination-free queries.
Secure Execution: Built to execute read-only queries safely using LangChain's SQLDatabase utilities.
FastAPI Backend: A lightweight, high-performance REST API bridging the LLM and the frontend.
Asynchronous Web UI: A responsive, interactive frontend built with Vanilla JS and Tailwind CSS, featuring loading states and dynamic table rendering.

🛠️ Tech Stack

Frontend: HTML5, Vanilla JavaScript, Tailwind CSS
Backend: Python, FastAPI, Uvicorn
AI / NLP: LangChain, Groq API (Llama-3.3-70b-versatile)
Database: MySQL 8.0, mysql-connector-python, SQLAlchemy.

🏗️ Architecture

graph TD
    subgraph Client-Side
        UI[Frontend Web UI<br>HTML / Tailwind / JS]
    end

    subgraph Backend Server
        API[FastAPI Server<br>main.py]
        Agent[LangChain SQL Agent]
    end

    subgraph External Services
        LLM[Groq API<br>Llama 3.3]
    end

    subgraph Database Layer
        DB[(MySQL Server<br>ecommerce_db)]
    end

    %% Data Flow
    UI -- "1. Asks Question (JSON)" --> API
    API -- "2. Invokes" --> Agent
    Agent -- "3. Pulls DB Schema" --> DB
    Agent -- "4. Sends Prompt + Schema" --> LLM
    LLM -- "5. Returns raw SQL String" --> Agent
    Agent -- "6. Executes SQL (Read-Only)" --> DB
    DB -- "7. Returns Data Rows" --> Agent
    Agent -- "8. Formats Response" --> API
    API -- "9. Returns Data & SQL (JSON)" --> UI

    classDef frontend fill:#dbeafe,stroke:#3b82f6,stroke-width:2px;
    classDef backend fill:#dcfce7,stroke:#22c55e,stroke-width:2px;
    classDef database fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
    classDef external fill:#f3e8ff,stroke:#a855f7,stroke-width:2px;
    
    class UI frontend;
    class API,Agent backend;
    class DB database;
    class LLM external;

🚀 Local Setup & Installation

1. Prerequisites

Python 3.10+
MySQL Server (Local instance running on port 3306)
A free Groq API Key

2. Clone the Repository

git clone https://github.com/yourusername/text-to-sql-assistant.git
cd text-to-sql-assistant

3. Set Up the Virtual Environment

python -m venv .venv
source .venv/Scripts/activate  # On Windows: .\.venv\Scripts\activate
pip install fastapi uvicorn pydantic langchain langchain-community langchain-groq pymysql mysql-connector-python sqlalchemy

4. Database Setup

Open load_csv_to_mysql.py and update the DB_CONFIG block with your local MySQL root password.
Ensure you have the ecommerce_sales_analytics_5000.csv file in your root directory.
Run the data loader script to create the database and populate it:
python load_csv_to_mysql.py

5. Configure the AI Backend

Open mysql_text_to_sql_starter_code.py and make two updates:
Add your Groq API Key: os.environ["GROQ_API_KEY"] = "your_key_here"
Update the db_uri with your MySQL password (remember to URL-encode special characters, e.g., @ becomes %40).

6. Run the Application

Start the FastAPI backend server:
python main.py

The server will start running at http://localhost:8000)
Finally, double-click the text_to_sql_ui.html file to open the frontend in your web browser.

💡 Example Queries to Try:

"Show me the top 5 product categories by quantity sold."
"What was our total revenue grouped by region?"
"How many orders were placed for Electronics?"