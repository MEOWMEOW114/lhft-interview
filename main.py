from re import S
from fastapi import FastAPI
from pydantic import BaseModel
from logging.config import dictConfig
import logging
import string
import random
import asyncio
from config import LogConfig
app = FastAPI()
symbols = list(
    set([''.join(random.choices(string.ascii_uppercase, k=4)) for _ in range(500)]))
dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")


# logger.info("Dummy Info")
# logger.error("Dummy Error")
# logger.debug("Dummy Debug")
# logger.warning("Dummy Warning")

items = {}
generate_ticker_queue = asyncio.Queue()
store_queue = asyncio.Queue()


async def publish_task():
    choices = string.digits
    letter_choices = string.ascii_uppercase
    # host_id = "".join(random.choices(choices, k=4))
    # ticker = "".join(random.choices(letter_choices, k=4))
    logger.debug(f"")

    # logger.debug(f"{host_id}")

    target_symbols = random.sample(symbols, 300)
    data_list = list(map(lambda sym:  {
        'ticker': sym,
        'price': int(random.uniform(0, 1) * 1000)
    }, target_symbols))
    # data_dict = {
    #     'ticker': ticker,
    #     'host_id': host_id
    # }
    generate_ticker_queue.put_nowait(data_list)

    # store histoical queue for query
    store_queue.put_nowait(data_list)


async def publish(queue):
    while True:
        asyncio.create_task(publish_task())
        await asyncio.sleep(0.1)


async def consume(queue, id):
    while True:
        msg_dict = await queue.get()
        logger.debug(f"consume {id} {msg_dict[:2]} {len(msg_dict)}")


async def hello():
    css = publish(generate_ticker_queue)
    consume_cr = consume(generate_ticker_queue, 1)
    consume_cr_2 = consume(store_queue, 2)

    publish_task = asyncio.create_task(css)
    publish_task_3 = asyncio.create_task(consume_cr)
    publish_task_2 = asyncio.create_task(consume_cr_2)

    print(publish_task.get_name())


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    logger.debug("Dummy Info")
    asyncio.create_task(hello())
