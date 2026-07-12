# experiments/

One subfolder per domain (fraud/currency/voice/scam), one subfolder per run:
`experiments/<domain>/exp_NN_<description>/` (e.g. `experiments/fraud/exp_02_lightgbm/`).
Each should contain the training script/notebook used, resulting metrics, and a one-line
note on what changed from the previous experiment (`SYSTEM_RULES.md` §3).

Promoting an experiment to production = copy its output into `models/<domain>/` and record
the source `exp_NN` in `configs/models.yaml`.
