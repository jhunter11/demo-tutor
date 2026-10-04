# Agent launch guide

Read START_HERE.md first. This folder is a deliberately small teaching demo.
Use Python 3.10+ and the standard library. Do not install the advanced AVP Tutor dependencies.
Run `python app.py --check`, then launch `python app.py --open`.
Use `python3` on macOS or Linux.

The user edits api-key.txt locally. Never print, quote, upload, or commit its contents.
Keep free_only true unless the user explicitly authorizes paid API access.
Do not replace a failing free model with a paid model.
Check a candidate free model against the current OpenRouter catalog and its reasoning capabilities.
The adapter performs the same check before requests.

Use one synthetic question to verify model inference when a key is present.
Distinguish a loaded key from successful model inference.
The model receives the question, recent chat, two draft skills, and the single exercise context.
The server supplies the problem and reference. The editor supplies the current student code and optional observed output.
The starter output comes from a manual trace. Do not claim the page executes code.
Do not load operator memory or private project files into its prompt.

Keep changes small. Validate backend changes with `python -m unittest -v`.
Use the browser to check layout and the question-and-answer flow after page changes.
Use `python package_demo.py` to prepare a key-free copy for sharing.
