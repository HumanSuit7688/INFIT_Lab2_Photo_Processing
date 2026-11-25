from bisect import bisect_left
from itertools import accumulate

from PIL import Image, ImageFilter


def median_filter(image: Image.Image) -> Image.Image:
    """Подавляет шум медианным фильтром с окном 3×3."""
    return image.filter(ImageFilter.MedianFilter(size=3))


def match_colors(image: Image.Image, reference: Image.Image) -> Image.Image:
    """Переносит распределение яркостей каждого канала RGB с шаблона."""
    matched_channels = [
        _match_channel(source_channel, reference_channel)
        for source_channel, reference_channel in zip(image.split(), reference.split())
    ]
    return Image.merge("RGB", matched_channels)


def _match_channel(source: Image.Image, reference: Image.Image) -> Image.Image:
    source_counts = list(accumulate(source.histogram()))
    reference_counts = list(accumulate(reference.histogram()))

    # Накопленные доли сравнимы даже у изображений разных размеров.
    reference_fractions = [count / reference_counts[-1] for count in reference_counts]
    lookup_table = [
        bisect_left(reference_fractions, count / source_counts[-1])
        for count in source_counts
    ]
    return source.point(lookup_table)
