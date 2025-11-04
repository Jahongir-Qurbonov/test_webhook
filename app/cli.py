import asyncio

import aiohttp
import typer


async def main(msg: str):
    async with aiohttp.ClientSession() as session:
        url = "http://0.0.0.0:8000/start"
        async with session.post(url, json={"msg": msg}) as response:
            greeting = await response.json()
            print(greeting)

    async with aiohttp.ClientSession() as session:
        url = "http://0.0.0.0:8000/finish"
        async with session.get(url) as response:
            status = await response.json()
            print(status)


if __name__ == "__main__":
    typer.run(lambda msg: asyncio.run(main(msg)))
