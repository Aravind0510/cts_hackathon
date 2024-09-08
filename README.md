
# MedScan: AI-Driven Healthcare Data Management

## Overview
**MedScan**  is an advanced application designed to manage patient health records stored in complex JSON formats. It integrates with Snowflake for efficient data handling and utilizes the LangChain model to convert natural language inputs into SQL queries. MedScan provides an intuitive dashboard and admin panel to facilitate seamless data interaction and management.splay the results in an intuitive interface. This tool simplifies complex database operations, making data retrieval and analysis more accessible.

## Problem Statement
### Complexity of Patient Health Records
-**Challenge**: Patient records are often complex, stored in intricate JSON file formats.
Impact: Managing and interpreting this data is challenging and time-consuming.
### Challenges in Data Retrieval
-**Challenge**: Retrieving specific, context-dependent information is difficult, leading to frequent misinterpretations.
### Impact on Decision-Making
-**Challenge**: Inadequate systems result in delayed decision-making and compromised data accuracy, affecting patient care quality.
### Scalability Issues
-**Challenge**: Current systems struggle to scale efficiently with growing healthcare data volumes, leading to bottlenecks in data processing and retrieval.

## Our Solution

MedScan offers a comprehensive solution to these challenges:

-**AI-Driven Data Management**: Utilizes AI to handle complex JSON patient records.
-**Integration with Snowflake**: Ensures efficient data processing and management.
-**LangChain Model**: Converts natural language inputs into SQL queries, providing contextualized data retrieval.
-**User-Friendly Dashboard**: Offers an intuitive interface for seamless data interaction.
-**Admin Panel:** Allows real-time updates of patient and doctor records to the connected database.


## Features
- **Natural Language Interface**: Interact with the system using natural language queries.
- **Schema Extraction & Prompting**: Guides query generation and provides examples for efficient query formation.
- **Conversation MemoryQuery Generation & Execution**:  Automatically generates and executes SQL queries based on user input.
- **Contextual Responses**: Provides responses from the database with contextual relevance.
- -**Dynamic Dashboard**: Visualizes data in an interactive and continuously updated format.
-**Admin Panel**: Facilitates adding and updating patient and doctor records.

## Installation

1. **Install Required Dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt

   ```

## Usage
### 1. Running the Application
Start the application with:
```bash
streamlit main2.py
```
TThis will launch the Streamlit interface where you can interact with MedScan.

### 2.. Using MedScan
-**Home:** Introduction and overview of MedScan’s capabilities.
-**AI-SQL Interface:** Enter natural language queries to interact with the AI SQL Assistant.
-**Schema Viewer:** View schema details to understand the database structure.
-**Admin Panel:** Manage and update patient and doctor records.

### 3. Starting a New Chat
- Click the "New Chat" button to reset the session and start a fresh interaction.

### 4. Downloading Results
- You can download the results of your queries directly from the interface.

## Code Structure
- **`main2.py`**: The main script that runs the Streamlit application and manages user interactions.
- **`sql_execution.py`**: Handles execution of SQL queries against the database.
- **`trialprompt.py`**: Contains AI prompt templates used for guiding the AI's responses.
- **`schemex1.py`**: Manages the schema information for database tables.

## Environment Variables
Before running the application, ensure you set up your environment variables correctly:
- **`OPENAI_API_KEY`**: Set your OpenAI API key in the `main2.py` file.

# MY Contribution

## Chat Interface
-Developed natural language input handling and prompt management.
-Created templates for efficient query generation and contextualization.

## Query Generation and Execution
-Implemented automatic SQL query generation and execution based on user input.

##Admin Panel with Dynamic Dashboard
-Developed the frontend interface for interaction and data visualization.
-Implemented backend logic for data retrieval and updates.
-Ensured synchronization between the backend and database for real-time updates.

