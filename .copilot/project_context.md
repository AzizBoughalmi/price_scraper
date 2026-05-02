# Project Context: PriceScout AI Agent

## Overview
PriceScout is an AI-powered agent designed to automate the monitoring of competitor pricing. It uses LLMs to "read" website content and extract pricing data dynamically, bypassing traditional fixed HTML rule scrapers.

## Technical Choices & Decisions
During the initial setup, we made several key architectural decisions for the MVP:
- **LLM Provider**: Selected **Gemini** (`gemini-2.5-flash` via `google-generativeai`) over GPT-4o-mini.
- **Orchestration**: Selected **Strands** library for agentic workflows instead of LangChain.
- **Web Discovery**: **Tavily Search API** to fetch product URLs from the web autonomously.
- **Web Scraping**: **Firecrawl SDK (v4)** to bypass JavaScript/bot-detection and parse HTML directly into Markdown.
- **Data Storage**: **JSON** file storage (selected over CSV for its flexibility with nested data).
- **Testing Approach**: Dual approach implementing both **Unit Tests** (`pytest` with mocks) and **CLI end-to-end testing** (`main.py`).
- **Environment Management**: **uv** for virtual environment management and fast pip installs.

## Development Phases

### Phase 1: Foundation & Setup (Completed)
- Created the core project structure (`src/`, `tests/`, `config/`).
- Initialized virtual environment using `uv`.
- Defined dependencies in `requirements.txt` and `.env` template.
- Implemented configuration management in `config/settings.py` using `python-dotenv`.

### Phase 2: Core Components (Completed)
- **Scraper (`src/scraper.py`)**: Built Firecrawl wrapper to extract Markdown from a given URL. Updated to Firecrawl v4 syntax (`.scrape()`).
- **LLM Parser (`src/llm_parser.py`)**: Built Gemini pipeline with a strictly enforced JSON extraction prompt to parse price, currency, status, and additional info.
- **Models & Storage (`src/models.py`, `src/storage.py`)**: Defined Pydantic models for data validation (`PriceResult`) and built JSON read/write handlers.
- **Agent Orchestrator (`src/agent.py`)**: Wired the Scraper and LLM Parser sequentially.
- **CLI (`main.py`)**: Built command-line interface for running the extraction pipeline against hardcoded URLs.
- **Unit Testing**: Implemented extensive mock tests for all these components in `tests/`.

### Phase 3: Agentic Integration & Tavily Search (Completed)
- **Search Tool (`src/search.py`)**: Integrated Tavily Search API to autonomously query e-commerce product links based on a product name and extract the probable competitor name.
- **Autonomous Mode**: Wired the Search Tool back into the `Agent` class and CLI (`main.py`). Modifying the `main.py` to allow fully autonomous extraction simply by providing `--product "ProductName"`.
- Tested the autonomous pipeline end-to-end, fetching live URLs and generating price intelligence dynamically.
- Committed all current code to local git and pushed to the remote GitHub repository (`master` branch).

### Phase 4: User Interface (Pending)
- Develop a Streamlit web-based dashboard for entering queries, viewing product price comparisons, and tracking price history.

## Current State
The project currently has a fully functional, headless (CLI) autonomous AI agent capable of searching the web for a given product and extracting its pricing from competitor sites into a structured JSON format. All code is tracked under version control and passing unit tests.