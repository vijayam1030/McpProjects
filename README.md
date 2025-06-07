
uv init
uv venv
 .venv\Scripts\activate
uv add "mcp[cli]"
uv run mcp dev server/weather.py
install node dure to npx 
uv run mcp install server/weather.py

# to add new llms eg: ollama2 from local or grok using api key

uv add langchain-ollama 
or
uv add langchain-groq
DONT use PIP
create .env file in root dir for the API_KEY



# to use as a mcp client using add the client.py
uv add mcp-use
uv run server/client.py


# to use