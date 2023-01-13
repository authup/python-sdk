import asyncio
import inspect


def syncify(cls):
    for name, func in inspect.getmembers(cls, inspect.isfunction):
        if asyncio.iscoroutinefunction(func):
            setattr(cls, f"{name}_sync", add_sync(func))
    return cls


def add_sync(func):
    assert asyncio.iscoroutine(func) or asyncio.iscoroutinefunction(func)

    def wrapper(*args, **kwds):
        if asyncio.iscoroutinefunction(func):
            print("coroutine")
            print("func", func)
            print("args", args)
            print("kwds", kwds)
            print(inspect.signature(func).parameters)
            self_param = inspect.signature(func).parameters.get("self")
            print("self_param", self_param)

            return asyncio.run(func(*args, **kwds))
        else:
            print("not coroutine")
            print("func", func)
            print("args", args)
            print("kwds", kwds)
            print("func is not a coroutine function")
            return asyncio.new_event_loop().run_until_complete(func(*args, **kwds))

    func.sync = wrapper
    return func
