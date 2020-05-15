#!/usr/bin/env python3
from time import sleep

class RoutingController:
    WAREHOUSE_MAP = {
        'Start' : [
            {
                'left': 'B'
            }, {
                'right': 'A'
            }, {
                'forward': 'cross2'
            }
        ],
        'A' : [
            {
                'left': 'Start'
            }, {
                'right': 'cross2'
            }, {
                'forward': 'B'
            }
        ],
        'B' : [
            {
                'left': 'cross2'
            }, {
                'right': 'Start'
            }, {
                'forward': 'A'
            }
        ],
        'cross2' : [
            {
                'left': 'D'
            }, {
                'right': 'C'
            }, {
                'forward': 'End'
            }
        ],
        'C' : [
            {
                'left': 'cross1'
            }, {
                'right': 'End'
            }, {
                'forward': 'D'
            }
        ],
        'D' : [
            {
                'left': 'End'
            }, {
                'right': 'cross1'
            }, {
                'forward': 'C'
            }
        ],
        'cross1' : [
            {
                'left': 'A'
            }, {
                'right': 'B'
            }, {
                'forward': 'Start'
            }
        ],
        'End' : [
            {
                'left': 'C'
            }, {
                'right': 'D'
            }, {
                'forward': 'cross1'
            }
        ]
    }

    def __init__(self, start, end):
        #set wheel motor for MovementController
        self.start = start
        self.end = end
        self.route = []

    def setStart(self, start):
        self.start = start

    def setEnd(self, end):
        self.end = end

    def resetRoute(self):
        self.route = []

    def findPath(self, start='', end=''):
        self.resetRoute()
        if (start == ''):
            start = self.start

        if (end == ''):
            end = self.end

        tmpKey = ""
        tmpValue = ""
        found = 0
        finish = 0
        while not finish:
            for key, value in self.WAREHOUSE_MAP.items():
                if (key == start):
                    for value1 in value:
                        for key2,value2 in value1.items():
                            if ('cross' in value2):
                                tmpKey = key2
                                tmpValue = value2

                            if (end == value2):
                                found = 1
                                finish = 1
                                self.route.append(key2)
                    if (found == 0):
                        start = tmpValue
                        self.route.append(tmpKey)
                        break
        return self.route
