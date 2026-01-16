from fileorg.cli import parse_args


def main():
    args = parse_args()
    print(args.directory)


if __name__ == "__main__":
    main()
