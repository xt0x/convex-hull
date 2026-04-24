from __future__ import annotations

import argparse
import sys

from convex_hull.visualize import load_points_from_json, save_convex_hull_plot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render points and their convex hull to a PNG file."
    )
    parser.add_argument("input", help="JSON file containing points")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument(
        "--title",
        default="Convex Hull",
        help="Plot title written into the PNG",
    )
    parser.add_argument(
        "--dpi",
        default=150,
        type=int,
        help="PNG resolution in dots per inch",
    )
    return parser


def _print_error(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)


def main() -> int:
    args = build_parser().parse_args()

    try:
        points = load_points_from_json(args.input)
        output = save_convex_hull_plot(
            points, args.output, title=args.title, dpi=args.dpi
        )
    except FileNotFoundError:
        _print_error(f"input file not found: {args.input}")
        return 2
    except (OSError, RuntimeError, ValueError) as exc:
        _print_error(str(exc))
        return 2

    print(f"saved plot to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
