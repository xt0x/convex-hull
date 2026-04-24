from __future__ import annotations

import argparse

from convex_full.visualize import load_points_from_json, save_convex_hull_plot


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


def main() -> int:
    args = build_parser().parse_args()
    points = load_points_from_json(args.input)
    output = save_convex_hull_plot(points, args.output, title=args.title, dpi=args.dpi)
    print(f"saved plot to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
