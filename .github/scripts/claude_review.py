import json
import os
import requests

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

with open("pr.diff", "r", encoding="utf-8") as f:
    diff = f.read()

# Prevent token overflow
diff = diff[:100000]

prompt = f"""
You are a strict senior .NET enterprise code reviewer.

Your task is to identify:
- Runtime exceptions
- Logical bugs
- Division by zero
- Null reference risks
- Async/await misuse
- Resource leaks
- SQL injection vulnerabilities
- Performance issues
- Security vulnerabilities
- Bad coding practices
- Violations of SOLID principles
- Production risks
- Maintainability issues

IMPORTANT:
- Be extremely critical.
- Treat this as production banking software.
- Identify even small runtime risks.
- Mention exact problematic code lines when possible.
- Assign severity:
  - Critical
  - High
  - Medium
  - Low

If you find issues, use this format:

[Severity] Issue Title

- Problem:
- Risk:
- Recommendation:

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

print("========== CLAUDE API RESPONSE ==========")
print("Status Code:", response.status_code)
print(response.text)

if response.status_code != 200:
    with open("comment.txt", "w", encoding="utf-8") as f:
        f.write(f"Claude API Error: {response.status_code}\n\n{response.text}")
    exit(1)

data = response.json()

comment = "No review generated."

try:
    if "content" in data:
        parts = []

        for item in data["content"]:
            if item.get("type") == "text":
                parts.append(item.get("text", ""))

        comment = "\n".join(parts)

except Exception as ex:
    comment = f"Error parsing Claude response: {str(ex)}"

with open("comment.txt", "w", encoding="utf-8") as f:
    f.write(comment)

print("========== FINAL COMMENT ==========")
print(comment)
