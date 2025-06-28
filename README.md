# 🛠️ CodeSnippetAgent

CodeSnippetAgent is a lightweight, terminal-based AI assistant that helps you generate reusable, stack-specific code snippets using the OpenAI API.

It’s designed to streamline repetitive developer tasks — like writing AJAX requests, or SQL templates — with context-aware output tailored to your personal tech stack.

---

## 💻 Tech Stack

This tool assumes and prioritizes the following technologies by default:

- **jQuery** for JavaScript-related tasks
- **C# / .NET** for backend logic
- **MySQL** for SQL templates and CTEs

You can override this context with flags like `--ns` to request neutral or alternate output.

---

## 🚀 Features

- Prompt AI for code snippets via natural language
- Save snippets to a local `snippets.json` file
- Add searchable tags to each saved snippet
- Search and retrieve past snippets by keyword

---

## 📦 Setup

1. **Clone the repo and install dependencies:**
  git clone  https://github.com/bq3573/CodeSnippetAgent.git
  cd CodeSnippetAgentClean
  pip install -r requirements.txt

2. **Create a .env file in the project root:**
   OPENAI_API_KEY=your-api-key-here
3. **Create an empty snippets.json file in the root:**
   "[]" - should be all that's in there to get started
## 🧠 Usage
  python main.py
## 🔍 Extra Commands (Search Saved Snippets)
  python main.py --s ajax
