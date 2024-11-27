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
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN1))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_2_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN2))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_3_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN3))

    @patch.object(GPIO, "input")
    def test_check_cuadrant_4_is_occupied(self, mock_infrared: Mock):
        mock_infrared.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN4))

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

    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_are_closed_on_weekend(self, mock_read_datetime: Mock):
        mock_read_datetime.return_value = datetime(2024, 11, 30, 8, 0) #Saturday at 8:00
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertFalse(io.blinds_open)

    @patch.object(VEML7700, "lux")
    @patch.object(GPIO, "output") #led
    def test_led_is_turned_on_when_light_is_lower_than_500(self, mock_led: Mock, mock_lux: Mock):
        mock_lux.return_value = 499
        io = IntelligentOffice()
        io.manage_light_level()
        mock_led.assert_called_with(io.LED_PIN, GPIO.HIGH)
        self.assertTrue(io.light_on)
