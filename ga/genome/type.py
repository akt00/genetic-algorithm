from typing import TypeAlias
from xml.dom.minidom import Document, Element, DOMImplementation
import numpy as np


GeneSeed: TypeAlias = np.ndarray[float, any]
DNA: TypeAlias = list[GeneSeed]
GeneSpec: TypeAlias = dict[str, dict]
Gene: TypeAlias = dict[str, float]
Genome: TypeAlias = list[Gene]

DEFAULT_GENE_SPEC: GeneSpec = {"link-shape": {"scale": 1},
                               "link-length": {"scale": 2},
                               "link-radius": {"scale": 1},
                               "link-recurrence": {"scale": 3},
                               "link-mass": {"scale": 1},
                               "joint-type": {"scale": 1},
                               "joint-parent": {"scale": 1},
                               "joint-axis-xyz": {"scale": 1},
                               "joint-origin-rpy-1": {"scale": np.pi * 2},
                               "joint-origin-rpy-2": {"scale": np.pi * 2},
                               "joint-origin-rpy-3": {"scale": np.pi * 2},
                               "joint-origin-xyz-1": {"scale": 1},
                               "joint-origin-xyz-2": {"scale": 1},
                               "joint-origin-xyz-3": {"scale": 1},
                               "control-waveform": {"scale": 1},
                               "control-amp": {"scale": 0.25},
                               "control-freq": {"scale": 1}
                               }

xmlDocument: TypeAlias = Document
xmlElement: TypeAlias = Element
xmlDom: TypeAlias = DOMImplementation
