﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from enum import IntEnum

class BracketParseAttr(IntEnum):
    """ Параметры выделения последовательности """
    NO = 0
    CANCONTAINSVERBS = 2
    """ По умолчанию, посл-ть не должна содержать чистых глаголов (если есть, то null).
     Почему так? Да потому, что это используется в основном для имён именованных
     сущностей, а там не может быть глаголов.
     Если же этот ключ указан, то глаголы не проверяются. """
    NEARCLOSEBRACKET = 4
    """ Брать первую же подходящую закрывающую кавычку """
    CANBEMANYLINES = 8
    """ Внутри могут быть переходы на новую строку (многострочный) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)