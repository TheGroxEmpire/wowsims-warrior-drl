import json
import wowsims

def permute(elements, size):
    if size == 0:
        yield []
    else:
        for i in range(len(elements)):
            for perm in permute(elements[i+1:], size - 1):
                yield [elements[i]] + perm

def apply_item_set(settings, item_set):
    for slot, item in item_set: 
        base_item = settings['raid']['parties'][0]['players'][0]['equipment']['items'][slot]
        base_item['id'] = item
        if 'gems' in base_item: del base_item['gems'] 
        settings['raid']['parties'][0]['players'][0]['equipment']['items'][slot] = base_item

def get_socket_count(database):
    mc, rc, yc, bc = 0, 0, 0, 0
    items = database['items']
    item_sockets = [item['gemSockets'] for item in items if 'gemSockets' in item]
    for sockets in item_sockets:
        for socket in sockets:
            if socket == "GemColorMeta": mc += 1
            if socket == "GemColorRed": rc += 1
            if socket == "GemColorYellow": yc += 1
            if socket == "GemColorBlue": bc += 1
    # For belt buckle
    rc += 1
    return mc, rc, yc, bc

def get_ratings(stats):
    hit, crt, arp, exp = 12, 13, 15, 16
    final_stats = stats['raidStats']['parties'][0]['players'][0]['finalStats']['stats']
    return final_stats[hit], final_stats[crt], final_stats[arp], final_stats[exp]

def apply_gem_policy(settings):
    # Targets for each rating
    hit_t, exp_t, arp_t = 263, 214, 649
    # Get the database
    item_ids = [item['id'] for item in settings['raid']['parties'][0]['players'][0]['equipment']['items'] if 'id' in item]
    database_json = wowsims.getDatabase(item_ids, [], [])
    database = json.loads(database_json)
    sockets_map = {item['id']: item['gemSockets'] for item in database['items'] if 'gemSockets' in item}
    mc, rc, yc, bc = get_socket_count(database)
    stats = wowsims.computeStats({'raid': settings['raid']})
    hit, crt, arp, exp = get_ratings(stats)

    # Some state
    tear_used, red_used, yellow_used, blue_used = False, False, False, False
    tear_socket_color = "blue"

    # Tack how close we are to targets
    hit_needed, exp_needed, arp_needed = hit_t - hit, exp_t - exp, arp_t - arp

    # Gem counts
    arp_g, exp_g, str_g, hit_g, sht_g, sct_g, eht_g, tear_g = 0, 0, 0, 0, 0, 0, 0, 0

    # Red gems will be arp until cap, then exp, then str
    while arp_needed > 0 and rc > 0:
        arp_g += 1
        rc -= 1
        arp_needed -= 20
        red_used = True
    while exp_needed > 0 and rc > 0:
        exp_g += 1
        rc -= 1
        exp_needed -= 20
        red_used = True
    while rc > 0:
        str_g += 1
        rc -= 1
        red_used = True
    
    # Active meta with 1 yellow, 1 blue
    while yc > 0:
        yc -= 1
        if hit_needed > 10:
            hit_needed -= 20
            hit_g += 1
            yellow_used = True
        elif hit_needed > 0:
            if exp_needed > 0:
                exp_needed -= 10
                hit_needed -= 10
                eht_g += 1
            else:
                hit_needed -= 10
                sht_g += 1
            yellow_used = True
        elif bc < 1 and tear_g < 1:
            tear_g += 1
            tear_socket_color = "yellow"
            yellow_used = True
            blue_used = True
        elif arp_needed > 0:
            arp_needed -= 20
            arp_g += 1
        else:
            yellow_used = True
            sct_g += 1
    
    while bc > 0:
        bc -= 1
        if not blue_used:
            blue_used = True
            tear_g += 1
        elif arp_needed > 0:
            arp_needed -= 20
            arp_g += 1
        elif exp_needed > 0:
            exp_needed -= 20
            exp_g += 1
        else:
            str_g += 1
    
    if tear_g < 1:
        tear_g = 1

    # Actually update the gems based on the counts we've calculated
    for slot, item in enumerate(settings['raid']['parties'][0]['players'][0]['equipment']['items']):
        sockets = sockets_map.get(item['id'], []) if 'id' in item else []
        if slot == 7:
            sockets += ["GemColorRed"]
        if len(sockets) > 0:
            gems = []
            for socket_color in sockets:
                if socket_color == "GemColorMeta":
                    gems.append(41398)
                elif socket_color == "GemColorBlue":
                    if tear_socket_color == "blue" and tear_g > 0:
                        gems.append(49110)
                        tear_g -= 1
                    elif arp_g > 0:
                        gems.append(40117)
                        arp_g -= 1
                    elif exp_g > 0:
                        gems.append(40118)
                        exp_g -= 1
                    else:
                        gems.append(40111)
                        str_g -= 1
                elif socket_color == "GemColorYellow":
                    if tear_socket_color == "yellow" and tear_g > 0:
                        gems.append(49110)
                        tear_g -= 1
                    elif hit_g > 0:
                        gems.append(40125)
                        hit_g -= 1
                    elif eht_g > 0:
                        gems.append(40162)
                        eht_g -= 1
                    elif sht_g > 0:
                        gems.append(40143)
                        sht_g -= 1
                    elif sct_g > 0:
                        gems.append(40142)
                        sct_g -= 1
                    elif arp_g > 0:
                        gems.append(40117)
                        arp_g -= 1
                    else:
                        gems.append(40111)
                        str_g -= 1
                else:
                    if arp_g > 0:
                        gems.append(40117)
                        arp_g -= 1
                    elif exp_g > 0:
                        gems.append(40118)
                        exp_g -= 1
                    else:
                        gems.append(40111)
                        str_g -= 1

            settings['raid']['parties'][0]['players'][0]['equipment']['items'][slot]['gems'] = gems
