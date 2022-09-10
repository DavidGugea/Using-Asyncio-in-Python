from concurrent.futures import ThreadPoolExecutor as Executor


def worker(data):
    # <process the data>
    pass


with Executor(max_workers=10) as exe:
    future = exe.submit(worker, data)
