import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

from vatu.config import Config
from vatu.engine.metrics import persist, get_metric


class TestMetrics(TestCase):
    @patch('time.time', return_value=123456.123456)
    def test_get_metric(self, time):
        metric = get_metric('a.b.c', '1')
        self.assertEqual(metric['timestamp'], 123456123456)
        self.assertEqual(metric['name'], 'a.b.c')
        self.assertEqual(metric['value'], '1')

    @patch('time.time', return_value=123456.123456)
    def test_persist(self, time):
        with tempfile.TemporaryDirectory() as d:
            Config.update({'metrics': {'outputdir': d}})
            persist([
                get_metric('a.b.c', '1'),
                get_metric('e', '2'),
            ])
            with open(os.path.join(d, 'vatu-123456123456.metrics')) as metricsfile:
                metrics = metricsfile.readlines()
                self.assertEqual(metrics[0], '123456123456// a.b.c{} 1\n')
                self.assertEqual(metrics[1], '123456123456// e{} 2\n')
