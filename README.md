![star_wars_rebellion](https://cdn.arstechnica.net/wp-content/uploads/2016/03/IMG_3696-scaled.jpg)
## Star Wars: Rebellion 
Board game combat simulations to explore the distribution of outcomes.

Here's the streamlit [app page](https://star-wars-rebellion.streamlit.app)

This project is a Monte Carlo combat simulator for my favorite board game Star Wars: Rebellion.
It estimates battle outcome probabilities under controlled conditions by simulating thousands of dice-based combat encounters.

The simulator was created to answer a practical gameplay and analytics question:

> Given a specific unit composition, what is the statistically most likely outcome of a battle?

The idea emerged after a decisive loss in a late-game battle (this batle took place in the Rebel Base).

### Problem Statement

In this battle the Rebel side (me) had:
- 1 Air Speeder
- 6 Rebel Troopers

The Imperial side (my opponent) had:
- 1 AT-AT
- 1 AT-ST

Despite what appeared to be favorable odds for the Rebels, the Empire won without losing a single unit.

This raised several questions:
- Is targeting a weaker unit (AT-ST in this case) first the correct strategy (that is a more general queestion, not specifically related to this case)?
- How likely was such an unfavorable dice outcome?
- What is the overall probability of victory for each side in this (and other) configuration?

Since I was not able to find any ready-made tools, I built this simulator to explore these questions quantitatively.

### Modeling Assumptions

To make the problem tractable, the simulation operates under “all else being equal” conditions:
- No leaders
- No tactic cards
- No hero abilities
- Standard unit configurations only

This isolates core combat mechanics and removes external modifiers.

### Dice Mechanics

![Dice](https://i0.wp.com/www.theboardgamefamily.com/wp-content/uploads/2017/05/StarWarsRebellion_Dice.jpg)

The game uses six-sided dice in two colors: red and black (extensions with green dice are excluded for simplicity).

Each die has the following sides:
|Outcome|Count|
|-------|-----|
|Direct damage|1|
|Colored hit|2|
|Blank|2|
|Block|1|

```
Smaple space: [direct, hit, hit, blank, blank, block]
```

Direct damage ignores unit defense color
Colored hits only affect units with matching defense color
Block cancels one damage in the current round

### Unit Attributes

Each unit has:
- Defense parameters (red and/or black)
- Attack parameters (red and/or black)

Each attack parameter rolls one die of the corresponding color.

**Example**

Unit	                        Defense	    Attack
Rebel Trooper / Stormtrooper	1 black	    1 black
Air Speeder / AT-ST	          2 red	      1 red, 1 black
AT-AT	                        3 red	      2 red, 1 black

![It looks like this](https://images-cdn.fantasyflightgames.com/filer_public/c1/58/c158ce5c-3d88-4b77-a5ab-11167efde4fe/sw03-imperial-faction-sheet.jpg)
### Example Combat Setup

Empire
- AT-AT
- AT-ST
- 1 Stormtrooper

Rolls: 3 red dice, 3 black dice

Rebels
- Air Speeder
- 3 Rebel Troopers

Rolls: 1 red die, 4 black dice

### What the Simulator Does

- Simulates combat rounds using official dice distributions
- Applies damage, blocking, and unit elimination rules
- Repeats battles thousands of times
- Aggregates outcomes to estimate:
  - Win probabilities
  - Expected remaining units
  - Variance in results
  - Likelihood of extreme outcomes






