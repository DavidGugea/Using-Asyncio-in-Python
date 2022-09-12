import inspect


async def f():
    return 123


print(type(f))
print(inspect.iscoroutinefunction(f))
