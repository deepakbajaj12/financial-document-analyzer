## Importing libraries and files
import os
from dotenv import load_dotenv

load_dotenv()

from crewai import Agent, LLM

from tools import search_tool, FinancialDocumentTool

### Loading LLM
# BUG FIX: Use crewai.LLM instead of langchain_openai.ChatOpenAI / ChatGoogleGenerativeAI.
# Modern CrewAI (v1.x) has its own LLM wrapper that handles providers uniformly.
# The original code used langchain wrappers which caused compatibility issues with
# CrewAI's Agent pydantic model.
llm = None
if os.getenv("GOOGLE_API_KEY"):
    llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.5)
elif os.getenv("OPENAI_API_KEY"):
    llm = LLM(model="openai/gpt-3.5-turbo", temperature=0.7)
else:
    # Default fallback — will fail at runtime if no keys are set,
    # but at least won't crash on import.
    llm = LLM(model="openai/gpt-3.5-turbo", temperature=0.7)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and provide accurate investment insights based on query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        # BUG FIX: Added spaces between concatenated string literals.
        # Original had "strategies." "You always" → "strategies.You always"
        "You are an experienced financial analyst with a strong background "
        "in market analysis and investment strategies. "
        "You always base your recommendations on data and facts from the document. "
        "You verify your findings and provide a balanced view of risks and opportunities."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True,
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and relevance of the uploaded document.",
    verbose=True,
    memory=True,
    backstory=(
        # BUG FIX: Added spaces between concatenated string literals.
        "You are a meticulous document verifier. "
        "Your job is to ensure that the document provided is indeed a financial report "
        "and contains relevant information. "
        "You check for key financial indicators and document structure."
    ),
    llm=llm,
    tools=[FinancialDocumentTool.read_data_tool],
    max_iter=3,
    max_rpm=10,
    allow_delegation=True,
)

# Creating an investment advisor agent
investment_advisor = Agent(
    role="Senior Investment Advisor",
    goal="Provide sound investment advice based on verified financial analysis.",
    verbose=True,
    memory=True,
    backstory=(
        # BUG FIX: Added spaces between concatenated string literals.
        "You are a certified financial planner with over 15 years of experience. "
        "You always prioritize the client's financial data and risk tolerance. "
        "You recommend diversified portfolios and evidence-based investment strategies."
    ),
    llm=llm,
    tools=[FinancialDocumentTool.read_data_tool],
    max_iter=3,
    max_rpm=10,
    allow_delegation=False,
)

# Creating a risk assessment specialist agent
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify and evaluate potential risks associated with the investment.",
    verbose=True,
    memory=True,
    backstory=(
        # BUG FIX: Added spaces between concatenated string literals.
        "You are a risk assessment expert with a focus on financial markets. "
        "You analyze market volatility, regulatory changes, and company-specific risks. "
        "You provide a comprehensive risk profile to ensure informed decision-making."
    ),
    llm=llm,
    tools=[FinancialDocumentTool.read_data_tool],
    max_iter=3,
    max_rpm=10,
    allow_delegation=False,
)
