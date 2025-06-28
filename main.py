import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime
from pathlib import Path
import sys

load_dotenv()
SNIPPETS_FILE = "snippets.json"



def search_snippets(keyword):
    if not Path(SNIPPETS_FILE).exists():
        print("📂 No saved snippets yet.")
        return

    with open(SNIPPETS_FILE, "r", encoding="utf-8") as f:
        try:
            snippets = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Cannot read snippets.json — it may be corrupted.")
            return

    keyword = keyword.lower()
    matches = [
        s for s in snippets
        if keyword in s["task"].lower() or any(keyword in tag.lower() for tag in s.get("tags", []))
    ]

    if not matches:
        print("❌ No matching snippets found.")
        return

    print(f"🔍 Found {len(matches)} match(es):\n")
    for s in matches:
        print(f"[{s['id']}] Task: {s['task']}")
        print(f"    Tags: {', '.join(s['tags'])}")
        print(f"    Saved: {s['timestamp']}")
        print("    --- Snippet ---")
        print(s['snippet'])
        print("-" * 50)


def save_snippet(task, snippet, stack="default", tags=None):
    tags = tags or []

    # Load existing snippets (if file exists)
    if Path(SNIPPETS_FILE).exists():
        with open(SNIPPETS_FILE, "r", encoding="utf-8") as f:
            snippets = json.load(f)
    else:
        snippets = []

    # Generate new ID
    next_id = max([s["id"] for s in snippets], default=0) + 1

    # Build snippet entry
    entry = {
        "id": next_id,
        "task": task,
        "stack": stack,
        "tags": tags,
        "timestamp": datetime.now().isoformat(),
        "snippet": snippet.strip()
    }

    # Append and save
    snippets.append(entry)
    with open(SNIPPETS_FILE, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2)

    print(f"✅ Snippet saved as entry #{next_id}")

def ask_for_snippet(task):
    if "--ns" in task:
        system_prompt = (
            "You are a programming assistant that generates clean, reusable code snippets and templates. "
            "Use self-describing variable names and concise inline comments where helpful. "
            "Only include code directly relevant to the task unless explicitly asked for full context (like HTML scaffolding). "
            "If necessary, include a very short explanation before the code."
        )
    else:
        system_prompt = (
            "You are a programming assistant that generates clean, reusable code snippets and templates. "
            "Assume the user works primarily with jQuery, .NET (C#), and MySQL unless told otherwise. "
            "Use self-describing variable names and concise inline comments. "
            "Only include code directly relevant to the task unless the user asks for full context (like HTML scaffolding or complete files). "
            "Prefer jQuery for JavaScript tasks, C# for backend logic, and MySQL syntax for database queries. "
            "Include a short explanation if helpful, but keep it minimal."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Task: {task}"}
    ]

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.3
    )

    raw_output = response.choices[0].message.content

    # Strip markdown-style code blocks (```language ... ```)
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")  # remove all backticks
        lines = raw_output.splitlines()
        # Drop first line if it contains the language label (like "python")
        if lines and not lines[0].strip().startswith(("import", "function", "class", "$", "const")):
            lines = lines[1:]
        raw_output = "\n".join(lines).strip()

    return raw_output



def main():
    # Handle --search keyword
    if len(sys.argv) > 1 and sys.argv[1] == "--s":
        if len(sys.argv) < 3:
            print("⚠️ Please provide a keyword to search. Usage: --search <keyword>")
        else:
            search_snippets(sys.argv[2])
        return
    print("🛠️ Code Snippet Generator\n")
    while True:
        user_input = input("Enter a coding task ('q' to quit): ")
        if user_input.lower() in {"q", "quit", "exit"}:
            break
        print("\n🔧 Here's your snippet:\n")
        result = ask_for_snippet(user_input)
        print(result)
        print("\n" + "-" * 50 + "\n")
        save_input = input("💾 Save this snippet? (y/n): ").lower()
        if save_input == "y":
            tag_input = input("🔖 Enter tags (comma-separated): ").strip()
            tags = [tag.strip() for tag in tag_input.split(",")] if tag_input else []
            save_snippet(task=user_input, snippet=result, tags=tags)


if __name__ == "__main__":
    main()
