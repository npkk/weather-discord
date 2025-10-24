from .entrypoint import run
import asyncio


def main() -> None:
    asyncio.run(run())
