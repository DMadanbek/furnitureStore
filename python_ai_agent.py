import os
from dotenv import load_dotenv
import sys 
import io 

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent 
from langchain_google_genai import ChatGoogleGenerativeAI 

GOOGLE_API_KEY = "AIzaSyDalpWk98iD1Tpap3QLZs4ZaHejS2tfB30"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY 

load_dotenv()

ai_agent = os.getenv("AI_AGENT_DB")
ai_agent_password = os.getenv("AI_AGENT_DB_PASSWORD")
ai_agent_host = os.getenv("AI_AGENT_DB_HOST")
ai_agent_db_name = os.getenv("AI_AGENT_DB_NAME")
ai_agent_port = os.getenv("AI_AGENT_DB_PORT")

if not all([ai_agent, ai_agent_password, ai_agent_db_name]):
    print("ВНИМАНИЕ: Не найдены переменные окружения. Используются тестовые значения.")
    ai_agent = "python_user"
    ai_agent_password = "strong_password"
    ai_agent_host = "localhost"
    ai_agent_db_name = "furniture_store"
    ai_agent_port = "3306"

DB_URI = f"mysql+mysqlconnector://{ai_agent}:{ai_agent_password}@{ai_agent_host}:{ai_agent_port}/{ai_agent_db_name}"
try:
    db = SQLDatabase.from_uri(DB_URI)
    print(f"Подключение к БД '{ai_agent_db_name}' успешно.")
except Exception as e:
    print(f"ОШИБКА ПОДКЛЮЧЕНИЯ К БД: {e}")
    exit()

try:
    if sys.stdin.encoding != 'utf-8':
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


system_prompt_template = """
You are a specialized SQL-based AI Analyst agent for the '{db_name}' database.
Your primary role is to analyze structured data and generate valuable insights for the user.

Given an input question:
1. First, you MUST check the database schema, including tables and if any pre-existing analytical VIEWs. If there are no VIEWs, you create it yourself and add it to the MySQL VIEWs OBLIGATORY.
2. Formulate a syntactically correct {dialect} query.
3. Execute the query, then analyze the results and provide a clear, concise final answer with SQL Query you used in a separated space (e.g SQL Query -- ...).

RULES:
- Always limit your query to at most {top_k} results, unless the user explicitly requests more.
- Always ask for only the necessary columns. DO NOT use SELECT *.
- You MUST utilize pre-defined analytical VIEWs when the question relates to complex insights (e.g., profitability, top-rated genres).
- **CRITICAL:** You are an analysis agent only. And I gave you the role of DBDesigner in my database. So you can ONLY WORK WITHIN THE BOUNDS OF THIS ROLE. DO NOT attempt to modify the database schema, add/drop tables, or alter data in any way
- Double-check your SQL query logic before execution. If an error occurs, rewrite the query and try again.
- Your final answer must be a summary of the data, not just the raw query result.
"""

system_prompt = system_prompt_template.format(
    db_name=ai_agent_db_name,
    dialect=db.dialect,
    top_k=5,
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="zero-shot-react-description",
    prefix=system_prompt,
    verbose=True,
    handle_parsing_errors=True
)


print("-" * 50)
print("AI Analyst Agent готов. Введите ваш вопрос:")

try:
    input_question = input("Ваш вопрос: ")
except UnicodeDecodeError:
    print("\n[ВНИМАНИЕ: Ошибка кодировки. Пожалуйста, введите запрос на латинице (английскими буквами).]")
    try:
        input_question = sys.stdin.readline().strip().encode('latin-1').decode('utf-8', 'ignore')
    except Exception:
        input_question = ""
        
print("-" * 50)

if not input_question:
    if 'UnicodeDecodeError' in str(sys.last_value):
        print("Ввод не прочитан из-за системной ошибки кодировки. Пожалуйста, перезапустите скрипт и введите вопрос на латинице.")
    sys.exit()

print(f"Анализируется запрос: {input_question}\n")

try:
    response = agent.invoke({"input": input_question})
    
    print("\n--- ОТВЕТ АГЕНТА ---")
    print(response['output'])

except Exception as e:
    print(f"Произошла ошибка во время выполнения агента.")
    print(f"Подробности: {e}")
