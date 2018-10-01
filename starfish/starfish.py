#!/usr/bin/env python

import argparse
import cProfile
from pstats import Stats

from starfish.experiment.builder.cli import Cli as BuilderCli
from starfish.image import (
    Filter,
    Registration,
    Segmentation,
)
from starfish.orgjson import OrgJsonCommand
from starfish.spots import (
    Decoder,
    SpotFinder,
    TargetAssignment,
)
from validate_sptx.cli import Cli as ValidateCli
from .util.argparse import FsExistsType


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--profile", action="store_true", help="enable profiling")
    parser.add_argument(
        "--noop",
        help=argparse.SUPPRESS,
        dest="starfish_command",
        action="store_const",
        const=noop
    )

    subparsers = parser.add_subparsers(dest="starfish_command")

    Registration._add_to_parser(subparsers)
    Filter._add_to_parser(subparsers)
    SpotFinder.add_to_parser(subparsers)
    Segmentation._add_to_parser(subparsers)
    TargetAssignment.add_to_parser(subparsers)
    Decoder.add_to_parser(subparsers)

    show_group = subparsers.add_parser("show")
    show_group.add_argument("in_json", type=FsExistsType())
    show_group.add_argument("--sz", default=10, type=int, help="Figure size")
    show_group.set_defaults(starfish_command=show)

    build_group = subparsers.add_parser("build")
    BuilderCli.add_to_parser(build_group)

    validate_group = subparsers.add_parser("validate")
    ValidateCli.add_to_parser(validate_group)

    OrgJsonCommand.add_to_parser(subparsers)

    return parser


PROFILER_KEY = "profiler"
"""This is the dictionary key we use to attach the profiler to pass to the resultcallback."""
PROFILER_LINES = 15
"""This is the number of profiling rows to dump when --profile is enabled."""


def starfish():
    parser = build_parser()
    args, argv = parser.parse_known_args()

    art = """
         _              __ _     _
        | |            / _(_)   | |
     ___| |_ __ _ _ __| |_ _ ___| |__
    / __| __/ _` | '__|  _| / __| '_  `
    \__ \ || (_| | |  | | | \__ \ | | |
    |___/\__\__,_|_|  |_| |_|___/_| |_|

    """
    print(art)
    if args.profile:
        profiler = cProfile.Profile()
        profiler.enable()

    if args.starfish_command is None:
        parser.print_help()
        parser.exit(status=2)
    args.starfish_command(args, len(argv) != 0)

    if args.profile:
        stats = Stats(profiler)
        stats.sort_stats('tottime').print_stats(PROFILER_LINES)


def show(args, print_help=False):
    import matplotlib.pyplot as plt
    from showit import tile

    from .experiment import Experiment

    s = Experiment()
    s.read(args.in_json)
    tile(s.image.squeeze(), size=args.sz, bar=True)
    plt.show()


def noop(args, print_help=False):
    pass
