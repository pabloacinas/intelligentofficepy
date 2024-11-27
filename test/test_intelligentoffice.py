import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):


    """
    The office is divided into four quadrants. On the ceiling of each quadrant, there is an infrared distance sensor that detects the presence of a worker in that quadrant.

The infrared distance sensors are connected, respectively, to pins 11, 12, 13, and 15 (BOARD mode). The communication with the sensors happens via the GPIO.input(channel) function (where channel is the pin). Specifically, this function returns True if a worker is detected by the sensor, False otherwise.

Note that the sensors have already been set up in the constructor of the IntelligentOffice class.
    """

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
