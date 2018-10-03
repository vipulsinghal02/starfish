import argparse
from typing import Type

from starfish.codebook.codebook import Codebook
from starfish.intensity_table.intensity_table import IntensityTable
from starfish.pipeline import AlgorithmBase, PipelineComponent
from starfish.util.argparse import FsExistsType
from . import _base
from . import per_round_max_channel_decoder


class Decoder(PipelineComponent):

    decoder_group: argparse.ArgumentParser

    @classmethod
    def _get_algorithm_base_class(cls) -> Type[AlgorithmBase]:
        return _base.DecoderAlgorithmBase

    @classmethod
    def add_to_parser(cls, subparsers):
        """Adds the decoder component to the CLI argument parser."""
        decoder_group = subparsers.add_parser("decode")
        decoder_group.add_argument("-i", "--input", type=FsExistsType(), required=True)
        decoder_group.add_argument("-o", "--output", required=True)
        decoder_group.add_argument("--codebook", type=FsExistsType(), required=True)
        decoder_group.set_defaults(starfish_command=Decoder._cli)
        decoder_subparsers = decoder_group.add_subparsers(dest="decoder_algorithm_class")

        for algorithm_cls in cls._algorithm_to_class_map().values():
            group_parser = decoder_subparsers.add_parser(algorithm_cls._get_algorithm_name())
            group_parser.set_defaults(decoder_algorithm_class=algorithm_cls)
            algorithm_cls._add_arguments(group_parser)

        cls.decoder_group = decoder_group

    @classmethod
    def _cli(cls, args, print_help=False):
        """Runs the decoder component based on parsed arguments."""

        if args.decoder_algorithm_class is None or print_help:
            cls.decoder_group.print_help()
            cls.decoder_group.exit(status=2)

        instance = args.decoder_algorithm_class(**vars(args))

        # load intensities and codebook
        intensities = IntensityTable.load(args.input)
        codebook = Codebook.from_json(args.codebook)

        # decode and save output
        intensities = instance.run(intensities, codebook)
        intensities.save(args.output)
