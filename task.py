## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool


## Task 1: Verify the uploaded document
# PROMPT FIX: Added step-by-step instructions and clearer expected output format.
verification = Task(
    description=(
        "Verify if the document at {file_path} is a valid financial report. "
        "Steps:\n"
        "1. Read the document using the Financial Document Tool.\n"
        "2. Check for key sections like balance sheet, income statement, cash flow statement.\n"
        "3. Verify the document contains numerical financial data.\n"
        "4. Confirm the document is not corrupt or unreadable."
    ),
    expected_output=(
        "A verification report confirming whether the document is a valid financial report. "
        "Include: document type identified, key sections found, and a pass/fail verdict."
    ),
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Task 2: Analyze the financial document
analyze_financial_document = Task(
    description=(
        "Analyze the financial document at {file_path} to answer the user's query: {query}. "
        "Steps:\n"
        "1. Use the Financial Document Tool to read the full document content.\n"
        "2. Extract key financial metrics (revenue, profit, margins, growth rates).\n"
        "3. Identify trends and significant changes year-over-year.\n"
        "4. Provide a direct answer to the user's specific query."
    ),
    expected_output=(
        "A detailed analysis answering the user's query based on the financial document. "
        "Include specific numbers, percentages, and data points from the document."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Task 3: Investment analysis
# BUG FIX: Added missing "and" — was "at {file_path} provide" → "at {file_path} and provide"
investment_analysis = Task(
    description=(
        "Analyze the financial document at {file_path} and provide investment recommendations. "
        "Focus on financial ratios, market trends, and potential opportunities. "
        "User query: {query}\n"
        "Steps:\n"
        "1. Review the financial analysis from the previous task.\n"
        "2. Calculate or identify key investment ratios (P/E, ROE, debt-to-equity, etc.).\n"
        "3. Assess growth potential and market positioning.\n"
        "4. Provide specific, actionable investment recommendations."
    ),
    expected_output=(
        "A comprehensive investment analysis including: "
        "key financial ratios, stock recommendation (if applicable), "
        "strategic recommendations, and clear rationale based on the document data."
    ),
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Task 4: Risk assessment
risk_assessment = Task(
    description=(
        "Assess the risks associated with the financial entity described in the document at {file_path}. "
        "Consider market volatility, regulatory risks, and financial stability. "
        "User query: {query}\n"
        "Steps:\n"
        "1. Review the financial data and previous analyses.\n"
        "2. Identify market risks (competition, market conditions, sector trends).\n"
        "3. Evaluate financial risks (debt levels, cash flow, liquidity).\n"
        "4. Consider regulatory and operational risks.\n"
        "5. Provide a risk rating and mitigation strategies."
    ),
    expected_output=(
        "A detailed risk assessment report including: "
        "identified risks categorized by type (market, financial, regulatory, operational), "
        "risk severity ratings, potential impact, and recommended mitigation strategies."
    ),
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)
