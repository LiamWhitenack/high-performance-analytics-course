from itertools import product

# Instructions for each processor as functions
def p1_step1(state): state['x'] = 1
def p1_step2(state): state['x'] = state['x'] + state['y']
def p1_step3(state): state['y'] = state['x'] + state['y']

def p2_step1(state): state['y'] = 2
def p2_step2(state): state['x'] = 4

# Steps in order for each processor
p1_steps = [p1_step1, p1_step2, p1_step3]
p2_steps = [p2_step1, p2_step2]

# Recursive function to explore all interleavings
def interleave(p1_idx, p2_idx, state, outcomes):
    if p1_idx == len(p1_steps) and p2_idx == len(p2_steps):
        outcomes.add((state['x'], state['y']))
        return
    if p1_idx < len(p1_steps):
        new_state = state.copy()
        p1_steps[p1_idx](new_state)
        interleave(p1_idx + 1, p2_idx, new_state, outcomes)
    if p2_idx < len(p2_steps):
        new_state = state.copy()
        p2_steps[p2_idx](new_state)
        interleave(p1_idx, p2_idx + 1, new_state, outcomes)

# Run
outcomes = set()
interleave(0, 0, {'x': 0, 'y': 0}, outcomes)

print("All possible (x, y) outcomes:")
for outcome in sorted(outcomes):
    print(outcome)
