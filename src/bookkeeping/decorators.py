import time
from functools import wraps

 #计时装饰器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"耗时：{time.time() - start:.4f}s")
        return result
    return wrapper

#重试装饰器
def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"重试{attempt + 1}/{times}次失败: {e}")
        return wrapper
    return decorator