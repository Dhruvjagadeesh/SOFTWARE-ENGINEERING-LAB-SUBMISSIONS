# Lab 5 – Reflection

**1. Which issues were the easiest and hardest to fix?**
Easiest: the mechanical ones – unused imports/variables, `== None`, missing final newline, docstrings and snake_case names. Pylint and Flake8 tell you exactly what to change. Hardest: `eval` in `calculateDiscountedBill`. Removing it meant changing the function's contract (a promo *expression* became a numeric `discount_rate`) and updating the caller, so it was a design decision, not a one-line edit. The MD5 → SHA-256 swap and the `os.system` removal were also quick once I understood why they were risky.

**2. Did the tools report any false positives?**
Mostly no, but some findings are context-dependent. Bandit's B324 (MD5) and B311 (`random`) are only truly dangerous if the value is used for security; here a "POS PIN" is security-sensitive, so B311 was valid, but a plain ticket ID checksum would be a borderline case (`usedforsecurity=False` would be an acceptable alternative). The "Line too long" check differs between Pylint (100) and Flake8 (79), so the same line is fine in one tool and flagged in the other. Also, no tool flagged the hardcoded `POS_TERMINAL_SECRET_TOKEN_2026` being printed to the console – I found that by reading the output, which shows tools don't catch everything.

**3. How would you integrate static analysis into your workflow?**
Run Flake8/Pylint in the editor on save, add a pre-commit hook for Flake8 and Bandit, and run all three in CI (e.g. GitHub Actions) so a pull request fails if Bandit reports High/Medium issues or the Pylint score drops below a threshold such as 9.5.

**4. What tangible improvements did I see in the code?**
Pylint went from 4.81 to 10.00, and Bandit and Flake8 dropped to zero findings. More importantly the code is safer (no code execution, no shell, no weak hash, no hardcoded secret), more correct (no shared mutable default, files always closed, errors no longer swallowed), more readable (consistent naming, docstrings) and importable without side effects thanks to the `__main__` guard.
