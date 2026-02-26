try:
    from crewai_tools import tool
    print("Found 'tool' in crewai_tools")
except ImportError:
    print("Not found 'tool' in crewai_tools")

try:
    from crewai import tool
    print("Found 'tool' in crewai")
except ImportError:
    print("Not found 'tool' in crewai")

try:
    from langchain.tools import tool
    print("Found 'tool' in langchain.tools")
except ImportError:
    print("Not found 'tool' in langchain.tools")
