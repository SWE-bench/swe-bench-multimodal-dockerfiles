# SWE-bench Dockerfiles (Multimodal)

Dockerfile generator for SWE-bench Multimodal benchmark.

## Usage

```bash
# From HuggingFace dataset
dockerfile-gen

# From local JSON/JSONL file
dockerfile-gen

# Specific instances
dockerfile-gen
```

## Output

`Dockerfile` and `eval.sh` are regenerated in place under `tasks/<instance_id>/`, from that task's `task.yaml`.

## Install

```bash
pip install -e .
```

## Running gold evaluation

Run with modest parallelism, around `-j 4`. Tests write their results to stdout, which
is buffered, while the markers the harness slices on are written to stderr. Under heavy
parallel load stdout can flush after the end marker, so the harness reads no results and
reports a failure even though the tests passed.

Three instances hit this most often: `PrismJS__prism-1853`, `PrismJS__prism-2348`, and
`carbon-design-system__carbon-7350`.

If an instance fails, re-run it on its own before treating it as a real failure. A run
where every test in a file "fails", or where the log ends without test output, is almost
always this problem rather than a broken instance. Check the saved log: if the tests
passed in it, the result was lost, not failed.
