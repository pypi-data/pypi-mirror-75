# redis-simple-mq

A simple message queue for Redis.

![release](https://img.shields.io/pypi/v/redis-simple-mq?label=release) ![python](https://img.shields.io/pypi/pyversions/redis-simple-mq) ![pipeline](https://gitlab.com/ErikKalkoken/redis-simple-mq/badges/master/pipeline.svg) ![coverage](https://gitlab.com/ErikKalkoken/redis-simple-mq/badges/master/coverage.svg) ![license](https://img.shields.io/badge/license-MIT-green) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Description

This is a light-weight message queue based on Redis.

Key features:

- Class based API to the queue with all basic queue functions
- Queue is implement as FIFO
- All messages are stored and retrieved as UTF-8 strings
- Bulk methods for enqueue and dequeue
- No limint on the number of parallel queues

## Basic example

```python
from redis import Redis
from simple_mq import SimpleMQ

conn = Redis()
q = SimpleMQ(conn)
q.enqueue('Hello, World!')
message = q.dequeue()
print(message)
```

See also the examples folder for examples.
