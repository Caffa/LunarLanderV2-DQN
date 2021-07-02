

# ONEFC=64
# TWOFC=64
# # For Basic DQN
# python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# # For Double DQN
# python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# # For Dueling DQN
# python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# # For Double Dueling DQN
# python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC

############################### --fc1_dims=128
ONEFC=128
TWOFC=128

# For Basic DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Double DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Double Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC
############################### --fc2_dims=32

ONEFC=32
TWOFC=32

# For Basic DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Double DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC

# For Double Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN  --fc1_dims=$ONEFC --fc2_dims=$TWOFC
############################### --fc1_dims=128
