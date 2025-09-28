### SUMMARIZE PROMPT ###
SUMMARIZE_PROMPT_SYSTEM = """
You are a helpful study assistant that summarizes text.
You will be provided with search results to summarize.
"""

SUMMARIZE_PROMPT_USER = """
# TASK:
Summarize the following text in a concise manner, focusing on the key points and main ideas. 
Use clear and simple language that can be understood by a high school student.

# Search Results:
{search_results}
"""