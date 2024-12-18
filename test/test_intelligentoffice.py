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

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output") #led
    @patch.object(GPIO, "input") #infrared
    def test_led_is_turned_on_when_light_is_lower_than_500(self,mock_infrared: Mock, mock_led: Mock, mock_lux: Mock):
        mock_infrared.return_value = True
        mock_lux.return_value = 499
        io = IntelligentOffice()
        io.manage_light_level()
        mock_led.assert_called_with(io.LED_PIN, GPIO.HIGH)
        self.assertTrue(io.light_on)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output") #led
    @patch.object(GPIO, "input") #infrared
    def test_led_is_turned_off_when_light_is_higher_than_550(self,mock_infrared: Mock, mock_led: Mock, mock_lux: Mock):
        mock_infrared.return_value = True
        mock_lux.return_value = 551
        io = IntelligentOffice()
        io.manage_light_level()
        mock_led.assert_called_with(io.LED_PIN, GPIO.LOW)
        self.assertFalse(io.light_on)

    @patch.object(GPIO, "output") #led
    @patch.object(GPIO, "input") #infrared
    def test_led_is_turned_off_when_office_is_not_occupied(self, mock_infrared: Mock, mock_led: Mock):
        mock_infrared.return_value = False
        io = IntelligentOffice()
        io.manage_light_level()
        mock_led.assert_called_with(io.LED_PIN, GPIO.LOW)
        self.assertFalse(io.light_on)

    # Test the buzzer is turned on when the air quality is bad
    @patch.object(GPIO, "input") #smoke sensor
    @patch.object(GPIO, "output") #buzzer
    def test_buzzer_is_turned_on_when_air_quality_is_bad(self, mock_smoke: Mock, mock_buzzer: Mock):
        mock_smoke.return_value = True
        io = IntelligentOffice()
        io.monitor_air_quality()
        mock_buzzer.assert_called_with(io.BUZZER_PIN, GPIO.HIGH)
        self.assertTrue(io.buzzer_on)

