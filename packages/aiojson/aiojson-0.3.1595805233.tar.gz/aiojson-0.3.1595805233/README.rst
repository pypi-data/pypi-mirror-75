aiojson
=======
|pipeline status| |coverage report| |pypi link|

.. |coverage report| image:: https://git.yurzs.dev/yurzs/aiojson/badges/master/coverage.svg
   :target: https://git.yurzs.dev/yurzs/aiojson/-/commits/master

.. |pipeline status| image:: https://git.yurzs.dev/yurzs/aiojson/badges/master/pipeline.svg
   :target: https://git.yurzs.dev/yurzs/aiojson/-/commits/master

.. |pypi link| image:: https://badge.fury.io/py/aiojson.svg
   :target: https://pypi.org/project/aiojson

Simple json template verifier for ``aiohttp``

Usage
-----

Simple example:

.. code-block:: python

    from aiohttp import JsonTemplate


    @JsonTemplate({
        "messages": [{
            "id": int,
            "text": str
    }])
    async def received_message(request, validated_data):
        pass
