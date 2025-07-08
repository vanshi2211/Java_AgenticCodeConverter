import streamlit as st
import datetime
import os
import io
from dotenv import load_dotenv
from contextlib import redirect_stdout

from langchain_groq import ChatGroq
from agents import get_agents
from tasks import get_review_task, get_validation_task, get_refactor_task
from crew import get_crew

load_dotenv()

# file paths. creates if not there
os.makedirs("legacy_code", exist_ok=True)
os.makedirs("docs", exist_ok=True)
os.makedirs("new_code", exist_ok=True)

legacy_path = "legacy_code/OldCode.java"
doc_path_agent1 = "docs/code_docs_agent1.md"
doc_path_agent2 = "docs/code_docs_agent2.md"
new_code_path = "new_code/RefactoredCode.java"

# page layout
st.set_page_config(page_title="Agentic Java Refactor with CrewAI", layout="wide")
st.title(" Agentic Java Refactorer (CrewAI + Groq/Llama3)")

# mode selector
mode = st.radio("Choose mode", ["Refactor Legacy Code", "Generate Docs from Modern Code"], horizontal=True)

# LLM 
if 'llm' not in st.session_state:
    try:
        # st.session_state.llm =  ChatGroq(
            # api_key=os.getenv("GROQ_API_KEY")
            # model="gorq/llama2-70b", 
            # temperature=0
        # ) 

        st.session_state.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="groq/llama-3.1-8b-instant",
            temperature=0
        )
    except Exception as e:
        st.error(f"Language Model API issue. Error: {e}")
        st.stop()

llm = st.session_state.llm

# create page layout with two columns
main_col, log_col = st.columns([0.7, 0.3])

with main_col:
    uploaded_file = st.file_uploader("Upload your Java code", type="java")

    if uploaded_file:
        # file_content = uploaded_file.read().decode("utf-8") 
        file_content = uploaded_file.getvalue().decode("utf-8")
        with open(legacy_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        st.success("✅ Java code uploaded successfully.")
        # st.text(file_content)  
        # print("File uploaded at", datetime.datetime.now())
        st.code(file_content, language="java")

        if st.button("🚀 Start Process", type="primary"):
            # print("reached A") 
            # print("Step 1 complete at", datetime.datetime.now())
            st.write("---")

            # import time 
            # time.sleep(2) 

            # get agents
            agent1, agent2, agent3 = get_agents(llm)

            # AGENT 1: REVIEW
            with st.status("Agent 1: Generating documentation...", expanded=True) as status:
                try:
                    task1 = get_review_task(agent1, file_content)
                    # crew1 = get_crew(agent1,task1)
                    crew1 = get_crew([agent1], [task1])

                    # result1 = crew1.kick()
                    f1 = io.StringIO()
                    with redirect_stdout(f1):
                        result1 = crew1.kickoff()
                    logs1 = f1.getvalue()
                    # output1 = result1.result
                    output1 = str(result1) 

                    with open(doc_path_agent1, 'w', encoding="utf-8") as f:
                        f.write(output1)

                    st.markdown("###  Agent 1 Output: Generated Documentation")
                    st.markdown(output1)

                    status.update(label=" Agent 1: Documentation generated!", state="complete")
                    st.session_state.logs1 = logs1
                except Exception as e:
                    st.session_state.logs1 = f"Agent 1 Error: {e}"
                    status.update(label=f" Agent 1 Error: {e}", state="error")
                    st.stop()

            st.write("---")

            if mode == "Refactor Legacy Code":
                # AGENT 2: VALIDATION
                with st.status("Agent 2: Improving documentation...", expanded=True) as status:
                    try:
                        task2 = get_validation_task(agent2, output1)
                        crew2 = get_crew([agent2], [task2])

                        f2 = io.StringIO()
                        with redirect_stdout(f2):
                            result2 = crew2.kickoff()
                        logs2 = f2.getvalue()
                        # output2 = result2.output  
                        output2 = str(result2)

                        with open(doc_path_agent2, 'w', encoding="utf-8") as f:
                            f.write(output2)

                        st.markdown("### Agent 2 Output: Improved Documentation")
                        st.markdown(output2)

                        status.update(label="Agent 2: Documentation improved!", state="complete")
                        st.session_state.logs2 = logs2
                    except Exception as e:
                        st.session_state.logs2 = f"Agent 2 Error: {e}"
                        status.update(label=f"Agent 2 Error: {e}", state="error")
                        st.stop()

                st.write("---")

                # AGENT 3: REFACTOR
                with st.status("Agent 3: Generating modern Java code...", expanded=True) as status:
                    try:
                        task3 = get_refactor_task(agent3, output2)
                        crew3 = get_crew([agent3], [task3])

                        f3 = io.StringIO()
                        with redirect_stdout(f3):
                            result3 = crew3.kickoff()
                        logs3 = f3.getvalue()
                        # output3 = result3.result.strip() 
                        output3 = str(result3).strip().replace("```java", "").replace("```", "").strip()

                        with open(new_code_path, 'w', encoding="utf-8") as f:
                            f.write(output3)

                        st.markdown("### Agent 3 Output: Refactored Java Code")
                        # st.markdown(f"```java
                        # {output3}
                        # ```")  
                        # print("Final here at", datetime.datetime.now())
                        st.code(output3, language="java")

                        status.update(label="Agent 3: Modern Java code generated!", state="complete")
                        st.session_state.logs3 = logs3

                        st.download_button(
                            label="⬇️ Download Refactored Java Code",
                            data=output3,
                            file_name="RefactoredCode.java",
                            mime="text/x-java-source",
                        )
                    except Exception as e:
                        st.session_state.logs3 = f"Agent 3 Error: {e}"
                        status.update(label=f"Agent 3 Error: {e}", state="error")
                        st.stop()

with log_col:
    st.markdown("## Verbose Logs")
    with st.expander("Agent 1 Logs", expanded=False):
        st.text(st.session_state.get("logs1", " Waiting for Agent 1..."))
    if mode == "Refactor Legacy Code":
        with st.expander("Agent 2 Logs", expanded=False):
            st.text(st.session_state.get("logs2", " Waiting for Agent 2..."))
        with st.expander("Agent 3 Logs", expanded=False):
            st.text(st.session_state.get("logs3", " Waiting for Agent 3..."))
