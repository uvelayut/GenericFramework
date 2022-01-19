#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     PortalLoginPage Class Implementation
"""

__author__ = "Biju Aramban"
__credits__ = ["Biju Aramban", ]
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Testing"
__date__ = '2019-08-16T20:49:05'


from collections import OrderedDict


class IndexedOrderedDict(OrderedDict):

    def __init__(self, args):
        super(IndexedOrderedDict, self).__init__(args)
        return

    def __len__(self):
        return len(self.items())

    def __str__(self):
        items_list = ["%s: %s" % (key, value) for key, value in self.items()]
        return "%s(%s)" % (self.__class__.__name__, repr(items_list))

    def items(self):
        list(super(IndexedOrderedDict, self).items())


def test_IndexedOrderedDict():
    iod_dict = IndexedOrderedDict(zip([1, 2, 3, 4, 5,], ['a', 'b', 'c', 'd', 'e',]))
    items = iod_dict.items()
    print('Type: %s | Content: %s' % (type(iod_dict.items()), iod_dict.items()))


if __name__ == '__main__':
    test_IndexedOrderedDict()
