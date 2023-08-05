import rasterio
from rasterio.plot import show


def plot(file, **kwargs):
    with rasterio.open(file) as dataset:
        show(dataset, **kwargs)
