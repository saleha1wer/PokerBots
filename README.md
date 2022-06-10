# PokerBots
A implementation of 3 poker agents: 1) Shallow-MCTS Agent, 2) EV Agent and 3) Network Agent

## Requirments
* Python 3.9.12+

## Packages
* Pokerface
* Numpy
* Tensorflow
* eval7
* pandas
* scipy

## Running instructions
* To initiate a Random Agent, Call Agent, Shallow-MCTS Agent or an EV Agent:
```
from shallow_mcts import ShallowMCTS
from random_agent import RandomAgent
from ev_agent import EVAgent
from callbot_agent imoort CallbotAgent

from pokerface import Stakes,NoLimitTexasHoldEm
stakes = Stakes(0, (1, 2))
starting_stacks = 200, 200, 200,200
nls = NoLimitShortDeckHoldEm(stakes, starting_stacks)

ra = RandomAgent(nls) # initiate random agent
smcts = ShallowMCTS(nls) # initiate sMCTS agent
ev = EVAgent(nls)  # initiate EV agent
cb = CallbotAgent(nls) # initiate call-bot agent
```
* To initiate a Network Agent:
