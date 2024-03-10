---
lab:
    title: 'DB chatbot on structured data using Azure Open AI'
---

# Integrate Azure OpenAI into your Azure Database

## Provision an Azure OpenAI resource

If you don't already have one, provision an Azure OpenAI resource in your Azure subscription.

1. Sign into the **Azure portal** at `https://portal.azure.com`.
2. Create an **Azure OpenAI** resource with the following settings:
    - **Subscription**: *Select an Azure subscription that has been approved for access to the Azure OpenAI service*
    - **Resource group**: *Choose or create a resource group*
    - **Region**: *Make a **random** choice from any of the following regions*\*
        - Australia East
        - Canada East
        - East US
        - East US 2
        - France Central
        - Japan East
        - North Central US
        - Sweden Central
        - Switzerland North
        - UK South
    - **Name**: *A unique name of your choice*
    - **Pricing tier**: Standard S0

    > \* Azure OpenAI resources are constrained by regional quotas. The listed regions include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit in scenarios where you are sharing a subscription with other users. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

3. Wait for deployment to complete. Then go to the deployed Azure OpenAI resource in the Azure portal.

## Deploy a model

Azure OpenAI provides a web-based portal named **Azure OpenAI Studio**, that you can use to deploy, manage, and explore models. You'll start your exploration of Azure OpenAI by using Azure OpenAI Studio to deploy a model.

1. On the **Overview** page for your Azure OpenAI resource, use the **Go to Azure OpenAI Studio** button to open Azure OpenAI Studio in a new browser tab.
2. In Azure OpenAI Studio, on the **Deployments** page, view your existing model deployments. If you don't already have one, create a new deployment of the **gpt-35-turbo-16k** model with the following settings:
    - **Model**: gpt-35-turbo-16k *(if the 16k model isn't available, choose gpt-35-turbo)*
    - **Model version**: Auto-update to default
    - **Deployment name**: *A unique name of your choice. You'll use this name later in the lab.*
    - **Advanced options**
        - **Content filter**: Default
        - **Deployment type**: Standard
        - **Tokens per minute rate limit**: 5K\*
        - **Enable dynamic quota**: Enabled

    > \* A rate limit of 5,000 tokens per minute is more than adequate to complete this exercise while leaving capacity for other people using the same subscription.

## Provision a Azure SQL database
If you don't already have one, provision an Azure SQL Database resource in your Azure subscription.

1. Sign into the **Azure portal** at `https://portal.azure.com`.
2. Create an **Azure SQL** resource with the following settings:
- **Pricing** General Purpose - Serverless: Gen5, 1 vCore
- **region** same region as your OpenAI
- **Backup Storage Redundancy** Locally Redundant
- **Authentication** SQL authentication (take note of the sql admin user and password)
3. Configure the Network connectivity: 
- Go to the Azure SQL database you created, click the **server name** link on the Overview page
- On the SQL Server page, go to **Networking** under **Security**
- Click **Add your client IPV4 address** under the firewall rules
4. Optionally you can test the Azure SQL connectivity with your preferred SQL Client such as SSMS. 

## Prepare to develop an app in Visual Studio Code


1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a **Git: Clone** command to clone the `https://github.com/wenjuweng37/dbchat.git` repository to a local folder (it doesn't matter which folder).
3. When the repository has been cloned, open the folder in Visual Studio Code.



## Configure your application

Applications for Python have been provided. First, you'll complete some key parts of the application to enable using your Azure OpenAI resource.

1. Create a Python virtual env if you have not done so. To do this, you can Open the palette (SHIFT+CTRL+P) and run a **Python Create Environment** command, select **Venv Creates a `.venv` virtual environment for current workspace**, Then **enter the intepreter path**. You will see at the right bottom Visual Studio Code, a virtual environment is being created. It may take some time. Click the bell notification to check the status. 
2. In Visual Studio Code, in the **Explorer** pane, browse to the **Labfiles/01-dbchat-azure-openai** folder and expand the **Python** folder.
3. Right-click the **Python** folder containing your code files and open an integrated terminal. Then install the Azure OpenAI SDK package and other related packages by running the pip install shown below (note, if you run into SSL certificate error, you can add these options:  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org, for example, pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org openai==1.2.0):


    **Python**:

    ```
    pip install openai==1.2.0
    pip install SQLAlchemy
    pip install pyodbc
    pip install langchain
    pip install langchain-community
    pip install python-dotenv
    pip install pandas
    pip install langchain-openai
    ```

4. In the **Explorer** pane, in the **Python** folder, open the configuration file for your preferred language

    - **Python**: .env
    
5. Update the configuration values to include:
    - The  **endpoint** and a **key** from the Azure OpenAI resource you created (available on the **Keys and Endpoint** page for your Azure OpenAI resource in the Azure portal)
    - The **deployment name** you specified for your model deployment (available in the **Deployments** page in Azure OpenAI Studio).
    - The Azure SQL Environment variables
6. Save the configuration file.
7. This application can connect to your Azure SQL database that have already had schema and data populated in the dbo schema. But you can also upload csv files in the **files** folder. The program will load these files into the Azure SQL database (the file name becomes the table name).
    - Currently, we have Customer.csv, Product.csv, ProductCategory.csv, SalesOrderDetail.csv and SalesOrderHeader.csv
    - upload your additional csv files under files if needed. 

## Run the program
1. Run the program by typing: **python dbchat.py** in the Terminal
2. It will prompt you to choose below:
    - 1: How many customers have bike in company name?
    - 2: Which customer ID has the most accumulative due?
    - 3: Ask your own question
    - 'quit' to exit the program

if you choose to ask your own question, the program will take your question at the prompt. 


## Clean up

When you're done with your Azure OpenAI resource, remember to delete the deployment or the entire resource in the **Azure portal** at `https://portal.azure.com`.
