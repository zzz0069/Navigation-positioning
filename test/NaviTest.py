from unittest import TestCase
from softwareprocess import dispatch as dp

class NavigationTest(TestCase):

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
        output = {'error':'mandatory information is missing'}
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
