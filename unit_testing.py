import unittest
import datetime
import pandas as pd

# Reading a row from xlsx file
df = pd.read_excel('HINDALCO.xlsx').iloc[1]
df["volume"] = int(df["volume"])

# Sample Data for unit testing
unit_data = {
    "Open": df["open"],
    "High": df["high"],
    "Low": df["low"],
    "Close": df["close"],
    "Volume": df["volume"],
    "Instrument": df["instrument"],
    "Datetime": df["datetime"]
}


class TestInputData(unittest.TestCase):
    # Testing that Open, High, Low, Close is decimal
    def test_open_high_low_close(self):
        self.assertTrue(isinstance(unit_data['Open'], float))
        self.assertTrue(isinstance(unit_data['High'], float))
        self.assertTrue(isinstance(unit_data['Low'], float))
        self.assertTrue(isinstance(unit_data['Close'], float))

    # Testing that volume value is an integer
    def test_volume(self):
        self.assertTrue(isinstance(unit_data['Volume'], int))

    # Testing that the instrument value is a string
    def test_instrument(self):
        self.assertTrue(isinstance(unit_data['Instrument'], str))

    # Testing that the datetime value is a datetime
    def test_datetime(self):
        self.assertTrue(isinstance(unit_data['Datetime'], datetime.datetime))


if __name__ == '__main__':
    unittest.main()
