                                              

from __future__ import annotations

import argparse
import sys

from .core import APP_VERSION, format_derived_output, run_derivation
from .gui import launch_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YellowSphere")
    parser.add_argument("--version", action="version", version=f"YellowSphere {APP_VERSION}")
    parser.add_argument("--gui", action="store_true", help="Launch the PySide6 desktop GUI.")
    parser.add_argument("--mnemonic", help="BIP39 mnemonic (12 or 24 words).")
    parser.add_argument("--passphrase", default="", help="Optional BIP39 passphrase.")
    parser.add_argument(
        "--derivation",
        default="",
        help="Custom derivation path. Supports both ' and h. Defaults to the selected coin standard.",
    )
    parser.add_argument(
        "--all-common",
        action="store_true",
        help="Derive m/44'/coin'/0', m/49'/coin'/0', m/84'/coin'/0', and m/86'/coin'/0' where applicable.",
    )
    parser.add_argument(
        "--script-type",
        choices=["auto", "p2pkh", "p2wpkh-p2sh", "p2wpkh", "p2tr"],
        default="auto",
    )
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument(
        "--coin",
        choices=[
            "bitcoin",
            "avalanche",
            "bitcoincash",
            "bnbchain",
            "cardano",
            "cosmos",
            "dogecoin",
            "ethereum",
            "litecoin",
            "polygon",
            "solana",
            "stellar",
            "tron",
            "xrp",
        ],
        default="bitcoin",
    )
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--output-format", choices=["json", "csv", "txt"], default="json", help="CLI output format.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.gui or not args.mnemonic:
        launch_gui()
        return

    out = run_derivation(
        mnemonic=args.mnemonic,
        passphrase=args.passphrase,
        derivation=args.derivation,
        all_common=args.all_common,
        script_type=args.script_type,
        count=args.count,
        coin=args.coin,
        testnet=args.testnet,
    )
    print(format_derived_output(out, args.output_format), end="")


def safe_main() -> None:
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
