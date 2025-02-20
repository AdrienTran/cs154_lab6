# ucsbcs154lab6
# All Rights Reserved
# Copyright (c) 2023 University of California Santa Barbara
# Distribution Prohibited

import pyrtl

pyrtl.core.set_debug_mode()

# Inputs
fetch_pc = pyrtl.Input(bitwidth=32, name='fetch_pc') # current pc in fetch

update_prediction = pyrtl.Input(bitwidth=1, name='update_prediction') # whether to update prediction
update_branch_pc = pyrtl.Input(bitwidth=32, name='update_branch_pc') # previous pc (in decode/execute)
update_branch_taken = pyrtl.Input(bitwidth=1, name='update_branch_taken') # whether branch is taken (in decode/execute)

# Outputs
pred_taken = pyrtl.Output(bitwidth=1, name='pred_taken')

pred_state = pyrtl.MemBlock(bitwidth=2, addrwidth=3, name='pred_state')

new_pred_state = pyrtl.WireVector(bitwidth=2, name="new_pred_state")

# Write your BHT branch predictor here
fetch_index = fetch_pc[2:5]
prev_fetch_index = update_branch_pc[2:5]

branch_pred_state = pred_state[prev_fetch_index]

with pyrtl.conditional_assignment:
    with update_prediction:
        with update_branch_taken:
            with branch_pred_state == 3:
                new_pred_state |= 3
            with pyrtl.otherwise:
                new_pred_state |= branch_pred_state + 1
        with pyrtl.otherwise:
            with branch_pred_state == 0:
                new_pred_state |= 0
            with pyrtl.otherwise:
                new_pred_state |= branch_pred_state - 1
    with pyrtl.otherwise:
        new_pred_state |= branch_pred_state

# pred_state[fetch_index] <<= new_pred_state
with pyrtl.conditional_assignment:
    with fetch_index == prev_fetch_index:
        # print("test")
        pred_taken |= new_pred_state[1]
    with pyrtl.otherwise:
        # print("test123")
        pred_taken |= pred_state[fetch_index][1]

pred_state[prev_fetch_index] <<= new_pred_state

#Testing
if __name__ == "__main__":
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)
    pcPrevious = 0
    branchTakenPrevious = 0
    isBranchPrevious = 0
    predictionPrevious = 0
    count = 0
    correct = 0
    f = open("demo_trace.txt", "r")  # Edit this line to change the trace file you read from
    for iteration,line in enumerate(f): # Read through each line in the file
        pcCurrent = int(line[0:line.find(':')],0) # parse out current pc
        branchTakenCurrent = int(line[12]) # parse out branch taken
        isBranchCurrent = int(line[16]) # parse if the current instr is a branch

        sim.step({ # Feed in input values
            'fetch_pc' : pcCurrent,
            'update_branch_pc' : pcPrevious,
            'update_prediction': isBranchPrevious,
            'update_branch_taken' : branchTakenPrevious
        })

        predictionCurrent = sim_trace.trace['pred_taken'][-1] # get the value of your prediction
        # print(iteration + 1, " : ",  predictionPrevious)
        if isBranchPrevious: # check if previous instr was a branch
            if predictionPrevious == branchTakenPrevious: # if prediction was correct
                # print (iteration, ": ", predictionPrevious, " ", branchTakenPrevious, " ", pcCurrent)
                # print ("curr: ", predictionCurrent, " ", branchTakenCurrent)
                correct += 1
            count += 1


        # Update for next cycle
        pcPrevious = pcCurrent
        branchTakenPrevious = branchTakenCurrent
        isBranchPrevious = isBranchCurrent
        predictionPrevious = predictionCurrent

    # one final check
    if isBranchPrevious:
        if predictionPrevious == branchTakenPrevious:
            correct += 1 # Correct prediction
        count += 1
        
    # print("correct: ", correct)
    # print("count: ", count)
    
    print("Accuracy = ", correct/count)
    sim_trace.render_trace()
