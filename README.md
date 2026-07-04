# 🏎️ FastF1 Telemetry Performance Analyzer

Compare Formula 1 driver telemetry from a real race session and benchmark three different computation approaches—**pandas**, **pure Python loops**, and **NumPy**—using approximately **90,000 telemetry rows**. Lights out and away we go

---

##  Features

-  Downloads and caches race session data using **FastF1**
-  Compares two drivers based on:
  - Average throttle
  - Braking distance
  - Top speed
  - Best lap sector times
  - Tire degradation (lap-time delta over a stint)
-  Benchmarks telemetry calculations with:
  - `timeit`
  - `cProfile`
-  Generates a performance comparison chart (`benchmark.png`)

---

##  Tech Stack

- **Python**
- **FastF1**
- **pandas**
- **NumPy**
- **matplotlib**

---

##  Setup

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

##  Running

Start the analyzer with:

```bash
python main.py
```

> **Note:** The first run downloads and caches the selected race session into the `data/` directory. Subsequent runs use the cached data.

---

##  Configuration

Edit the constants in `main.py` to customize the analysis.

| Variable | Example | Description |
|----------|---------|-------------|
| `YEAR` | `2025` | Formula 1 season |
| `GP` | `"Monaco"` | Grand Prix name |
| `SESSION` | `"R"` | Session type (`R` = Race, `Q` = Qualifying) |
| `DRIVER_A` / `DRIVER_B` | `"VER"`, `"LEC"` | Three-letter driver codes |
| `VERBOSE` | `False` | Print detailed telemetry information |
| `BENCHMARK_RUNS` | `50` | Number of `timeit` benchmark iterations |

---

##  Example Output

```text
Metric                        VER        LEC
--------------------------------------------
Avg throttle (%)       46.8       50.8
Braking dist (m)       65812.3    59196.2
Top speed (km/h)       288.0      291.0
...

=== timeit (50 runs, 90,865 rows) ===
pandas:  0.19s  (3.73 ms/run)
loops:   0.66s  (13.27 ms/run)
numpy:   0.06s  (1.23 ms/run)

loops vs numpy: 10.8× slower
```

---

##  Project Structure

```text
├── main.py                 # Entry point
├── data/                   # FastF1 cache (gitignored)
├── benchmark.png           # Generated benchmark chart (gitignored)
└── src/
    ├── session_loader.py   # Session loading & telemetry retrieval
    ├── metrics.py          # Driver comparison metrics
    ├── benchmarks.py       # Benchmarking & profiling
    └── telemetry_inspect.py
```

---

##  Why This Project?

This project goes beyond simply visualizing Formula 1 data. It demonstrates:

- Processing large telemetry datasets efficiently
- Comparing vectorized operations against pure Python loops
- Measuring performance with `timeit`
- Profiling bottlenecks using `cProfile`
- Applying a performance-first workflow: **measure first, optimize hot paths second**

The same mindset is widely used in high-performance software, systems programming, and kernel-adjacent development.

---

##  Built With

- **Python**
- **FastF1**
- **pandas**
- **NumPy**
- **matplotlib**
