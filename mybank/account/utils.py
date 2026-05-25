from django.core.cache import cache


def rate_limit(key, max_attempts=5, window_seconds=900):
    attempts = cache.get(key, 0)
    if attempts >= max_attempts:
        return False
    cache.set(key, attempts + 1, timeout=window_seconds)
    return True
