# SWE-bench Dockerfiles (Multimodal)

Dockerfile generator for SWE-bench Multimodal benchmark.

## Usage

```bash
# From HuggingFace dataset
sb-dockerfile-gen-multimodal SWE-bench/SWE-bench_Multimodal --output_dir src/dockerfiles

# From local JSON/JSONL file
sb-dockerfile-gen-multimodal instances.jsonl --output_dir src/dockerfiles

# Specific instances
sb-dockerfile-gen-multimodal SWE-bench/SWE-bench_Multimodal --instance_ids some_instance --output_dir src/dockerfiles
```

## Output

Generated Dockerfiles are written to `src/dockerfiles/<instance_id>.Dockerfile`.

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
