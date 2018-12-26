import redis

import redis

conn  = redis.Redis(host=":",port = "6379",password="123456",socket_timeout=3)
conn.set("x1","bob")
print(conn.get("x1"))