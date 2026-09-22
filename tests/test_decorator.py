from src.bookkeeping.decorators import timer, retry
import time


def test_timer_decorator():
    @timer
    def slow_function():
        time.sleep(1)
        print("测试计时装饰器")
        return "done"
    result = slow_function()
    assert result == "done"
    return result

def test_retry_decorator():
    count = 0
    @retry(times=3)
    def flaky_function():
        nonlocal count
        count += 1
        print(f"执行第{count}次")
        if count < 2:
            raise ValueError("临时失败")
        return "成功"

    result = flaky_function()
    assert result == "成功"
    print(f"一共尝试了 {count} 次")
    return result

print(test_timer_decorator())
print(test_retry_decorator())
