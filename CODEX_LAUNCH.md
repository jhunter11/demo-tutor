# Launch demo-tutor with Codex

Give this document to a local Codex task on the computer where you want to use the demo.
Codex can get the app from these links. No second attachment is needed.

- Repository: [jhunter11/demo-tutor](https://github.com/jhunter11/demo-tutor)
- Demo ZIP: [v0.1.0 download](https://github.com/jhunter11/demo-tutor/releases/download/v0.1.0/demo-tutor.zip)
- Setup guide: [START_HERE.md](https://github.com/jhunter11/demo-tutor/blob/main/START_HERE.md)

Requirements: Python 3.10 or newer, an internet connection, and an OpenRouter API key.
Paste the key locally when Codex asks. This document contains no key.

## Request for Codex

> Get the tutor demo from the repository or ZIP linked in this document. Complete the setup and check the running page. Keep the server running for me. Use the free API configuration. Ask me to paste a key locally only if the key file contains a placeholder. Never print the key. Verify one real tutor response and give me the local page URL.

## Launch task

1. Use an existing demo folder, clone the repository, or download and extract the linked ZIP.
2. Read `AGENTS.md` and `START_HERE.md` in that folder. Keep this small demo separate from other projects.
3. Use Python 3.10 or newer. The app uses the standard library and needs no package installation.
4. Run the setup check below. It reports whether the key is present without showing its value.
5. If the key is missing, tell the user the absolute path to `api-key.txt`.
6. Have the user replace its placeholder with an OpenRouter key, then save. Paste only the key, without quotes.
7. Keep `free_only` set to `true`. Keep the supplied OpenRouter provider and reasoning setting.
8. Run the offline tests. Then start the app in a terminal that can remain running.

Use these commands from the extracted app folder on Windows:

```powershell
python --version
python app.py --check
python -m unittest -v
python app.py --open
```

To get a fresh copy with Git, run these commands in a suitable parent folder first:

```sh
git clone https://github.com/jhunter11/demo-tutor.git
cd demo-tutor
```

If Git is unavailable, use the linked ZIP. Find its folder containing `app.py`, `exercise.json`, and `settings.json`.

On macOS or Linux, use `python3` in place of `python`.
On Windows, `py -3` is another option if that launcher is available.
The local page is `http://127.0.0.1:8780/`.
The server keeps running until its terminal receives Ctrl+C.

## If the demo already runs

Check `/health` at the local address. Its `app` field must be `api-tutor-mvp`.
Check that `/exercise` returns the `first-match-search` example.
Reuse that server and open its page. Preserve any user code or unsent question already in the browser.

If another app uses port 8780, leave it running and start this demo on 8781:

```powershell
python app.py --port 8781 --open
```

Use the reported address. After an owned server restart, refresh its page before testing submission.

## Verify one reply

Open the page. Check the reference algorithm, editable student code, and sample input.
For the untouched starter, select "Why does my loop stop early?" and press Send.
The sample is `values = [4, 7, 2]`, `target = 7`, with expected index `1`.
Check that a final tutor answer appears and explains the premature `return -1`.
Confirm that the page shows token counts and allows another question.

If browser control is unavailable, use this one-request check instead:

```powershell
python app.py --verify-model
```

Use one verification path. A loaded key and passing offline tests do not prove model access.
Report any provider access or rate-limit failure. Do not repeat requests in a loop or enable paid fallback.
The page does not execute AVP. Its starter output comes from a manual trace.

## Return to the user

Give the page URL, absolute key-file path, and terminal stop command.
State the setup result, test result, and live reply result separately.
If setup fails, state the observed error and the next required action.
Keep credentials in the local key file. Do not copy them into this document or the ZIP.
