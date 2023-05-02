import json

SPEC_NAMES = [
    'assassin',
    'combat',
    'enhance',
    'dw_unholy',
    'feral',
    'frost',
    'fury',
    'mm',
    'ret',
    'surv',
]

def settings_for_spec(spec):
    if spec not in SPEC_NAMES:
        raise ValueError(f'Unknown spec {spec}')
    base_settings = json.load(open(f'data/p4_{spec}.json'))
    del base_settings['raid']['parties'][0]['players'][0]['database']
    return base_settings

def items_for_phase(phase):
    items = json.load(open(f'data/{phase}_bis.json'))
    return items

def set_items(settings, items):
    settings['raid']['parties'][0]['players'][0]['equipment']['items'] = items

def set_trinkets(settings, trinkets):
    settings['raid']['parties'][0]['players'][0]['equipment']['items'][12] = {'id': trinkets[0]}
    settings['raid']['parties'][0]['players'][0]['equipment']['items'][13] = {'id' :trinkets[1]}

