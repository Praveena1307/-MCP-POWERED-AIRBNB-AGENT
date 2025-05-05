# MCP-Powered Airbnb Agent

A conversational travel booking assistant that uses Google's Gemini 2.0 model with Machine Comprehension Protocol (MCP) to process natural language booking requests.

## Features

- Natural language booking request processing
- Asynchronous agent architecture with multi-turn conversations
- Tool-calling capabilities for real-time interaction with booking services
- User-friendly Streamlit interface
- Transparent tool execution reporting

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Praveena1307/-MCP-POWERED-AIRBNB-AGENT.git
   cd mcp-airbnb-agent
   ```

2. Install dependencies:
   ```
   pip install streamlit python-dotenv google-generativeai mcp-client asyncio
   ```

3. Install Node.js dependencies:
   ```
   npm install -g @openbnb/mcp-server-airbnb
   ```

4. Create a `.env` file with your API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Enter your booking request in natural language, for example:
   ```
   I want to book an apartment in Paris for 2 nights. 03/28 - 03/30
   ```

3. Click "Run Agent" to process your request

4. View the agent's actions and final booking recommendation

## How It Works

1. The user enters a natural language booking request
2. The Gemini 2.0 model processes the request
3. The agent uses MCP tools to search for and filter listings
4. Results are displayed to the user in a conversational format
5. The entire process is executed asynchronously for responsiveness

## Requirements

- Python 3.8+
- Node.js and npm
- Google Gemini API key
- Internet connection for API access

## License

MIT

## Acknowledgments

- Google for the Gemini 2.0 model
- The MCP team for the Machine Comprehension Protocol
- Streamlit for the web interface framework
