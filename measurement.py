import time

def measure_performance(algo_name="", operation=""):

    def decorator(func):

        def wrapper(*args, **kwargs):

            start = time.time()

            result = func(*args, **kwargs)

            end = time.time()

            execution_time = end - start

            print(
                f"[{algo_name}] {operation} completed in "
                f"{execution_time:.4f} seconds"
            )

            return result

        return wrapper

    return decorator
