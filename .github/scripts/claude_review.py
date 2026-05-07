import json
import os
import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

with open("pr.diff", "r", encoding="utf-8") as f:
    diff = f.read()[:100000]

prompt = f"""
You are an expert .NET and SQL enterprise code reviewer.

Review the following pull request diff carefully.

Focus on:
- C# coding standards
- SOLID principles
- ASP.NET Core best practices
- SQL query optimization
- SQL injection vulnerabilities
- Stored procedure best practices
- Transaction handling
- EF Core optimization
- Async/await issues
- Exception handling
- Logging gaps
- Memory leaks
- Security vulnerabilities
- Maintainability
- Possible production bugs
- Code readability

Provide concise actionable recommendations with severity levels (Critical, High, Medium, Low).

PR Diff:

{diff}
"""

body = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 2000,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    json=body
)

print(response.text)

data = response.json()

comment = "No review generated."

if "content" in data:
    comment = data["content"][0]["text"]

with open("comment.txt", "w", encoding="utf-8") as f:
    f.write(comment)
