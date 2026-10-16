# System 1 Powered SLM

When should a small model ask for help? A "System One" router watches a small thinking model (Qwen3-1.7B) work through a write → test → revise loop on HumanEval+ and MBPP+, predicts whether the current attempt will fail the withheld tests, and decides at each checkpoint whether it should consult a frontier model. Target: IEEE BigData 2026 Workshop on Data and Model Efficiency for Scalable AI (deadline Oct 29, 2026, 11:59 PM AoE).

- Plan: [docs/research-plan.md](docs/research-plan.md) (exported from the team's Claude Doc, which is the source of truth)
- Research behind the design: [research/](research/)

## Layout

| Path | What goes there |
| --- | --- |
| `docs/` | The research plan and other project docs |
| `research/` | Literature reports (drift signals, reasoning-trace monitoring) |
| `docker/gpu/`, `docker/cpu/` | The vLLM GPU image and the slim CPU image |
| `configs/` | Model, decoding, router and pinned price (`prices.yaml`) configs |
| `src/system1/loop/` | The small model's write → test → revise loop and sandboxed test runner |
| `src/system1/features/` | Trace statistics and loop telemetry computed at each checkpoint |
| `src/system1/routers/` | System One routers (Jev with typed drift questions, Pinocchio-0.8B; optional fine-tuned Qwen3-1.7B) and baselines |
| `src/system1/frontier/` | Frontier takeover calls through OpenRouter |
| `src/system1/eval/` | Offline replay, cost ledger analysis and statistics |
| `scripts/` | Entry points (smoke test, pilot, full run) |
| `tests/` | Unit tests |
| `notebooks/` | Exploration and figures |
| `data/` | Benchmarks, trajectories and logs (not committed) |
| `results/` | Run outputs (not committed) |
| `paper/` | The LaTeX paper and `figures/` |

Secrets go in `.env` (copy `.env.example`); it is git-ignored.
