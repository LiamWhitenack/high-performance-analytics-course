import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Directories ---
LOG_DIR = Path("hw4/logs")
SCTRL_DIR = Path("scontrol_logs")

# --- Regex patterns for data extraction ---
patterns = {
    "tasks": re.compile(r"Using\s+(\d+)\s+tasks"),
    "total_limit": re.compile(r"TOTAL_LIMIT=(\d+)"),
    "largest_prime": re.compile(r"Largest\s+prime=(\d+)"),
    "total_primes": re.compile(r"Total\s+primes=(\d+)"),
    "wall_time": re.compile(r"Wallclock time elapsed:\s*([\d.]+)\s*seconds")
}

data = []

# --- Parse each log file ---
for logfile in LOG_DIR.glob("mpi_*.out"):
    match = re.match(r"mpi_(single_node|two_nodes)_(\d+)cores\.out", logfile.name)
    if not match:
        continue
    scenario, cores = match.groups()
    cores = int(cores)

    text = logfile.read_text()

    parsed = {
        "scenario": scenario,
        "cores": cores,
    }

    for key, pattern in patterns.items():
        m = pattern.search(text)
        if m:
            parsed[key] = float(m.group(1)) if key == "wall_time" else int(m.group(1))
        else:
            parsed[key] = None

    data.append(parsed)

# --- Build DataFrame ---
df = pd.DataFrame(data).sort_values(["scenario", "cores"])
print("\n=== Parsed Results ===")
print(df.to_string(index=False))

# --- Save to CSV ---
df.to_csv("weak_scaling_results.csv", index=False)
print("\nResults saved to weak_scaling_results.csv")

# --- Plot time vs cores for each scenario ---
for scenario, group in df.groupby("scenario"):
    plt.figure()
    plt.plot(group["cores"], group["wall_time"], marker="o", label=scenario)
    plt.title(f"Weak Scaling: {scenario}")
    plt.xlabel("Number of Cores")
    plt.ylabel("Wallclock Time (s)")
    for _, row in group.iterrows():
        label = f"TOT={row['total_limit']}\nMax={row['largest_prime']}\n#={row['total_primes']}"
        plt.annotate(label, (row["cores"], row["wall_time"]),
                     textcoords="offset points", xytext=(5,5), fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"weak_scaling_{scenario}.png", dpi=200)
    plt.close()
    print(f"Plot saved: weak_scaling_{scenario}.png")

# --- Weak scalability evaluation ---
# Ideal weak scaling: time should stay constant as cores increase
for scenario, group in df.groupby("scenario"):
    base_time = group.iloc[0]["wall_time"]
    avg_time = group["wall_time"].mean()
    efficiency = base_time / avg_time * 100
    print(f"\nWeak scalability efficiency ({scenario}): {efficiency:.1f}%")
    print("Interpretation: 100% = perfect scaling; lower values mean communication overhead.")
