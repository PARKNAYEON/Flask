from flask import Flask
from flask_executor import Executor
import os
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import json
import time

app = Flask(__name__)


# Task manager executor
_processpool_cpus = int(os.cpu_count() / 2)
executor = ProcessPoolExecutor(max_workers=max(_processpool_cpus, 2))


@app.route("/first", methods=["POST"])
def main():
    print("Request received")
    executor.submit(func1)
    return json.dumps({"status": True})


def func1():
    time.sleep(10)
    print("do it!!!!!!!!!!!!")


@app.route("/second", methods=["POST"])
def func2():
    print("Request received twotwo")
    time.sleep(5)
    print("func222222")
    return json.dumps({"status": False})


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)