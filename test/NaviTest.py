import unittest
from softwareprocess import dispatch as dp

class NavigationTest(unittest.TestCase):

    def test_something(self):
        self.assertTrue(True)

    def test100_010_ShouldReturnAltitude(self):
        input = { 'observation': '15d04.9', 'height': '6.0', 'pressure': '1010', 'horizon': 'artificial', 'temperature': '72'}
        output = {'observation': '15d04.9', 'height': '6.0', 'pressure': '1010', 'horizon': 'artificial', 'temperature': '72', 'error':'no op is specified'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_020_ShouldReturnAltitude(self):
        input = {'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        expected = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_030_ShouldReturnAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_040_ShouldReturnAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_910_ShouldReturnError(self):
        input = {}
        output = {'error': 'no op is specified'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_920_ShouldReturnError(self):
        input = {'observation': '15d04.9', 'height': '6.0', 'pressure': '1010', 'horizon': 'artificial', 'temperature': '72'}
        output = {'observation': '15d04.9', 'height': '6.0', 'pressure': '1010', 'horizon': 'artificial', 'temperature': '72', 'error':'no op is specified'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_930_ShouldReturnError(self):
        input = 42
        output = {'error':'parameter is not a dictionary'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_940_ShouldReturnError(self):
        input = {'op': 'unknown'}
        output = { 'op': 'unknown', 'error':'op is not a legal operation'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_950_ShouldReturnError(self):
        output = {'error':'parameter is missing'}
        self.assertDictEqual(dp.dispatch(), output)

    def test100_960_ShouldReturnError(self):
        input = {'op': 'adjust'}
        output = {'op': 'adjust','error':'mandatory information is missing'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_970_ShouldReturnError(self):
        input = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        output = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'observation is invalid'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_980_ShouldReturnError(self):
        input = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        output = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'height is invalid'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_990_ShouldReturnError(self):
        input = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71'}
        output = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71', 'error':'horizon is invalid'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test200_010_ShouldPredictLongAndLat(self):
        input = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'}
        output = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42', 'long':'75d53.7', 'lat':'7d24.3'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test200_910_ShouldReturnError(self):
        input = {'op': 'predict'}
        output = {'error':'mandatory information is missing', 'op': 'predict'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test200_920_ShouldReturnError(self):
        input = {'op':'predict', 'body': 'unknown', 'date': '2016-01-17', 'time': '03:15:42'}
        output = {'op':'predict', 'body': 'unknown', 'date': '2016-01-17', 'time': '03:15:42', 'error':'star not in catalog'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test200_930_ShouldReturnError(self):
        input = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-99-17', 'time': '03:15:42'}
        output = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-99-17', 'time': '03:15:42', 'error':'invalid date'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test200_940_ShouldReturnError(self):
        input = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:99'}
        output = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:99', 'error':'invalid time'}
        self.assertDictEqual(dp.dispatch(input), output)

#correct

    def test300_010_ShouldCorrect(self):
        input = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        output = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'correctedDistance':'3950', 'correctedAzimuth':'164d42.9'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test300_910_ShouldReturnError(self):
        input = {'op':'correct'}
        output = {'error':'mandatory information is missing', 'op': 'correct'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test300_920_ShouldReturnError(self):
        input = {'op':'correct', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3'}
        output = {'op':'correct', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3', 'error':'mandatory inmformation is missing'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test300_930_ShouldReturnError(self):
        input = {'op':'correct', 'lat':'16.0d32.3', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3'}
        output = {'op':'correct', 'lat':'16.0d32.3', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3', 'error':'invalid lat'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test300_940_ShouldReturnError(self):
        input = {'op':'correct', 'lat':'16d32.3', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-153d38.4', 'assumedLong':' 74d35.3'}
        output = {'op':'correct', 'lat':'16d32.3', 'long':'95.41.6', 'altitude':'13d42.3',  'assumedLat':'-153d38.4', 'assumedLong':' 74d35.3', 'error':'invalid assumedLat'}
        self.assertDictEqual(dp.dispatch(input), output)
