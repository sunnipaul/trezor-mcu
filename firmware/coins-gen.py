#!/usr/bin/env python2
from __future__ import print_function
import json, sys

coins_json = json.load(open('coins.json', 'r'))

coins_stable, coins_debug = [], []

if len(sys.argv) != 2 or sys.argv[1] not in ("count", "array"):
    print("usage: coins-gen.py [count|array]\n", file=sys.stderr)
    sys.exit(1)


def get_fields(coin):
    return [
        'true' if coin['coin_name'] is not None else 'false',
        '"%s"' % coin['coin_name'] if coin['coin_name'] is not None else 'NULL',

        'true' if coin['coin_shortcut'] is not None else 'false',
        '" %s"' % coin['coin_shortcut'] if coin['coin_shortcut'] is not None else 'NULL',

        'true' if coin['address_type'] is not None else 'false',
        '%d' % coin['address_type'] if coin['address_type'] is not None else '0',

        'true' if coin['maxfee_kb'] is not None else 'false',
        '%d' % coin['maxfee_kb'] if coin['maxfee_kb'] is not None else '0',

        'true' if coin['address_type_p2sh'] is not None else 'false',
        '%d' % coin['address_type_p2sh'] if coin['address_type_p2sh'] is not None else '0',

        'true' if coin['signed_message_header'] is not None else 'false',
        '"\\x%02x" "%s"' % (len(coin['signed_message_header']), coin['signed_message_header'].replace('\n', '\\n')) if coin['signed_message_header'] is not None else 'NULL',

        'true' if coin['xpub_magic'] is not None else 'false',
        '0x%s' % coin['xpub_magic'] if coin['xpub_magic'] is not None else '00000000',

        'true' if coin['xprv_magic'] is not None else 'false',
        '0x%s' % coin['xprv_magic'] if coin['xprv_magic'] is not None else '00000000',

        'true' if coin['segwit'] is not None else 'false',
        'true' if coin['segwit'] else 'false',

        'true' if coin['forkid'] is not None else 'false',
        '%d' % coin['forkid'] if coin['forkid'] else '0'
    ]


def justify_width(coins):
    for j in range(len(coins[0])):
        l = max([len(x[j]) for x in coins]) + 1
        for i in range(len(coins)):
            if coins[i][j][0] in '0123456789':
                coins[i][j] = (coins[i][j] + ',').rjust(l)
            else:
                coins[i][j] = (coins[i][j] + ',').ljust(l)


for coin in coins_json:
    if coin['firmware'] == 'stable':
        coins_stable.append(get_fields(coin))
    if coin['firmware'] == 'debug':
        coins_debug.append(get_fields(coin))

justify_width(coins_stable)
justify_width(coins_debug)

print("// THIS IS A GENERATED FILE - DO NOT HAND EDIT\n\n")

if sys.argv[1] == "array":
    for row in coins_stable:
        print('\t{' + ' '.join(row) + ' },')

    print('#if DEBUG_LINK')

    for row in coins_debug:
        print('\t{' + ' '.join(row) + ' },')

    print('#endif')


if sys.argv[1] == "count":
    print('#if DEBUG_LINK')
    print('#define COINS_COUNT %d' % (len(coins_stable) + len(coins_debug)))
    print('#else')
    print('#define COINS_COUNT %d' % (len(coins_stable)))
    print('#endif')
