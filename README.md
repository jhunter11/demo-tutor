# Demo Tutor

A small first milestone: one chatbot page, a hosted model API, and two draft teaching skills.
Read [START_HERE.md](START_HERE.md) to set one key file and launch the page.
Give [CODEX_LAUNCH.md](CODEX_LAUNCH.md) to Codex for a complete launch task.

The current default uses a free OpenRouter Nemotron 3 Super model with reasoning enabled.
The server checks catalog prices before each request and caps routing prices at zero.
It stops if pricing, model availability, or reasoning support fails those checks.
It makes no automatic retries or paid fallback calls.

## Files

| File | Purpose |
| --- | --- |
| `api-key.txt` | Your local API key. The shareable copy contains a placeholder. |
| `app.py` | Local server and model adapter, using only the Python standard library |
| `index.html` | The single chatbot page |
| `skills/tutor.md` | Draft explanation and teaching rules |
| `skills/hint.md` | Draft guided-hint rules |
| `settings.json` | Provider, model, reasoning, output limit, port, and free-price policy |
| `exercise.json` | One search problem, reference algorithm, input, expected output, and starter code |

The skill text enters the model instructions on each request.
Every question includes the fixed problem, reference algorithm, sample input, and expected output.
It also includes the latest code from the editor and optional observed output.
The server supplies the reference. The browser cannot replace it through a chat request.
The tutor compares behavior against the problem. It can accept correct code that differs from the reference.

Editing the code clears the old observed output. Add a result from your own run if available.
The starter output comes from a manual trace. This page does not execute the code.
New chat clears the conversation and keeps your code. Reset example restores the starter code and clears the chat.

The chatbot keeps recent conversation in browser memory and loses it after a reload.
It shows only the final answer, with reported token usage below it.
Reasoning tokens count toward total generated output and the configured limit.
The page does not execute code or verify student understanding.

## Other providers

The adapter also includes OpenAI Responses and the Gemini OpenAI-compatible endpoint.
These alternatives require an intentional change to `settings.json` and the matching key in `api-key.txt`.

For OpenAI, set `provider` to `openai`, `model` to `gpt-6-luna`, and `free_only` to `false`.
For Gemini, set `provider` to `gemini`, choose a thinking model available to your key, and set `free_only` to `false`.
Those settings permit provider charges. The default stays on free OpenRouter routing.
No provider switch occurs automatically. These alternate adapters have offline checks;
this demo's live checks used OpenRouter.

Official references: [OpenAI reasoning](https://developers.openai.com/api/docs/guides/reasoning),
[Gemini compatibility](https://ai.google.dev/gemini-api/docs/openai), and
[OpenRouter routing](https://openrouter.ai/docs/guides/routing/provider-selection), and
[the default free model](https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free).

## Scope

This is a standalone implementation with its own repository and Git history.
It includes one practice example and a small provider adapter.
Parser execution, vector retrieval, training datasets, and visualization remain future work.

Suggested milestones:

1. API chat and draft teaching skills: this MVP.
2. Reviewed explanations and a small retrieval example.
3. Execution context and integration with the team visualizer.
4. Session-level learning and cost evaluation.

These are scope proposals, not a backdated record of completed weekly work.
