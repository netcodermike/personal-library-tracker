# Validation

Authoring date: November 6, 2026. Host: Windows. Target: Windows, macOS, Linux desktop.

## Local result

Both Python test cases passed locally on Windows. Tkinter interaction remains manual.

## Reproducible checks

The GitHub Actions workflow builds/runs the following on `ubuntu-latest`:

```sh
python -m unittest -v
```

## Manual acceptance

Add two books, change reading status, lend/return one, test an overdue date and duplicate checkout, search for literal % or _, export CSV, and reopen the catalog.

A workflow file is not evidence of a passing run. Observed CI run links and source commits are recorded after publication. Native GUI, sound, sleep/resume, and platform permissions require direct target-platform acceptance even when model tests pass.
