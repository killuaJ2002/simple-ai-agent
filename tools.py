from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper
from langchain.tools import Tool
from datetime import datetime

search = SerpAPIWrapper()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
