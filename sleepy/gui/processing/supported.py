from sleepy.processing.algorithms import Massimi, Walkthrough, Relative
from sleepy.processing.filters import BandPassFilter
from sleepy.processing.mat.core import MatDataset

SUPPORTED_ALGORITHMS = [
    Massimi,
    Walkthrough,
    Relative
]

SUPPORTED_FILTERS = [
    BandPassFilter
]

SUPPORTED_DATASETS = {
    'MAT' : MatDataset
}
