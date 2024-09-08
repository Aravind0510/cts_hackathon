import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
#from langchain.chat_models import ChatOpenAI
from json_execution import execute_mysql_query
from updated_prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE1
from langchain_google_genai import ChatGoogleGenerativeAI



# Set Streamlit page configuration
st.set_page_config(page_title="JSON Querying", layout="wide")

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "sql_queries" not in st.session_state:
    st.session_state["sql_queries"] = []
if "input_history" not in st.session_state:
    st.session_state["input_history"] = []
if "output_tables" not in st.session_state:
    st.session_state["output_tables"] = []
if "con_history" not in st.session_state:
    st.session_state["con_history"] = []
if "sql_statement" not in st.session_state:
    st.session_state["sql_statement"] = []
if 'chart_buffer' not in st.session_state:
    st.session_state['chart_buffer'] = None
if "sidebar_selection" not in st.session_state:
    st.session_state["sidebar_selection"] = "JSON Querying"

history = st.session_state["past"]

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + str(st.session_state["generated"][i]))
    session = [(user, bot) for user, bot in zip(st.session_state["past"], st.session_state["generated"])]
    st.session_state["stored_session"].append(session)
    # Reset the session state
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state["output_tables"] = []
    st.session_state["input_history"] = []
    st.session_state["sql_queries"] = []
    st.session_state["con_history"] = []
    st.session_state["sql_statement"] = []
    st.session_state.entity_memory.buffer.clear()


os.environ['GOOGLE_API_KEY'] ="AIzaSyBEeIGxpdKR7rAg6ALiLD9pgYNkVJOyt2A"



llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
# Correct the model name to "gpt-4"
#llm = OpenAI(temperature=0, openai_api_key="sk-UST-29KaVbUsoPoE6H_1ROgnlM4XEVRlIhkhcknV73T3BlbkFJJwVMCCU6ChweOO_fuHoCHYcq8pTpD1mN4paDHaFvAA", model="gpt-3.5-turbo-instruct", verbose=False)

if "entity_memory" not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm)

conversation_chain = ConversationChain(llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE1, verbose=True, memory=st.session_state.entity_memory)

st.markdown(
    """
<style>
button.st-emotion-cache-s48dsx{
    align-content: center;
    height: auto;
    width: auto;
    padding-left: 70px !important;
    padding-right: 70px !important;
}

div.stButton > button:first-child {
        background-color: #2596BE;  /* Blue color */
        color: white;
        font-size: 20px;
</style>
""",
    unsafe_allow_html=True,
)




with st.sidebar:
    selected = option_menu("Chat Interface", ["JSON Querying"], 
        icons=['database'], default_index=0, orientation="vertical",
        styles={
            "container": {"width": "290px", "padding": "5px", "float": "left", "background-color": "#FFFFFF", "font-family": "'Trebuchet MS',Helvetica,sans-serif"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"color": "white", "font-size": "20px", "margin": "0px", "hover-color": "red"},
            "nav-link-selected": {"background-color": "#2596BE"}
            
        })
    
st.session_state.sidebar_selection = selected

s = f"<center><span style='font-size:55px; color:#2596BE'>Patient Data </span><span style='font-size:55px; color:rgb(0,0,0)'>Retrieval Assistant</span></center>"
st.markdown(s, unsafe_allow_html=True)
st.divider()

