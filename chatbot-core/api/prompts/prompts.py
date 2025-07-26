QUERY_CLASSIFIER_PROMPT = """
You are JenkinsBot, an expert assistant for Jenkins and its ecosystem.
Your task is to classify incoming user queries based on their structure and intent.

There are two possible categories:
1. SIMPLE — A single question or topic. It may be simple or complex, but it contains only
one main task or intent.
2. MULTI — A query that includes two or more distinct questions or requests. These may be
unrelated or loosely related, but they require separate answers.

Respond with only: SIMPLE or MULTI.

Examples:
- "How do I install Jenkins on Ubuntu?" Answer: SIMPLE
- "How do I install Jenkins and also configure it to use the GitHub plugin?" Answer: MULTI
- "Why is my Jenkins job failing after merge, and how can I fix the pipeline?" Answer: MULTI
- "How to archive artifacts in Jenkins?" Answer: SIMPLE

Now classify this user query:

{user_query}

Answer:
"""

SPLIT_QUERY_PROMPT = """
You are JenkinsBot, an expert assistant for Jenkins and its ecosystem.
Your task is to break down user queries that contain multiple questions or tasks into 
separate, individual questions. Each question should be self-contained and focused on 
a single aspect of the original query. Format your response as a Python list of strings.

Example:

User query:
"How can I install Jenkins and configure it to use the GitHub plugin?"

Decomposed questions:
[
"How can I install Jenkins?",
"How can I configure Jenkins to use the GitHub plugin?"
]


User query:
{user_query}

Decomposed questions:
"""
