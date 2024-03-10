import os  
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
from openai import AzureOpenAI

from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.chat_models import AzureChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_openai import AzureChatOpenAI


def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        sql_server_username = os.getenv("SQL_SERVER_USERNAME")
        sql_server_endpoint = os.getenv("SQL_SERVER_ENDPOINT")
        sql_server_password = os.getenv("SQL_SERVER_PASSWORD")
        sql_server_database = os.getenv("SQL_SERVER_DATABASE")

        db_config = {  
            'drivername': 'mssql+pyodbc',  
            'username': sql_server_username + '@' + sql_server_endpoint,  
            'password': sql_server_password,  
            'host': sql_server_endpoint,  
            'port': 1433,  
            'database': sql_server_database,  
            'query': {'driver': 'ODBC Driver 18 for SQL Server'} 
        }  
        #print(f"Database configuration: {db_config}")
        db_url = URL.create(**db_config)
        #db = SQLDatabase.from_uri(db_url)
        #df = pd.read_csv('../files/customer.csv')
        engine = create_engine(db_url)

        for root, dirs, files in os.walk('../files'):
            for file_name in files:
                if file_name.endswith(".csv"):
                    try:
                        # Read the CSV file into a DataFrame
                        file_path = os.path.join(root, file_name)
                        df = pd.read_csv(file_path)
                        df.to_sql(file_name.split(".")[0], engine, index=False)
                
                    except Exception as e:
                        print(f"{file_name}: {e}")

  

        db = SQLDatabase(engine=engine)
        result = db.run("SELECT count(*) FROM customer;")
        print(f"Total count in customer table: {result}")
        table_names = db.get_usable_table_names()
        print(f"These are the tables found in the database: {table_names}")



        #setting Azure OpenAI env variables

        os.environ["OPENAI_API_TYPE"] = "azure"
        os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
        os.environ["AZURE_OPENAI_ENDPOINT"] = azure_oai_endpoint
        os.environ["OPENAI_API_KEY"] = azure_oai_key

        llm = AzureChatOpenAI(deployment_name=azure_oai_deployment, temperature=0, max_tokens=3900)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )


        #ask sample question you want to ask
        #agent_executor.invoke("how many customers have bike in company name")

        while True:
            try:
                print('1: How many customers have bike in company name?\n' +
                    '2: Which customer ID has the most accumulative due? \n' +
                    '3: Ask your own question \n' +
                    '\'quit\' to exit the program\n')
                command = input('Enter a number:')
                if command == '1':
                    agent_executor.invoke("how many customers have bike in company name")
                elif command =='2':
                    agent_executor.invoke("Which customer ID has the most accumulative due")
                elif command =='3':
                    question = input('Enter your question:')
                    agent_executor.invoke(question)
                    
                elif command.lower() == 'quit':
                    print('Exiting program...')
                    break
                else :
                    print("Invalid input. Please try again.")
            except Exception as ex:
                print(ex)

         

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()


 


 
