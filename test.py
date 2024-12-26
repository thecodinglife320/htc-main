import pickle

with open('q_table_expanded.pkl', 'rb') as f:
    my_dict = pickle.load(f)
for (state, action), q_value in my_dict.items():
    print(f"State: {state}, Action: {action}, Q-value: {q_value}")
