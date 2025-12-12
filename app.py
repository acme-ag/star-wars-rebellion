import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Define all units
ground_unit_stats = {
    'AT-AT': {'defense_red': 3, 'attack_black': 1, 'attack_red': 2},
    'AT-ST': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Soldier': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0},
    'Speeder': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
}

space_unit_stats = {
    'Star Destroyer': {'defense_red': 4, 'attack_black': 1, 'attack_red': 2},
    'Carrier': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Mon-Calamari Cruiser': {'defense_red': 4, 'attack_black': 1, 'attack_red': 2},
    'Corellian Corvette': {'defense_red': 2, 'attack_black': 1, 'attack_red': 1},
    'Tie-Fighter': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0},
    'X-Wing': {'defense_black': 1, 'attack_black': 1, 'attack_red': 0},
    'Y-Wing': {'defense_black': 1, 'attack_black': 0, 'attack_red': 1},
}
battle_type = st.radio("Choose battle type", ["Ground", "Space"])

if battle_type == "Ground":
    unit_stats = ground_unit_stats
    empire_unit_types = ['AT-AT', 'AT-ST', 'Soldier']
    rebel_unit_types = ['Speeder', 'Soldier']
else:
    unit_stats = space_unit_stats
    empire_unit_types = ['Star Destroyer', 'Carrier', 'Tie-Fighter']
    rebel_unit_types = ['Mon-Calamari Cruiser', 'Corellian Corvette', 'X-Wing', 'Y-Wing']

unit_types = list(unit_stats.keys())
# Define valid unit types per side
# empire_unit_types = ['AT-AT', 'AT-ST', 'Soldier']
# rebel_unit_types = ['Speeder', 'Soldier']

st.title("Star Wars: Rebellion combat simulator")

with st.sidebar:
    st.header("Simulation Setup")

    sim_count = st.number_input("Number of simulations", 1000, 100000, 10000, step=1000)

    st.subheader("Empire (Attackers)")
    empire_units = defaultdict(int)
    for i in range(3):
        unit = st.selectbox(f"Empire unit {i + 1}", empire_unit_types, key=f"empire_unit_{i}")
        count = st.number_input(f"How many {unit}?", 0, 10, 1, key=f"empire_count_{i}")
        empire_units[unit] += count

    st.subheader("Rebels (Defenders)")
    rebel_units = defaultdict(int)
    for i in range(4):
        unit = st.selectbox(f"Rebel unit {i + 1}", rebel_unit_types, key=f"rebel_unit_{i}")
        count = st.number_input(f"How many {unit}?", 0, 10, 1, key=f"rebel_count_{i}")
        rebel_units[unit] += count

# visual confirmation
# st.write("Empire units selected:", dict(empire_units))
# st.write("Rebel units selected:", dict(rebel_units))

start = st.button("Start simulation")

if start:
    from simulation import expand_units, multiple_combat

    results = []
    for _ in range(sim_count):
        attackers = expand_units(Counter(empire_units), unit_stats)
        defenders = expand_units(Counter(rebel_units), unit_stats)
        combat_result = multiple_combat(attackers, defenders)
        result = (len(combat_result[0]), len(combat_result[1]))  # attackers, defenders
        results.append(result)

    empire_rebellion_outcome = [0, 0, 0]
    for i in results:
        if i[0] > 0 and i[1] < 1:
            empire_rebellion_outcome[0] += 1
        elif i[0] < 1 and i[1] > 0:
            empire_rebellion_outcome[1] += 1
        else:
            empire_rebellion_outcome[2] += 1

    # empire_rebellion_outcome
    empire_ratio = round((empire_rebellion_outcome[0] / len(results)) * 100, 2)
    rebel_ratio = round((empire_rebellion_outcome[1] / len(results)) * 100, 2)
    draw_ratio = round((empire_rebellion_outcome[2] / len(results)) * 100, 2)

    st.subheader("Simulation results")
    st.write(f"Empire wins in {empire_ratio}%")
    st.write(f"Rebels win in {rebel_ratio}% combats.")
    st.write(f"{draw_ratio}% of draw combats ")

    # statistics
    df = pd.DataFrame(results, columns=["Empire", "Rebels"])
    outcome_counts = df.value_counts().reset_index(name='Frequency')
    outcome_counts['Outcome'] = 'E' + outcome_counts['Empire'].astype(str) + '_R' + outcome_counts['Rebels'].astype(
        str)
    outcome_counts = outcome_counts.sort_values(by='Frequency', ascending=False)

    #
    # # Show histogram
    st.write("Aggregated statistics")

    st.dataframe(outcome_counts)

    plt.figure(figsize=(10, 6))
    plt.bar(outcome_counts['Outcome'], outcome_counts['Frequency'])
    plt.xlabel('Battle outcomes')
    plt.ylabel('Frequency')
    plt.title('Battle outcomes: Empire vs Rebellion')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # render it in streamlit
    st.pyplot(plt)
