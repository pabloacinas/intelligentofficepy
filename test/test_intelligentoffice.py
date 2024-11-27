import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_cuadrant_1_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(11))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_2_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(12))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_3_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(13))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_4_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(15))

    @patch.object(SDL_DS3231, "read_datetime")
    def test_open_blinds_at_8_am(self, mock_read_datetime: Mock):
        mock_read_datetime.return_value = datetime(2024, 11, 25, 8, 0) #Monday at 8:00
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertTrue(io.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_close_blinds_at_20_pm(self, mock_read_datetime: Mock):
        mock_read_datetime.return_value = datetime(2024, 11, 25, 20, 0)
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertFalse(io.blinds_open)