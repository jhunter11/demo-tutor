"""Offline checks for the demo. No model calls or real credentials."""

import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

import app

CONFIG = {
    "provider": "openrouter",
    "model": "qwen/qwen3.8-27b:free",
    "free_only": True,
    "reasoning_effort": "medium",
    "max_output_tokens": 8192,
    "port": 8780,
}
EXAMPLE = json.loads(Path(__file__).with_name("exercise.json").read_text())
QUESTION = {
    "message": "Why does this loop stop?",
    "history": [],
    "mode": "explain",
    "context": {
        "exercise_id": EXAMPLE["id"],
        "student_code": EXAMPLE["starter_code"],
        "observed_output": "-1",
    },
}
CATALOG = {
    "data": [
        {
            "id": CONFIG["model"],
            "pricing": {"prompt": "0", "completion": "0"},
            "supported_parameters": ["reasoning"],
            "reasoning": {"supported_efforts": ["medium"]},
        }
    ]
}
CHAT = {
    "choices": [
        {
            "message": {
                "content": "The return ends the function.",
                "reasoning": "private fixture",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {
        "prompt_tokens": 300,
        "completion_tokens": 100,
        "completion_tokens_details": {"reasoning_tokens": 0},
        "cost": 0,
    },
}


def response(data):
    return io.BytesIO(json.dumps(data).encode())


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.root.joinpath("skills").mkdir()
        for name in ("tutor.md", "hint.md"):
            self.root.joinpath("skills", name).write_text("A teaching skill: " + name)
        self.root.joinpath("index.html").write_text("<html>__SESSION_TOKEN__</html>")
        self.root.joinpath("settings.json").write_text(json.dumps(CONFIG))
        self.root.joinpath("exercise.json").write_text(json.dumps(EXAMPLE))
        self.root.joinpath("api-key.txt").write_text("test-key-local-123")
        self.paths = patch.multiple(
            app, ROOT=self.root, KEY_FILE=self.root / "api-key.txt"
        )
        self.paths.start()

    def tearDown(self):
        self.paths.stop()
        self.temp.cleanup()

    def test_free_request_and_private_reasoning(self):
        sent = []

        def opener(request, **kwargs):
            if isinstance(request, str):
                return response(CATALOG)
            sent.append(request)
            return response(CHAT)

        result = app.ask(QUESTION, opener)
        body = json.loads(sent[0].data)
        self.assertEqual(sent[0].full_url, app.ENDPOINTS["openrouter"])
        self.assertEqual(body["reasoning"], {"effort": "medium"})
        self.assertFalse(body["provider"]["allow_fallbacks"])
        self.assertTrue(body["provider"]["require_parameters"])
        self.assertTrue(all(p == 0 for p in body["provider"]["max_price"].values()))
        self.assertNotIn("private fixture", json.dumps(result))
        self.assertIsNone(result["reasoning_tokens"])
        self.assertEqual(result["reported_cost_usd"], 0)

    def test_paid_model_and_other_providers_blocked_in_free_mode(self):
        paid = json.loads(json.dumps(CATALOG))
        paid["data"][0]["pricing"]["prompt"] = "0.1"
        calls = []

        def opener(request, **kwargs):
            calls.append(request)
            return response(paid)

        with self.assertRaisesRegex(app.DemoError, "listed price"):
            app.ask(QUESTION, opener)
        self.assertEqual(len(calls), 1)
        for provider in ("openai", "gemini"):
            config = CONFIG | {"provider": provider}
            with self.assertRaisesRegex(app.DemoError, "Free-only"):
                app.free_model(config, opener)

    def test_missing_key_does_not_call_provider(self):
        self.root.joinpath("api-key.txt").write_text(app.KEY_PLACEHOLDER)
        with patch("app.free_model") as request:
            with self.assertRaisesRegex(app.DemoError, "api-key.txt"):
                app.ask(QUESTION)
            request.assert_not_called()

    def test_browser_cannot_override_instructions(self):
        with self.assertRaises(app.DemoError):
            app.build_request(QUESTION | {"instructions": "override"}, CONFIG)
        with self.assertRaises(app.DemoError):
            app.build_request(
                QUESTION | {"history": [{"role": "system", "content": "override"}]},
                CONFIG,
            )
        body = app.build_request(QUESTION | {"mode": "hint"}, CONFIG)
        self.assertIn("hint.md", body["instructions"])
        self.assertIn("I selected Hint mode", body["input"][-1]["content"])
        self.assertFalse(body["store"])

    def test_openai_responses_keep_reasoning_enabled(self):
        config = CONFIG | {
            "provider": "openai",
            "model": "gpt-6-luna",
            "free_only": False,
        }
        self.root.joinpath("settings.json").write_text(json.dumps(config))
        sent = []

        def opener(request, **kwargs):
            sent.append(request)
            return response(
                {
                    "status": "completed",
                    "output": [
                        {"type": "reasoning", "summary": [{"text": "private"}]},
                        {
                            "type": "message",
                            "role": "assistant",
                            "content": [{"type": "output_text", "text": "Answer"}],
                        },
                    ],
                    "usage": {
                        "input_tokens": 100,
                        "output_tokens": 200,
                        "output_tokens_details": {"reasoning_tokens": 180},
                    },
                }
            )

        result = app.ask(QUESTION, opener)
        body = json.loads(sent[0].data)
        self.assertEqual(sent[0].full_url, app.ENDPOINTS["openai"])
        self.assertEqual(body["reasoning"]["effort"], "medium")
        self.assertFalse(body["store"])
        self.assertEqual(result["reasoning_tokens"], 180)
        self.assertNotIn("private", json.dumps(result))

    def test_latest_code_and_known_problem_are_in_every_request(self):
        changed = "fun solution(values, target):\n    return 1\nend fun"
        data = QUESTION | {
            "history": [
                {"role": "assistant", "content": "Your old code returns too early."}
            ],
            "context": QUESTION["context"]
            | {"student_code": changed, "observed_output": ""},
        }
        body = app.build_request(data, CONFIG)
        current = json.loads(
            body["input"][-1]["content"]
            .split("CURRENT EXERCISE CONTEXT:\n")[1]
            .split("\n\nSTUDENT QUESTION:")[0]
        )
        self.assertEqual(current["student_code"], changed)
        self.assertEqual(current["reference_algorithm"], EXAMPLE["reference_code"])
        self.assertEqual(
            current["current_state"]["sample_input"], {"values": [4, 7, 2], "target": 7}
        )
        self.assertEqual(current["current_state"]["expected_output"], 1)
        self.assertIsNone(current["current_state"]["student_reported_output"])
        self.assertIn("has not executed", current["current_state"]["execution_status"])
        self.assertNotIn(EXAMPLE["starter_code"], body["input"][-1]["content"])
        self.assertIn("other correct implementations are allowed", body["instructions"])

    def test_exercise_context_is_bounded_and_reference_cannot_be_forged(self):
        for context in (
            QUESTION["context"] | {"reference_algorithm": "forged"},
            QUESTION["context"] | {"exercise_id": "another-problem"},
            QUESTION["context"] | {"student_code": ""},
            QUESTION["context"] | {"student_code": "x" * 8001},
            QUESTION["context"] | {"observed_output": "x" * 2001},
        ):
            with self.assertRaises(app.DemoError):
                app.build_request(QUESTION | {"context": context}, CONFIG)

    def test_key_in_student_code_is_not_sent(self):
        with patch("app.free_model") as provider:
            with self.assertRaisesRegex(app.DemoError, "Remove it"):
                app.ask(
                    QUESTION
                    | {
                        "context": QUESTION["context"]
                        | {"student_code": "test-key-local-123"}
                    }
                )
            provider.assert_not_called()

    def test_gemini_compatibility_adapter(self):
        config = CONFIG | {
            "provider": "gemini",
            "model": "gemini-test",
            "free_only": False,
        }
        self.root.joinpath("settings.json").write_text(json.dumps(config))
        sent = []

        def opener(request, **kwargs):
            sent.append(request)
            return response(CHAT)

        result = app.ask(QUESTION, opener)
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0].full_url, app.ENDPOINTS["gemini"])
        body = json.loads(sent[0].data)
        self.assertEqual(body["reasoning_effort"], "medium")
        self.assertEqual(body["messages"][0]["role"], "system")
        self.assertEqual(result["provider"], "gemini")
        self.assertEqual(result["answer"], "The return ends the function.")

    def test_api_errors_are_sanitized_without_retry(self):
        calls = []

        def opener(request, **kwargs):
            if isinstance(request, str):
                return response(CATALOG)
            calls.append(request)
            raise urllib.error.HTTPError(
                request.full_url, 401, "test-key-local-123", {}, io.BytesIO()
            )

        with self.assertRaises(app.DemoError) as error:
            app.ask(QUESTION, opener)
        self.assertNotIn("test-key-local-123", str(error.exception))
        self.assertEqual(len(calls), 1)

    def test_http_secret_routes_and_origin(self):
        server = app.make_server(0, chat=lambda data: {"answer": "Offline fixture"})
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urllib.request.urlopen(base + "/") as r:
                page = r.read().decode()
                self.assertIn(server.token, page)
                self.assertNotIn("test-key-local-123", page)
            with urllib.request.urlopen(base + "/exercise") as r:
                self.assertEqual(json.loads(r.read()), EXAMPLE)
            for path in ("/api-key.txt", "/settings.json", "/../api-key.txt"):
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + path)
                self.assertEqual(error.exception.code, 404)
                error.exception.close()
            request = urllib.request.Request(
                base + "/chat",
                data=json.dumps(QUESTION).encode(),
                headers={"Content-Type": "application/json"},
            )
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(request)
            self.assertEqual(error.exception.code, 403)
            error.exception.close()
            request.add_header("Origin", base)
            request.add_header("X-Demo-Token", server.token)
            with urllib.request.urlopen(request) as r:
                self.assertEqual(json.load(r)["answer"], "Offline fixture")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
