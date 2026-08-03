#!/usr/bin/env python3
"""
CLI entry point to run either FastAPI or Flask server.
"""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run FastAPI or Flask server")
    parser.add_argument(
        "--framework",
        choices=["fastapi", "flask"],
        required=True,
        help="Which framework to run"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run server on (default: 8000)"
    )
    return parser.parse_args()


def run_fastapi(port: int):
    from fastapi_app.main import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


def run_flask(port: int):
    from flask_app.main import app
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    args = parse_args()
    
    if args.framework == "fastapi":
        run_fastapi(args.port)
    else:
        run_flask(args.port)