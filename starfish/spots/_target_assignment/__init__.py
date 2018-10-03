import argparse
import json
import os
from typing import List, Type

from starfish.intensity_table.intensity_table import IntensityTable
from starfish.pipeline import AlgorithmBase, PipelineComponent
from starfish.util.argparse import FsExistsType
from . import point_in_poly
from ._base import TargetAssignmentAlgorithm


class TargetAssignment(PipelineComponent):

    target_assignment_group: argparse.ArgumentParser

    @classmethod
    def _get_algorithm_base_class(cls) -> Type[AlgorithmBase]:
        return TargetAssignmentAlgorithm

    @classmethod
    def add_to_parser(cls, subparsers) -> None:
        """Adds the target_assignment component to the CLI argument parser."""
        target_assignment_group = subparsers.add_parser("target_assignment")
        target_assignment_group.add_argument(
            "--coordinates-geojson", type=FsExistsType(), required=True)
        target_assignment_group.add_argument("--intensities", type=FsExistsType(), required=True)
        target_assignment_group.add_argument("-o", "--output", required=True)
        target_assignment_group.set_defaults(starfish_command=TargetAssignment._cli)
        target_assignment_group = target_assignment_group.add_subparsers(
            dest="target_assignment_algorithm_class")

        for algorithm_cls in cls._algorithm_to_class_map().values():
            group_parser = target_assignment_group.add_parser(algorithm_cls._get_algorithm_name())
            group_parser.set_defaults(target_assignment_algorithm_class=algorithm_cls)
            algorithm_cls._add_arguments(group_parser)

        cls.target_assignment_group = target_assignment_group

    @classmethod
    def _cli(cls, args, print_help=False) -> None:
        """Runs the target_assignment component based on parsed arguments."""
        from starfish import munge

        if args.target_assignment_algorithm_class is None or print_help:
            cls.target_assignment_group.print_help()
            cls.target_assignment_group.exit(status=2)

        with open(args.coordinates_geojson, "r") as fh:
            coordinates = json.load(fh)
        regions = munge.geojson_to_region(coordinates)

        print('Assigning targets to cells...')
        intensity_table = IntensityTable.load(args.intensities)

        instance = args.target_assignment_algorithm_class(**vars(args))

        intensities = instance.run(intensity_table, regions)

        print("Writing intensities, including cell ids to {}".format(args.output))
        intensities.save(os.path.join(args.output))
