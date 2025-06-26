from crewai import Task

def get_review_task(agent, code):
    return Task(
        description=f"""
            Generate detailed documentation in Markdown for the following Java code. 
            Analyze the code, explain its functionality, identify potential limitations, 
            and point out any outdated Java patterns.

            ---
            CODE:
            ```java
            {code}
            ```
        """,
        expected_output="A comprehensive Markdown document containing the code explanation, a list of limitations, and a summary of outdated patterns. Also give important points if any",
        agent=agent
    )

def get_validation_task(agent, documentation):
    return Task(
        description=f"""
            Review, validate, and improve the following documentation. 
            Ensure it is accurate, complete, and follows modern technical documentation standards. 
            Add any missing details and clarify complex points.

            ---
            DOCUMENTATION:
            {documentation}
        """,
        expected_output="An improved and complete version of the Java code documentation in Markdown format. The final output should be ready for a developer to use for refactoring.",
        agent=agent
    )

def get_refactor_task(agent, documentation):
    return Task(
        description=f"""
            Generate clean, modern Java 17+ code based on the final documentation provided. 
            The code should be complete, runnable, and enclosed in a single markdown code block.
            Do not include any explanations or text outside the ```java ... ``` block.

            ---
            FINAL DOCUMENTATION:
            {documentation}
        """,
        expected_output="A single, complete, and clean Java code block containing the modern refactored code.",
        agent=agent
    )
