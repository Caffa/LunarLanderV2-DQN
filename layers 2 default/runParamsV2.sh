

VAR1="64 128"
VAR2="128 64"

fun()
{
    MYSEED=$RANDOM
    set $VAR2
    for i in $VAR1; do
        echo command "$i" "$1"
        # For Basic DQN
        python main.py --seed=$MYSEED --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=SIMPLE --name=DQN --fc1_dims=$i --fc2_dims=$1

        # For Double DQN
        python main.py --seed=$MYSEED --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=SIMPLE --name=DoubleDQN --fc1_dims=$i --fc2_dims=$1

        # For Dueling DQN
        python main.py --seed=$MYSEED --test_mode=TRAIN --agent_mode=SIMPLE --network_mode=DUELING --name=DuelDQN  --fc1_dims=$i --fc2_dims=$1

        # For Double Dueling DQN
        python main.py --seed=$MYSEED --test_mode=TRAIN --agent_mode=DOUBLE --network_mode=DUELING --name=DoubleDuelDQN  --fc1_dims=$i --fc2_dims=$1
        
        shift
    done
}

fun
fun
fun
