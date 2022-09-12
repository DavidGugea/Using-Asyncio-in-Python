import asyncio


async def f():
    await asyncio.sleep(1.0)
    return 123


async def main():
    result = await f()  # Calling f() produces a coroutine; this means we are allowed to await it. The value of the
    # result variable will be 123 when f() completes
    return result
