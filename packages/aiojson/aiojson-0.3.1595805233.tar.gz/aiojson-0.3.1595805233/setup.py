import datetime
from setuptools import setup, find_packages


with open("README.rst") as description_file:
    setup(
        name="aiojson",
        version="0.3.{0}".format(int(datetime.datetime.now().timestamp())),
        description="Simple json request template validator for aiohttp",
        long_description=description_file.read(),
        packages=find_packages(exclude=["tests"]),
        url="https://git.yurzs.dev/yurzs/aiojson",
        install_requires=["aiohttp"],
    )
