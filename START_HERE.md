# Start the tutor demo

This is the small API-and-skill MVP. It runs as one local chatbot page.
Requirements: Python 3.10 or newer, an internet connection, and an OpenRouter API key.
No package installation, Node, local model, or GPU is required.

## Set the key

Open `api-key.txt` in this folder.
Replace the placeholder with your OpenRouter API key, then save the file.
Paste only the key. Do not add quotes or a variable name.
The server reads this file when you send a question, so key changes need no restart.

Get a key from [OpenRouter Keys](https://openrouter.ai/settings/keys).
The shipped configuration uses `nvidia/nemotron-3-super-120b-a12b:free` and enforces zero-price routing.
Free access can have rate limits. There is no automatic paid fallback.

## Launch

On Windows, double-click `Start Demo.cmd`, or run:

```powershell
python app.py --open
```

On macOS or Linux, run:

```sh
python3 app.py --open
```

Open the folder in a terminal before running the command.
The page opens at `http://127.0.0.1:8780/`.
Press Ctrl+C in the terminal to stop the server.
If that port is busy, use `python app.py --port 8781 --open`.
Use `python3` instead of `python` on macOS or Linux.

## Give this to an agent

Copy this request into Codex or Claude Code after opening the extracted folder:

> Read START_HERE.md and AGENTS.md in this folder. Check setup with python app.py --check, then launch python app.py --open. Use python3 on macOS or Linux. Keep free_only true. If api-key.txt contains a placeholder, have the user paste their key locally. Never print the key. Check the page and one synthetic tutor reply. Report setup, model, and observed results separately. Do not send private project files to the model.

Useful checks:

```sh
python app.py --check
python -m unittest -v
python app.py --verify-model
```

The first two commands make no model calls.
`--verify-model` makes one request and reports the answer and token use.
The default configuration rejects a model with a listed price before sending the tutor request.

## Present the MVP

The page shows one search problem, its reference algorithm, and an editable copy of the student code.
The sample input is `values = [4, 7, 2]` and `target = 7`. The expected output is `1`.
Expand "Reference algorithm" if it is closed.
Select "Why does my loop stop early?" and send the supplied question.
Both code versions and the sample context accompany each question.
Ask a follow-up such as "What does return do here?"
Select "Give me a hint" to show the second draft skill.

Edit "Your code" to remove the early `return -1` inside the loop.
Ask what the edited code returns. The next request includes the new code.
Editing clears the old observed output. Enter the output you saw if you have run the code elsewhere.
The supplied starter output comes from a manual trace. This page does not run code.
Use "Reset example" to restore the starter and clear the conversation.

Say: "This MVP uses a hosted API for the chat and a first draft of a tutoring skill."
It shows the first integration milestone of the AVP tutoring work.
Full AVP execution, retrieval, and visualizer integration belong to later milestones.

## Share

Send the prepared `api-tutor-mvp.zip`, or create a fresh bundle with:

```sh
python package_demo.py
```

The packager includes a placeholder key file and excludes your real key, logs, and local test artifacts.
The recipient pastes the key you provide, or uses their own key.
The ZIP contains a placeholder. Provide a working key separately through your chosen method.
