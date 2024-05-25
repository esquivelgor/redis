import json
import time
import numpy as np
import pandas as pd
import redis
import requests
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

url = "https://raw.githubusercontent.com/bsbodden/redis_vss_getting_started/main/data/bikes.json"
response = requests.get(url)
bikes = response.json()

start_time = time.time()

json.dumps(bikes[0], indent=2)

pipeline = client.pipeline()
for i, bike in enumerate(bikes, start=1):
    redis_key = f"bikes:{i:03}"
    #pipeline.json().set(redis_key, "$", bike)
res = pipeline.execute()

cache_time = time.time() - start_time

# Measure time without caching
start_time = time.time()

# Process the data without caching
for i, bike in enumerate(bikes, start=1):
    print(json.dumps(bike, indent=2))
no_cache_time = time.time() - start_time
print("--------------------------------------")
print("Cache Time (ns): ", cache_time * 10000)
print("No Cache Time (ns):", no_cache_time * 10000)
print("--------------------------------------")