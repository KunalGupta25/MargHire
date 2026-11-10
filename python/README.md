# MargHire Python helper

Optional sidecar for local inference (Laya), embeddings and evaluation scripts.

Requires Python 3.11+. Install with [uv](https://github.com/astral-sh/uv):

```sh
cd python
uv pip install -e ".[dev]"
```

## Evaluation harness

The `eval/` directory contains the Phase 0 evaluation harness for the Role Lens comparison.

```sh
# Run all unit tests for the harness
pytest

# Run the eval (requires adapter config; see eval/README.md)
python -m eval.run --adapter llm --output results/
```

See `eval/data/README.md` for the pair schema and how to add pairs.
