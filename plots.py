import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
CSV_PATH = "results.csv"
GRAPH_DIR = "analysis/graphs"

def generate_plots():
    print("📊 Starting Data Analysis...")

    # Ensure the graphs directory exists
    os.makedirs(GRAPH_DIR, exist_ok=True)

    # 1. Load the data
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f" Error: {CSV_PATH} not found. Please run experiments first.")
        return

    # Convert columns to numeric (forces errors to NaN, then we drop them if any)
    df['Time_sec'] = pd.to_numeric(df['Time_sec'], errors='coerce')
    df['Energy_Joules'] = pd.to_numeric(df['Energy_Joules'], errors='coerce')
    df = df.dropna(subset=['Time_sec', 'Energy_Joules'])

    # 2. Separate Data into Encryption and OTPs
    encryption_algos = ['AES-128', 'AES-256', 'ChaCha20']
    otp_algos = ['SHA256-OTP', 'HMAC-OTP', 'TOTP']

    # Filter data for only "Encrypt" and "Generate" operations to keep comparisons fair
    df_encrypt = df[(df['Algorithm'].isin(encryption_algos)) & (df['Operation'] == 'Encrypt')]
    df_otp = df[(df['Algorithm'].isin(otp_algos)) & (df['Operation'] == 'Generate')]

    # Calculate the average (mean) for each algorithm
    avg_encrypt = df_encrypt.groupby('Algorithm')[['Time_sec', 'Energy_Joules']].mean().reindex(encryption_algos)
    avg_otp = df_otp.groupby('Algorithm')[['Time_sec', 'Energy_Joules']].mean().reindex(otp_algos)

    # --- PLOTTING ---
    plt.style.use('bmh') # Nice, professional styling for academic reports

    # Plot 1: Encryption Energy
    plt.figure(figsize=(8, 5))
    avg_encrypt['Energy_Joules'].plot(kind='bar', color=['#3498db', '#e74c3c', '#2ecc71'])
    plt.title('Energy Consumption: Encryption Algorithms (10MB File)')
    plt.ylabel('Energy (Joules)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/encryption_energy.png", dpi=300)
    plt.close()

    # Plot 2: Encryption Time
    plt.figure(figsize=(8, 5))
    avg_encrypt['Time_sec'].plot(kind='bar', color=['#3498db', '#e74c3c', '#2ecc71'])
    plt.title('Execution Time: Encryption Algorithms (10MB File)')
    plt.ylabel('Time (Seconds)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/encryption_time.png", dpi=300)
    plt.close()

    # Plot 3: OTP Energy
    plt.figure(figsize=(8, 5))
    avg_otp['Energy_Joules'].plot(kind='bar', color=['#9b59b6', '#f1c40f', '#e67e22'])
    plt.title('Energy Consumption: OTP Generation')
    plt.ylabel('Energy (Joules)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/otp_energy.png", dpi=300)
    plt.close()

    # Plot 4: OTP Time
    plt.figure(figsize=(8, 5))
    avg_otp['Time_sec'].plot(kind='bar', color=['#9b59b6', '#f1c40f', '#e67e22'])
    plt.title('Execution Time: OTP Generation')
    plt.ylabel('Time (Seconds)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/otp_time.png", dpi=300)
    plt.close()

    print(f" Success! 4 graphs have been saved to the '{GRAPH_DIR}' folder.")

if __name__ == "__main__":
    generate_plots()