if st.session_state.sidebar_selection == "JSON Querying":
    st.sidebar.button("New Chat", on_click=new_chat)

    user_input = st.chat_input("Your AI assistant is here! Ask me anything ..")

    user_icon = "👤"
    bot_icon = "🤖"
    
    download_data = []
     
    if user_input:
        # Generate SQL query
        sql_query = conversation_chain.run(input=user_input)
        
        if sql_query:
            st.session_state.sql_statement.append(sql_query)
            
            print(f"Generated SQL Query: {sql_query}")
        
            input_with_sql = f"{user_input} {sql_query}" if sql_query else user_input
            output = conversation_chain.run(input_with_sql)
            
            st.session_state.sql_statement.append(sql_query)

            # +Execute the SQL query
            if "SELECT" in sql_query or "SHOW" in sql_query:
                df = execute_mysql_query(sql_query)

                if df.empty:
                    # Handle empty DataFrame
                    
                    diagnosis = conversation_chain.run(input=f"The query returned no results. Could you help diagnose why?")
                    print(diagnosis)
                    st.session_state.generated.append(diagnosis)
                    st.session_state.output_tables.append(diagnosis)
                    st.session_state.past.append(user_input)
                    if isinstance(df, pd.DataFrame):
                        st.session_state.input_history.append(user_input)
                        st.session_state.output_tables.append(diagnosis)
                else:
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(df)
                    st.session_state.output_tables.append(df)
                    
                    if isinstance(df, pd.DataFrame):
                        st.session_state.input_history.append(user_input)
                        st.session_state.output_tables.append(df)
            else:
                st.session_state.past.append(user_input)
                st.session_state.generated.append(sql_query)
                if isinstance(sql_query, type(sql_query)):
                        st.session_state.con_history.append(sql_query)
                        st.session_state.input_history.append(user_input)
        else:
            # If no SQL query is generated, inform the user
            st.session_state.generated.append("No SQL query was generated. Please try rephrasing your question.")
        
        st.markdown(
                    """
                        <style>        
                    .chat-row {
                        display: flex;
                        margin: 5px;
                        width: 100%;
                    }

                    .row-reverse {
                         display: flex;
                         flex-direction: row-reverse;
                         margin: 5px;
                    }
                    .row-reverse1 {
                         display: flex;
                         margin: 5px;
                    }
                    .chat-bubble {
                        font-family: "Source Sans Pro", sans-serif, "Segoe UI", "Roboto", sans-serif;
                        border: 1px solid transparent;
                        padding: 5px 10px;
                        margin: 0px 7px;
                        max-width: 70%;  /* Ensures both bubbles adjust size */
                        word-wrap: break-word;
                        display:flex;
                    }

                    .ai-bubble {
                        background: rgb(240, 242, 246);
                        border-radius: 10px;
                        display:flex;
                        margin: 5px;
                    }

                    .human-bubble {
                        background: linear-gradient(135deg, rgb(0, 178, 255) 0%, rgb(0, 106, 255) 100%); 
                        color: white;
                        border-radius: 20px;
                       
                    }

                    .chat-icon {
                        border-radius: 5px;
                    }
                    
                    </style>
        """,
            unsafe_allow_html=True,
        )
                
        # Display conversation history
        for input_, output, sql_query1 in zip(st.session_state.input_history, st.session_state.generated, st.session_state.sql_statement):
           st.markdown(f"<div class='chat-row row-reverse'>{user_icon}<b> <span style='color:#2596BE'>Your Input</span></b></div>", unsafe_allow_html=True)
           with st.container():
                st.markdown(f"<div class='row-reverse'><div class='chat-bubble human-bubble '>{input_}</div></div>", unsafe_allow_html=True)
                
                st.write("")
                st.markdown(f"<div class='chat-row'>{bot_icon}<b>  <span style='color:#2596BE'>AI Response:</span></b></div>", unsafe_allow_html=True)

                with st.container():
                    if isinstance(output, pd.DataFrame):
                        tab_titles = ["Output", "SQL Query"]
                        tabs = st.tabs(tab_titles)
                        with tabs[0]:
                            st.markdown("<span style='color:#2596BE'>Output:</span>", unsafe_allow_html=True)
                            st.write(output)
                        with tabs[1]:
                            st.markdown("<span style='color:#2596BE'>Generated SQL Query:</span>", unsafe_allow_html=True)
                            st.code(sql_query1)
                    else:
                        st.markdown(f"<div class='row-reverse1'><div class='chat-bubble ai-bubble'>{output}</div></div>", unsafe_allow_html=True)

    # Prepare data for download
    download_str = "\n".join(map(str, download_data))
    if download_str:
        st.download_button("Download", download_str)

    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label=f"Conversation-Session:{i}"):
            st.write(sublist)

    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:
        if st.sidebar.checkbox("Clear-all"):
            del st.session_state.stored_session