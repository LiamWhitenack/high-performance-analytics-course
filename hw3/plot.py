import pandas as pd
import matplotlib.pyplot as plt

# --- Load the data ---
# Example log lines look like: "Threads=4 Time=0.039912"
df = pd.read_csv("results.log", sep=r"\s+", engine="python", header=None, names=["Threads", "Time"])

# --- Clean the data ---
df["Threads"] = df["Threads"].str.split("=").str[1].astype(int)
df["Time"] = df["Time"].str.split("=").str[1].astype(float)

# --- Compute averages per thread count ---
summary = df.groupby("Threads", as_index=False).agg(Average_Time=("Time", "mean"))

# --- Compute speedup relative to 1 thread ---
t1 = summary.loc[summary["Threads"] == 1, "Average_Time"].values[0]
summary["Speedup"] = t1 / summary["Average_Time"]

print(summary)

# --- Plot results ---
plt.figure(figsize=(8, 5))
plt.plot(summary["Threads"], summary["Average_Time"], marker="o")
plt.xlabel("Number of Threads")
plt.ylabel("Average Execution Time (s)")
plt.title("OpenMP Performance Scaling")
plt.grid(True)
plt.tight_layout()
plt.savefig("execution_time.png")
plt.show()

# --- Plot speedup ---
plt.figure(figsize=(8, 5))
plt.plot(summary["Threads"], summary["Speedup"], marker="o", color="green")
plt.xlabel("Number of Threads")
plt.ylabel("Speedup (relative to 1 thread)")
plt.title("OpenMP Speedup Curve")
plt.grid(True)
plt.tight_layout()
plt.savefig("speedup.png")
plt.show()
