# 🤝 Optimal Matching with Men’s Coalition (House-Swapping / Strict Core)

This project implements a coalition-based stable matching algorithm where men can collude to improve their match outcomes in a traditional Gale-Shapley stable marriage setting. The strategy models the coalition as a **house-swapping problem** and uses the **Top Trading Cycle (TTC)** algorithm to find the **strict core** of the market.

---

## Overview

- Implements the **Gale-Shapley algorithm** for men-optimal stable matching (M₀).
- Models men's coalition as a **house-swapping market** where their M₀ partners are tradable "houses".
- Uses the **Top Trading Cycle (TTC)** algorithm to find a **strict core** matching that improves men's outcomes collectively.
- Measures happiness using a **rank-based utility**:  
  `Happiness = len(pref_list) - index_of_assigned_partner`  
  (Higher = better; Top choice gives maximum score)

---

## Input Format

The program expects a `prefs.json` file structured as follows:

```json
{
  "men": {
    "m1": ["w1", "w2", "w5", "w4", "w3"],
    "m2": ["w2", "w5", "w4", "w1", "w3"],
    ...
  },
  "women": {
    "w1": ["m3", "m2", "m4", "m1", "m5"],
    "w2": ["m4", "m5", "m1", "m2", "m3"],
    ...
  }
}
```

- Keys: `"men"` and `"women"` — each maps to a dictionary of preference lists.
- Each individual ranks all members of the opposite group in order of preference.

---

## How to Run

1. **Ensure you have Python 3 installed.**
2. Place `main.py` and `prefs.json` in the same directory.
3. Run the program using:

```bash
python3 main.py
```

4. The result will be printed to the console and also saved in `output.txt`.

---

## Output Format (`output.txt`)

The program generates the following:

- **Original Preferences** of all individuals.
- **Men-Optimal Matching (M₀)** from Gale-Shapley.
- **Coalition Matching** using TTC (strict core).
- **Final Enforced Matching** via modified preferences.
- **Happiness scores** for each man in both M₀ and final matching.
- **Total happiness** comparison before and after coalition.

Example excerpt:
```
Step 1: Men-Optimal Matching (M0):
  m1 → w5
  m2 → w4
  ...

Step 3: Final Matching (Enforced by Coalition):
  m1 → w1
  m2 → w2
  ...

Happiness Scores (higher is better):
  (M0)    (Final)
m1:   3       5
...
```

---

## Features

- **No woman rejects first proposals** in coalition enforcement (assumption).
- Ensures **Pareto-improvement** or at least no-worse outcome for all men.
- Reports if strict core gives an improvement over M₀.
- Modular, readable code design with pseudocode-style clarity.

---

## Theoretical Foundation

- **Gale-Shapley Algorithm (1962)** – Stable marriage problem.
- **Shapley & Scarf (1974)** – House-swapping and strict core.
- **Top Trading Cycles (TTC)** – Algorithm to find core allocations in exchange economies.
- **Rank-based utility** – A standard ordinal utility model in matching theory.

---

## Files Included

- `main.py` – Main implementation.
- `prefs.json` – Input preference data.
- `output.txt` – Program output (generated after running).

---
