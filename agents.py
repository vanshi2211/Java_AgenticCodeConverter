from crewai import Agent

def get_agents(llm):
    reviewer = Agent(
        role="Java Code Reviewer",
        goal="Review legacy Java code and generate clear documentation in Markdown format, highlighting any limitations or outdated patterns. Also give important points if any",
        backstory="An expert Java developer responsible for reviewing legacy code and creating detailed, easy-to-understand documentation for other developers to remake into modern code.",
        llm=llm,
        verbose=True
        
    )

    validator = Agent(
        role="Documentation Validator",
        goal="Validate and improve Java documentation to ensure it is accurate, complete, and according to modern standards.",
        backstory="A senior JAVA software engineer, who ensures that all technical documentation is clear, detailed and professional.",
        llm=llm,
        verbose=True
    )

    developer = Agent(
        role="Modern Java Developer",
        goal="Write modern, clean, and efficient Java 17+ code based on validated documentation.",
        backstory="An experienced developer who specializes in remaking legacy code into modern Java applications, focusing on best practices, readability, and performance.",
        llm=llm,
        verbose=True
    )
    
    return reviewer, validator, developer
