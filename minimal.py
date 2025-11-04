#!/usr/bin/env python3
"""
Minimal webhook test application - single file version
Usage: python minimal_webhook.py <message>
"""

import os
import time
from typing import Dict, Literal, Optional

import requests
import typer
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

API_URL = "https://test.icorp.uz/interview.php"

STORAGE_FILE = "data/minimal.json"


def load_storage() -> Dict[str, Optional[str]]:
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            import json

            return json.load(f)
    return {
        "req_msg": None,
        "part1": None,
        "part2": None,
        "message": None,
    }


def save_storage(storage: Dict[str, Optional[str]]):
    with open(STORAGE_FILE, "w") as f:
        import json

        json.dump(storage, f)


def save_single_value(**kwargs):
    storage = load_storage()
    storage.update(kwargs)
    save_storage(storage)
    return storage


class CallbackRequest(BaseModel):
    part2: str


class CallbackResponse(BaseModel):
    part2: str


app = FastAPI(title="Minimal Webhook Test")


@app.post("/callback")
def callback_endpoint(data: CallbackRequest):
    part2 = data.part2
    save_single_value(part2=part2)

    print(f"Callback received, part2: {part2}")
    return CallbackResponse(part2=part2)


def run_cli(msg: str):
    CALLBACK_URL = os.getenv("CALLBACK_URL")
    assert CALLBACK_URL is not None, "CALLBACK_URL environment variable must be set"

    print("Callback URL:", CALLBACK_URL)
    print(f"Starting with msg: '{msg}'")

    storage = load_storage()
    storage["req_msg"] = msg
    storage["part1"] = None
    storage["part2"] = None
    storage["message"] = None
    save_storage(storage)

    print("Sending initial request...")
    try:
        if CALLBACK_URL.endswith("/"):
            CALLBACK_URL = f"{CALLBACK_URL}callback"
        else:
            CALLBACK_URL = f"{CALLBACK_URL}/callback"

        response = requests.post(API_URL, json={"msg": msg, "url": CALLBACK_URL})
        response.raise_for_status()

        resp_data = response.json()
        part1 = resp_data["part1"]

        storage = save_single_value(part1=part1)
        print(f"Initial part received: {part1}")
    except Exception as e:
        print(f"Error sending initial request: {e}")
        return

    retry_count = 0
    while storage["part2"] is None:
        storage = load_storage()
        retry_count += 1
        time.sleep(1)

        if retry_count > 15:
            raise RuntimeError("Callback not received within expected time")

    print("Getting final message...")
    if storage["part1"] and storage["part2"]:
        final_code = f"{storage['part1']}{storage['part2']}"

        try:
            response = requests.get(API_URL, params={"code": final_code})
            response.raise_for_status()

            resp_data = response.json()
            message = resp_data["msg"]

            storage = save_single_value(message=message)

            print(f"Final message: {message}")
        except Exception as e:
            print(f"Error getting final message: {e}")
    else:
        print("Missing part1 or part2")


def main(type: Literal["server", "cli"] = "cli", msg: Optional[str] = None):
    match type:
        case "server":
            uvicorn.run(app, host="0.0.0.0", port=8000)
        case "cli":
            if msg is None:
                print("Please provide a message argument for CLI mode.")
                return

            run_cli(msg)


if __name__ == "__main__":
    typer.run(main)
