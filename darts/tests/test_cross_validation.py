import unittest
import logging
from ..utils.cross_validation import generalized_rolling_origin_evaluation as groe
from ..models import ExponentialSmoothing, NaiveSeasonal
from ..utils.timeseries_generation import (random_walk_timeseries as rt, constant_timeseries as ct,
                                           sine_timeseries as st, linear_timeseries as lt)
from ..metrics import mape, mae
import numpy as np
import pandas as pd


class CrossValidationTestCase(unittest.TestCase):
    series0 = ct(value=0, length=50)
    series1 = rt(length=50)
    series2 = st(value_frequency=10, length=50)
    series3 = lt(length=50)
    model1 = NaiveSeasonal()
    model2 = ExponentialSmoothing(seasonal_periods=10)

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    def test_groe_input_metric(self):
        groe(self.series1, self.model1, metric=mape, stride=5)
        groe(self.series1, self.model1, metric='mape', stride=5)
        groe(self.series1, self.model1,
             metric=lambda ts1, ts2: 0.5 * mape(ts1, ts2) + 0.5 * mae(ts1, ts2), stride=5)
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric='plop', stride=5)

    def test_groe_input_params(self):
        groe(self.series1, self.model1, metric=mape, stride=5, n_prediction_steps=9)
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape)
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape, stride=-5, n_prediction_steps=10)

    def test_groe_input_origin(self):
        # small time series
        groe(self.series1, self.model1, metric=mape, stride=1, first_origin=2)
        groe(self.series1, self.model1, metric=mape, stride=1, first_origin=48)
        # impossible values
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape, stride=1, first_origin=52)
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape, stride=1, first_origin=0)

    def test_groe_input_timestamp(self):
        # small time series
        groe(self.series1, self.model1, metric=mape, stride=1, first_origin=pd.Timestamp('2000-01-03'))
        groe(self.series1, self.model1, metric=mape, stride=1, first_origin=pd.Timestamp('2000-02-18'))
        # impossible values
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape, stride=1, first_origin=pd.Timestamp('2000-02-25'))
        with self.assertRaises(ValueError):
            groe(self.series1, self.model1, metric=mape, stride=1, first_origin=pd.Timestamp('2000-01-01'))

    def test_groe_inf_output(self):
        # metric
        self.assertEqual(np.inf, groe(self.series0, self.model1, metric=mape, stride=1))
        # model
        self.assertEqual(np.inf, groe(self.series2, self.model2, metric=mape, first_origin=5, stride=1))

    def test_groe_ouput(self):
        value = groe(self.series2 + self.series3, self.model1, first_origin=35, n_prediction_steps=6, forecast_horizon=10)
        self.assertAlmostEqual(value, 6 * 55)


if __name__ == '__main__':
    unittest.main()