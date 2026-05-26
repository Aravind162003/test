import time
import psutil
import os
import csv
from functools import wraps

# ==========================================
# POWER CONFIGURATION
# ==========================================
MAX_POWER_WATTS = 15.0
IDLE_POWER_WATTS = 5.0

# ==========================================
# CSV FILE
# ==========================================
CSV_FILE = "performance_results.csv"

# ==========================================
# CREATE CSV IF NOT EXISTS
# ==========================================
if not os.path.exists(CSV_FILE):

    with open(CSV_FILE, mode='w', newline='') as file:

        writer = csv.writer(file)

        writer.writerow([
            "Algorithm",
            "Operation",
            "File Size (MB)",
            "Execution Time (s)",
            "CPU Usage (%)",
            "Energy Consumption (J)"
        ])

# ==========================================
# ENERGY CALCULATION
# ==========================================
def calculate_energy(cpu_percent, exec_time):

    average_power = (

        IDLE_POWER_WATTS +

        (
            MAX_POWER_WATTS -
            IDLE_POWER_WATTS
        ) * (cpu_percent / 100.0)

    )

    energy_joules = (
        average_power * exec_time
    )

    return energy_joules

# ==========================================
# MAIN DECORATOR
# ==========================================
def measure_performance(algo_name, operation):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # ==================================
            # FILE SIZE DETECTION
            # ==================================
            file_size_mb = "N/A"

            file_path = (
                args[0] if args else None
            )

            if (
                file_path and
                isinstance(file_path, str)
            ):

                try:

                    if (
                        os.path.exists(file_path)
                        and
                        os.path.isfile(file_path)
                    ):

                        file_bytes = (
                            os.path.getsize(file_path)
                        )

                        file_size_mb = round(
                            file_bytes / (1024 * 1024),
                            4
                        )

                except Exception:
                    pass

            # ==================================
            # START CPU + TIMER
            # ==================================
            psutil.cpu_percent(interval=None)

            start_time = (
                time.perf_counter()
            )

            # ==================================
            # EXECUTE FUNCTION
            # ==================================
            result = func(*args, **kwargs)

            # ==================================
            # STOP TIMER
            # ==================================
            end_time = (
                time.perf_counter()
            )

            cpu_percent = (
                psutil.cpu_percent(interval=None)
            )

            # ==================================
            # CALCULATIONS
            # ==================================
            exec_time = (
                end_time - start_time
            )

            energy = calculate_energy(
                cpu_percent,
                exec_time
            )

            # ==================================
            # PRINT OUTPUT
            # ==================================
            print(
                f"[{algo_name}] "
                f"{operation} | "
                f"Size: {file_size_mb} MB | "
                f"Time: {exec_time:.6f}s | "
                f"CPU: {cpu_percent}% | "
                f"Energy: {energy:.6f} J"
            )

            # ==================================
            # SAVE TO CSV
            # ==================================
            with open(
                CSV_FILE,
                mode='a',
                newline=''
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    algo_name,
                    operation,
                    file_size_mb,
                    round(exec_time, 6),
                    cpu_percent,
                    round(energy, 6)
                ])

            return result

        return wrapper

    return decorator
