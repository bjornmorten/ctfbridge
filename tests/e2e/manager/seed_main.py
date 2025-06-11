"""
CLI entry point for seeding / test-bootstrapping.
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed a CTF instance for E2E tests.")
    parser.add_argument(
        "--platform",
        required=True,
        choices=["ctfd", "rctf"],
        help="The platform to seed.",
    )
    parser.add_argument("--url", required=True, help="Base URL of the live instance.")
    args = parser.parse_args()

    if args.platform == "ctfd":
        from .ctfd_manager import CTFdManager

        manager = CTFdManager(base_url=args.url)
        manager.run_seed()

    elif args.platform == "rctf":
        from .rctf_manager import RCTFManager

        seeder = RCTFManager(base_url=args.url)
        seeder.run_seed()
    else:
        raise ValueError(f"Unknown platform: {args.platform}")


if __name__ == "__main__":
    main()
