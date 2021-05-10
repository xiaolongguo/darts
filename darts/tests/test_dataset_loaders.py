import os

from darts import TimeSeries
from darts.datasets import (
    AirPassengersDataset, AusBeerDataset, #EnergyDataset,
    HeartRateDataset, IceCreamHeaterDataset, MonthlyMilkDataset,
    SunspotsDataset, TaylorDataset, TemperatureDataset,
    USGasolineDataset, WineDataset, WoolyDataset
)
from darts.datasets.dataset_loaders import (
    DatasetLoadingException,
    DatasetLoaderCSV,
    DatasetLoaderMetadata,
    DatasetLoader
)
from darts.tests.base_test_class import DartsBaseTestClass

datasets = [
    AirPassengersDataset, AusBeerDataset,
    HeartRateDataset, IceCreamHeaterDataset, MonthlyMilkDataset,
    SunspotsDataset, TaylorDataset, TemperatureDataset,
    USGasolineDataset, WineDataset, WoolyDataset
]

width_datasets = [
    1, 1,
    1, 2, 1,
    1, 1, 1,
    1, 1, 1
]

wrong_hash_dataset = DatasetLoaderCSV(
    metadata=DatasetLoaderMetadata(
        "wrong_hash",
        uri="https://raw.githubusercontent.com/unit8co/darts/master/examples/AirPassengers.csv",
        hash="will fail",
        header_time="Month",
        format_time="%Y-%m"
    )
)

wrong_url_dataset = DatasetLoaderCSV(
    metadata=DatasetLoaderMetadata(
        "wrong_url",
        uri="https://AirPassengers.csv",
        hash="167ffa96204a2b47339c21eea25baf32",
        header_time="Month",
        format_time="%Y-%m"
    )
)


class DatasetLoaderTestCase(DartsBaseTestClass):
    def tearDown(self):
        # we need to remove the cached datasets between each test
        default_directory = DatasetLoader._DEFAULT_DIRECTORY
        for f in os.listdir(default_directory):
            os.remove(os.path.join(default_directory, f))
        os.rmdir(DatasetLoader._DEFAULT_DIRECTORY)

    def test_ok_dataset(self):
        for width, dataset in zip(width_datasets, datasets):
            ts: TimeSeries = dataset.load()
            self.assertEqual(ts.width, width)

    def test_hash(self):
        with self.assertRaises(DatasetLoadingException):
            wrong_hash_dataset.load()

    def test_uri(self):
        with self.assertRaises(DatasetLoadingException):
            wrong_url_dataset.load()
