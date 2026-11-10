# MargHire Python helper

Optional sidecar for local inference (Laya), embeddings and evaluation scripts.

Requires Python 3.11+. Install with [uv](https://github.com/astral-sh/uv):

```sh
cd python
uv pip install -e ".[dev]"
```

## Evaluation harness

The `eval/` directory contains the Phase 0 evaluation harness and public synthetic pairs for the Role Lens comparison. Clef and Gemini adapters make provider calls; Laya and the generic LLM adapter are stubs in the main harness.

```sh
# Run all unit tests for the harness
pytest

# Run the Gemini comparison (set GEMINI_API_KEY in the environment or repo-root .env)
python -m eval.run --adapter gemini-flash --shuffles 3 --output results/

```

### Laya comparison in a separate environment

Install the [Laya upstream server](https://github.com/NandhaKishorM/laya) into a temporary environment rather than the MargHire environment. In PowerShell:

```powershell
$LayaVenv = Join-Path $env:TEMP "marghire-laya"
uv venv --python 3.14 $LayaVenv
$LayaPython = Join-Path $LayaVenv "Scripts/python.exe"
uv pip install --python $LayaPython "laya[serve]==0.4.23"
$env:LAYA_HOST = "127.0.0.1"
$env:LAYA_DEVICE = "cpu"
& (Join-Path $LayaVenv "Scripts/laya-serve.exe")
```

The server downloads its checkpoint on first inference. Leave it running, open another terminal, change to `python/`, then run the standalone evaluator:

```powershell
python -m eval.run_laya_endpoint --shuffles 3 --output results/
```

The standalone evaluator accepts `--model` to select a checkpoint name served by Laya (default: `english`). It only accepts a loopback endpoint and sends requests to `http://127.0.0.1:8000/v1/systemone`. Set `LAYA_API_KEY` in the evaluator terminal only if you enable server authentication. Results from private pairs may contain their IDs; keep those files out of version control.

See `eval/data/README.md` for the pair schema and how to add pairs. Result JSON records the run time, adapter and model identifiers, shuffle count, per-pair metrics, and mean order sensitivity. Provider costs remain unknown unless measured separately. Commit results only for the public synthetic set; keep results from private pairs outside the repository.
