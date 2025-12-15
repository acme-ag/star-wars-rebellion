import numpy as np
import random
from collections import Counter
import re
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

ground_unit_stats = {
    'AT-AT': {'defense_red': 3, 'attack_black': 1, 'attack_red': 2},
    'AT-ST': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Speeder': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Soldier': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0}
}

space_unit_stats = {
    'Star Destroyer': {'defense_red': 4, 'attack_black': 1, 'attack_red': 2},
    'Carrier': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Mon-Calamari Cruiser': {'defense_red': 4, 'attack_black': 1, 'attack_red': 2},
    'Corellian corvette': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Tie-Fighter': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0},
    'X-Wing': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0},
    'Y-Wing': {'defense_black': 1, 'attack_black': 0, 'attack_red': 1}
}

# ground / space units
unit_stats = ground_unit_stats
red_die = ['direct', 'red', 'red', 'block', None, None]
black_die = ['direct', 'black', 'black', 'block', None, None]

# unit_stats = space_unit_stats
def outcome(red_die_num, black_die_num):
    red_roll = random.choices(red_die, k=red_die_num)
    black_roll = random.choices(black_die, k=black_die_num)

    # we need to return 4 numbers: direct damage, red damage, black damage and block

    all_rolls = red_roll + black_roll
    counts = Counter(all_rolls)

    direct = counts['direct']
    red = counts['red']
    black = counts['black']
    block = counts['block']

    return direct, red, black, block

def expand_units(counter, unit_stats):
    unit_list = []
    for unit_name, count in counter.items():
        for _ in range(count):
            unit = unit_stats[unit_name].copy()
            unit['name'] = unit_name
            unit['hp'] = unit.get('defense_red', unit.get('defense_black'))
            unit_list.append(unit)
    return unit_list


# sorting
def sort_by_defense(unit):
    return unit.get('defense_red', unit.get('defense_black'))


def total_dice(attackers, defenders):
    # first calculate total dice for attackers
    a_total_red_dice = 0
    a_total_black_dice = 0

    for i in attackers:
        a_total_red_dice += i['attack_red']
        a_total_black_dice += i['attack_black']

    # same for defenders
    d_total_red_dice = 0
    d_total_black_dice = 0

    for i in defenders:
        d_total_red_dice += i['attack_red']
        d_total_black_dice += i['attack_black']

    # first group: atttackers; then: defenders
    return (a_total_red_dice, a_total_black_dice), (d_total_red_dice, d_total_black_dice)


# here's our main distinction from the previous versions
def assign_damage(units, direct_hits, red_hits, black_hits, block_hits):
    updated_units = []

    # block direct hits first -- most dangerous, -- then colored hits.
    remaining_blocks = block_hits

    direct_remaining = max(direct_hits - remaining_blocks, 0)
    remaining_blocks = max(remaining_blocks - direct_hits, 0)

    red_remaining = max(red_hits - remaining_blocks, 0)
    remaining_blocks = max(remaining_blocks - red_hits, 0)

    black_remaining = max(black_hits - remaining_blocks, 0)

    # apply blocks
    total_hits = {
        'direct': direct_remaining,
        'red': red_remaining,
        'black': black_remaining
    }

    for unit in units:
        hp = unit['hp']

        # direct hits
        while total_hits['direct'] > 0 and hp > 0:
            hp -= 1
            total_hits['direct'] -= 1

        # Color hits
        if hp > 0:
            if 'defense_red' in unit:
                while total_hits['red'] > 0 and hp > 0:
                    hp -= 1
                    total_hits['red'] -= 1
            elif 'defense_black' in unit:
                while total_hits['black'] > 0 and hp > 0:
                    hp -= 1
                    total_hits['black'] -= 1

        if hp > 0:
            unit['hp'] = hp
            updated_units.append(unit)

    return updated_units


def multiple_combat(attackers, defenders, verbose=False):
    # sort to have an order from strongest to weakest units
    sorted_attackers = sorted(attackers, key=lambda unit: unit.get('defense_red', unit.get('defense_black')),
                              reverse=True)
    sorted_defenders = sorted(defenders, key=lambda unit: unit.get('defense_red', unit.get('defense_black')),
                              reverse=True)

    for unit in sorted_attackers:
        if 'hp' not in unit:
            # unit['hp'] = unit.get('defense_red') or unit.get('defense_black')
            unit['hp'] = unit.get('defense_red') if 'defense_red' in unit else unit.get('defense_black', 0)

    for unit in sorted_defenders:
        if 'hp' not in unit:
            # unit['hp'] = unit.get('defense_red') or unit.get('defense_black')
            unit['hp'] = unit.get('defense_red') if 'defense_red' in unit else unit.get('defense_black', 0)

    if verbose:
        debug_container = st.expander("Combat round-by-round debug log")
    else:
        debug_container = None

    round_num = 1
    while sorted_attackers and sorted_defenders:
        (a_red, a_black), (d_red, d_black) = total_dice(sorted_attackers, sorted_defenders)
        a_direct, a_red, a_black, a_block = outcome(a_red, a_black)
        d_direct, d_red, d_black, d_block = outcome(d_red, d_black)

        sorted_defenders = assign_damage(sorted_defenders, a_direct, a_red, a_black, d_block)
        sorted_attackers = assign_damage(sorted_attackers, d_direct, d_red, d_black, a_block)

        if debug_container:
            with debug_container:
                st.markdown(f"### Round {round_num}")
                st.text(f"Empire rolls:  direct={a_direct}, red={a_red}, black={a_black}, block={a_block}")
                st.text(f"Rebels rolls:  direct={d_direct}, red={d_red}, black={d_black}, block={d_block}")
                st.text(f"Empire remaining: {[u['name'] + '(' + str(u['hp']) + ')' for u in sorted_attackers]}")
                st.text(f"Rebels remaining: {[u['name'] + '(' + str(u['hp']) + ')' for u in sorted_defenders]}")
                st.markdown("---")

        round_num += 1

    return sorted_attackers, sorted_defenders
