from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper
from langchain.tools import Tool, tool
from datetime import datetime

search = SerpAPIWrapper()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=400)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

@tool
def word_counter(text: str) -> str:
    """
    Count the number of words and characters in the input text.
    Returns a string summary with word count, character count, and average word length.
    """

    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_space = len(text.replace(" ", ""))
    avg_word_len = round(char_count / word_count, 2) if word_count>0 else 0

    return (
        f"Word count: {word_count}\n"
        f"Character count with spaces: {char_count}\n"
        f"Character count without spaces: {char_count_no_space}\n"
        f"Average word count: {avg_word_len}"
    )
