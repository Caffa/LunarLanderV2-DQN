# For Basic DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN

# For Double DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN

# For Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN

# For Double Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN

############################### --fc1_dims=128
# For Basic DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc1_dims=128

# For Double DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc1_dims=128

# For Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN --fc1_dims=128

# For Double Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN --fc1_dims=128

############################### --fc2_dims=32

# For Basic DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc2_dims=32

# For Double DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc2_dims=32

# For Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN --fc2_dims=32

# For Double Dueling DQN
python main.py --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN --fc2_dims=32