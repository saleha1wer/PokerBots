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

# initiate game
stakes = Stakes(0, (1, 2))
starting_stacks = 200, 200, 200,200
nls = NoLimitShortDeckHoldEm(stakes, starting_stacks)

ra = RandomAgent(nls) # initiate random agent
smcts = ShallowMCTS(nls) # initiate sMCTS agent
ev = EVAgent(nls)  # initiate EV agent
cb = CallbotAgent(nls) # initiate call-bot agent
```
* To initiate a Network Agent:
```
from policy_network.network import Network
from policy_network.network_agent import NetworkAgent
import keras

max_opp = 4 #maximum number of opponents that can be encoded by the network
network = Network([(7),(2*max_opp)],5)
# to use a specific network: 
network_path = 'policy_network/saved_models/max_4_opp/final.tf'
model = keras.models.load_model(network_path)
network.network = model
net_agent = NetworkAgent(nls,network,0) # initiate network agent
# to initialize random network: 
network.initialize_network()
net_agent = NetworkAgent(nls,network,1) # initiate network agent
```
* To train a network agent: 
```
  max_n_opp = 1 # -- > number of opponents

  policy_network = Network([(7),(max_n_opp*2)],5)
  # policy_network.initialize_network() --> uncomment this and comment the next line to train a network from scratch
  # use last network as initial network
  policy_network.network = keras.models.load_model('policy_network/saved_models/max_1_opp/trained_EVandRandom/final.tf')
  
  opp = 'EV' # --> opponenet to train against. Can be 'random' or 'EV'. If max_n_opp > 1, the rest of the opponents are random agents.
  total = 10 # -->  Number of games in every training run
  max_rounds = 35 # -->  max round per game
  m_p=True # -->  whether to use multiprocessing or not
  buffer_size = 1000
  sample_size = 500 # -->  size of sample from buffer for network training 
  new_policy_network = policy_network_self_play(policy_network,max_n_opp,total=total,max_rounds=max_rounds,
                                              opp=opp,m_p=m_p,buffer_size=buffer_size,sample_size=sample_size)

  new_policy_network.save_network('max_1_opp/new_final')  # --> save new network

```
