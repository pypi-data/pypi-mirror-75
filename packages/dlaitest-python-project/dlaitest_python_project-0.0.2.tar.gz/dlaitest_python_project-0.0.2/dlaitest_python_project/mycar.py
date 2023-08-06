#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import json
import logging


class Car:
    def __init__(self, year, make, speed):
        self.__year_model = year
        self.__make = make
        self.__speed = 0

    # Setter
    def set_year_model(self, year):
        self.__year_model = year

    def set_make(self, make):
        self.__make = make

    def set_speed(self, speed):
        self.__speed = 0

    # Getter
    def get_year_model(self):
        return self.__year_model

    def get_make(self):
        return self.__make

    def get_speed(self):
        return self.__speed

    # methods
    def accelerate(self):
        self.__speed += 5

    def brake(self):
        self.__speed -= 5
