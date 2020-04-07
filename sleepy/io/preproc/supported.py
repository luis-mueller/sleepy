from sleepy.processing.algorithms import Massimi, Walkthrough
from sleepy.processing.filters import BandPassFilter
from sleepy.io.matfiles.core import MatDataset

SUPPORTED_ALGORITHMS = [
    Massimi,
    Walkthrough
]

SUPPORTED_FILTERS = [
    BandPassFilter
]

SUPPORTED_DATASETS = {
    'MAT' : MatDataset
}
