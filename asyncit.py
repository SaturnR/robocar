import asyncio


def fire(task, *args, **kwargs):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    if callable(task):
        return loop.run_in_executor(None, task, *args, **kwargs)
    else:    
        raise TypeError("This task isn't callable")


