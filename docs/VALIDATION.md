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

## Observed CI result

Passed: [target-platform build/check](https://github.com/netcodermike/personal-library-tracker/actions/runs/42204015297). Source commit: `68194c34f2be39d06755bdfe23c4522a3a5337c3`. Later documentation-only changes do not alter the tested implementation. The reproducible commands above identify test scope; native GUI/audio/permissions are not implied by compilation.
