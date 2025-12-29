from __future__ import annotations

import argparse
from pathlib import Path

from .dgps import get_dgp, list_dgps
from .runner import RunConfig, XGBConfig, run_experiment


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m dgp_xgb",
        description="Generate synthetic DGP data and evaluate a low-capacity XGBoost baseline.",
    )

    parser.add_argument("--list-dgps", action="store_true", help="List available DGPs and exit.")

    parser.add_argument("--dgp", type=str, default="dgp001_linear", help="DGP name.")
    parser.add_argument("--n-train", type=int, default=5000, help="Training rows.")
    parser.add_argument("--n-test", type=int, default=2000, help="Test rows.")
    parser.add_argument("--seed", type=int, default=0, help="Base RNG seed.")
    parser.add_argument("--noise-std", type=float, default=0.1, help="Gaussian noise stddev.")

    parser.add_argument(
        "--backend",
        type=str,
        default="baseline_mean",
        choices=["baseline_mean", "xgboost"],
        help="Model backend.",
    )

    parser.add_argument("--out-root", type=Path, default=Path("runs"), help="Output root directory.")
    parser.add_argument("--run-id", type=str, default=None, help="Optional run id (directory name).")

    parser.add_argument("--xgb-max-depth", type=int, default=2)
    parser.add_argument("--xgb-eta", type=float, default=0.1)
    parser.add_argument("--xgb-subsample", type=float, default=0.8)
    parser.add_argument("--xgb-colsample-bytree", type=float, default=0.8)
    parser.add_argument("--xgb-rounds", type=int, default=50)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list_dgps:
        for dgp in list_dgps():
            print(f"{dgp.name}\t(n_features={dgp.n_features})\t{dgp.description}")
        return 0

    try:
        get_dgp(args.dgp)
    except KeyError as exc:
        parser.error(str(exc))

    config = RunConfig(
        dgp=args.dgp,
        n_train=args.n_train,
        n_test=args.n_test,
        seed=args.seed,
        noise_std=args.noise_std,
        backend=args.backend,
        xgb=XGBConfig(
            max_depth=args.xgb_max_depth,
            eta=args.xgb_eta,
            subsample=args.xgb_subsample,
            colsample_bytree=args.xgb_colsample_bytree,
            num_boost_round=args.xgb_rounds,
        ),
    )

    artifacts = run_experiment(config=config, out_root=args.out_root, run_id=args.run_id)
    print(str(artifacts.run_dir))
    return 0
