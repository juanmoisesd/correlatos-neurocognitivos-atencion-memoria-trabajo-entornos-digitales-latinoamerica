# Randomness Policy

To ensure reproducibility, all scripts involving random processes (e.g., data splitting, imputation) must set a fixed seed.
- Default seed: `42`
- Language specific implementations:
  - Python: `random.seed(42)`, `np.random.seed(42)`
  - R: `set.seed(42)`
