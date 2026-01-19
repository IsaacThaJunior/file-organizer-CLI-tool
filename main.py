from fileorg.cli import parse_args
from fileorg.organizer import FileOrganizer


def main():
    args = parse_args()
    print(f"✓ Organizing: {args.directory}")

    organizer = FileOrganizer(args.directory, args.dry_run)
    organizer.call_funcs()


if __name__ == "__main__":
    main()
