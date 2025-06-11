import argparse


def main():
    parser = argparse.ArgumentParser(description="Seed a CTF instance for E2E tests.")
    parser.add_argument(
        "--platform", required=True, choices=["ctfd", "rctf"], help="The platform to seed."
    )
    parser.add_argument("--url", required=True, help="The base URL of the live instance.")
    args = parser.parse_args()

    if args.platform == "ctfd":
        from ctfd_seeder import CTFdSeeder

        seeder = CTFdSeeder(base_url=args.url)
        seeder.run_seed()
    elif args.platform == "rctf":
        from rctf_seeder import RCTFSeeder

        seeder = RCTFSeeder(base_url=args.url)
        seeder.run_seed()
    else:
        raise ValueError(f"Unknown platform: {args.platform}")


if __name__ == "__main__":
    main()
