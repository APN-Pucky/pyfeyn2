"""Moved to :py:mod:`feynml.interface.hepmc`"""
from feynml.interface.hepmc import hepmc_event_to_feynman as _event_to_feynman
from smpl.doc import deprecated

event_to_feynman = deprecated(
    "2.2.6", "Directly use feynml.interface.hepmc.hepmc_event_to_feynman()"
)(_event_to_feynman)
