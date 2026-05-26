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
# RESULTS FOLDER (RENDER COMPATIBLE)
# ==========================================

RESULTS_FOLDER = "results"

os.makedirs(
    RESULTS_FOLDER,
    exist_ok=True
)

# ==========================================
# CSV FILE PATH
# ==========================================

CSV_FILE = os.path.join(
    RESULTS_FOLDER,
    "performance_results.csv"
)

# ==========================================
# CREATE CSV FILE IF NOT EXISTS
# ==========================================

if not os.path.exists(CSV_FILE):

    with open(
        CSV_FILE,
        mode='w',
        newline=''
    ) as file:

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
# ENERGY CALCULATION FUNCTION
# ==========================================

def calculate_energy(cpu_percent, exec_time):

    """
    Estimates energy consumption
    in Joules using CPU utilization
    and execution time.
    """

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
# PERFORMANCE DECORATOR
# ==========================================

def measure_performance(algo_name, operation):

    """
    Measures:
    - File Size
    - Execution Time
    - CPU Usage
    - Energy Consumption
    """

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
            # CURRENT PROCESS
            # ==================================

            process = psutil.Process(
                os.getpid()
            )

            # ==================================
            # INITIALIZE CPU MONITOR
            # ==================================

            process.cpu_percent(
                interval=None
            )

            # ==================================
            # START TIMER
            # ==================================

            start_time = (
                time.perf_counter()
            )

            # ==================================
            # EXECUTE ORIGINAL FUNCTION
            # ==================================

            result = func(*args, **kwargs)

            # ==================================
            # STOP TIMER
            # ==================================

            end_time = (
                time.perf_counter()
            )

            # ==================================
            # CPU USAGE
            # ==================================

            cpu_percent = (
                process.cpu_percent(
                    interval=None
                )
            )

            # ==================================
            # EXECUTION TIME
            # ==================================

            exec_time = (
                end_time - start_time
            )

            # ==================================
            # ENERGY CONSUMPTION
            # ==================================

            energy = calculate_energy(
                cpu_percent,
                exec_time
            )

            # ==================================
            # TERMINAL OUTPUT
            # ==================================

            print(

                f"[{algo_name}] "

                f"{operation} | "

                f"Size: {file_size_mb} MB | "

                f"Time: {exec_time:.6f}s | "

                f"CPU: {cpu_percent:.2f}% | "

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

                    round(cpu_percent, 2),

                    round(energy, 6)

                ])

            return result

        return wrapper

    return decorator
