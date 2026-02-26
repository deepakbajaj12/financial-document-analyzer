## Importing libraries and files
import os
from dotenv import load_dotenv

load_dotenv()

# BUG FIX: Import `tool` from crewai.tools (not langchain_core.tools).
# The langchain_core version creates StructuredTool objects which CrewAI's
# Agent pydantic model rejects with:
#   "Input should be a valid dictionary or instance of BaseTool"
from crewai.tools import tool

# BUG FIX: Import SerperDevTool from crewai_tools instead of using a dummy stub.
# The original code had `from crewai_tools import SerperDevTool, tool` which was
# commented out. We import SerperDevTool separately and handle import failure gracefully.
try:
    from crewai_tools import SerperDevTool
except ImportError:
    class SerperDevTool:
        """Fallback stub if crewai_tools is not installed."""
        def __init__(self):
            pass
        def run(self, query):
            return f"Search results for: {query} (SerperDevTool unavailable)"

from pypdf import PdfReader

## Creating search tool
search_tool = SerperDevTool()


## Creating custom PDF reader tool
class FinancialDocumentTool:
    @tool("Read Financial Document")
    def read_data_tool(file_path: str) -> str:
        """Read and extract text from a financial PDF document at the given file path."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                # BUG FIX: was "\\n" (literal backslash-n) instead of "\n" (newline)
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"


## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("Process investment data")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """Analyze financial document data for investment insights."""
        processed_data = financial_document_data
        return f"Processed investment data: {processed_data[:100]}..."


## Creating Risk Assessment Tool
class RiskTool:
    @tool("Create risk assessment")
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """Assess risks based on financial document data."""
        return f"Risk assessment based on data: {financial_document_data[:100]}..."
