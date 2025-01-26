from redis import Redis

# Configuration for Redis
def get_redis_client():
    return Redis(host='localhost', port=6379, decode_responses=True)