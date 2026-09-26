"""
Config file for bank cards.
Has all the info about supported bank systems, their banks and e.t.c.
"""

PAYMENT_SYSTEMS = {
    [34, 37]:"American Express",
    [62, 81]:"China UnionPay",
    [n for n in range(2221, 2720+1)]:"Mastercard",
    []:"MIR",
    4:"Visa",
}

