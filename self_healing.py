import time
from datetime import datetime


def self_healing(retries=3, delay=1):
    """
    A decorator that adds self-healing behavior to any function.
    Automatically retries the function when an exception occurs.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    log_error(func.__name__, e, attempts)
                    time.sleep(delay)
            raise Exception(f"Function '{func.__name__}' failed after {retries} retries.")
        return inner
    return wrapper


def log_error(func_name, error, attempt):
    """Log errors with timestamps for debugging & tracing."""
    print(f"[{datetime.now()}] Attempt {attempt}: {func_name} failed → {error}")


@self_healing(retries=3, delay=0.5)
def unstable_operation():
    """
    Simulates a real-world unstable operation.
    70% chance of failure → tests the self-healing decorator.
    """
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure occurred!")
    return "Operation completed successfully."


def main():
    result = unstable_operation()
    print(result)


if __name__ == "__main__":
    main()

