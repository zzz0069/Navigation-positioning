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
        input = {'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        expected = {'altitude':'45d11.9', 'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_040_ShouldReturnAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_050_ShouldReturnAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test100_910_ShouldReturnNoOpError(self):
        input = {}
        output = {'error': 'no op is specified'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_930_ShouldReturnErrorIfInputIsNotDict(self):
        input = 42
        output = {'error':'parameter is not a dictionary'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_940_ShouldReturnIllegalOpError(self):
        input = {'op': 'unknown'}
        output = { 'op': 'unknown', 'error':'op is not a legal operation'}
        self.assertDictEqual(dp.dispatch(input), output)

    def test100_950_ShouldReturnDictMissingError(self):
        output = {'error':'parameter is missing'}
        self.assertDictEqual(dp.dispatch(), output)

    def test200_020_ShouldReturnCalcuatedAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_030_ShouldReturnCalcuatedAltitude(self):
        input = {'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        expected = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_910_ShouldReturnMandatoryElemMissingError(self):
        input = {'op': 'adjust'}
        expected = {'op': 'adjust', 'error':'mandatory information is missing'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_920_ShouldReturnInvalidObservationError(self):
        input = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '101d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'observation is invalid'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_910_ShouldReturnInvalidHeightError(self):
        input = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'height is invalid'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_920_ShouldReturnInvalidHorizonError(self):
        input = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': '6', 'horizon': '   ', 'pressure': '1010', 'op': 'adjust', 'temperature': '71', 'error':'horizon is invalid'}
        self.assertDictEqual(dp.adjust(input), expected)

    def test200_930_ShouldReturnInvalidHorizonError(self):
        input = {'observation': '45d15.2', 'height': '6', 'horizon': 2, 'pressure': '1010', 'op': 'adjust', 'temperature': '71'}
        expected = {'observation': '45d15.2', 'height': '6', 'horizon': 2, 'pressure': '1010', 'op': 'adjust', 'temperature': '71', 'error':'horizon is invalid'}
        self.assertDictEqual(dp.adjust(input), expected)

    def shouldReturnErrorIfAltitudeExists(self):
        input = {'altitude': 'something'}
        expected = {'altitude': 'something', 'error': 'altitude already exists in the input'}
        actual = dp.adjust(input)
        self.assertDictEqual(expected, actual)

    def shouldReturnErrorIfObservationDoesNotExist(self):
        input = { ''}

