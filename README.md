# SWE-bench Dockerfiles (Multimodal)

Dockerfile generator for SWE-bench Multimodal (JavaScript) benchmarks.

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

Generated Dockerfiles are written to `src/dockerfiles/<instance_id>/Dockerfile`.

## Install

```bash
pip install -e .
```
