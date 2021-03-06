import gurobipy as gp 
import pandas as pd

    # Read in lengths
df_read = pd.read_excel('Rod_cutting_input.xlsx')
columns = df_read.columns
df_read = df_read.drop(columns=columns[0])
df_read = df_read.rename(columns={columns[1]:'count', columns[2]:'length'})

m = gp.Model("Beam to Rods")

# Given Info
cost_beam = 1380
cost_weld = 156
initial_length = 12005
num_beams = 236
num_orders = df_read.shape[0]


# Initializing rod lengths and number of rods to produce
rod_lengths = {}
num_rods = 0
for order in range(num_orders):
    for rod in range(int(df_read.iloc[order][0])):
        rod_lengths[num_rods] = df_read.iloc[order][1]
        num_rods +=1
        

# DECISION VARIABLES
# Whether or not we purchase a beam
beam_purchase = {}
for beam in range(num_beams):
    beam_purchase[beam] = m.addVar(name = "Beam #" + str(beam+1), vtype = gp.GRB.BINARY)
    

# Whether or not a beam is used to produce a rod
beam_use = {}
for beam in range(num_beams):
    for rod in range(num_rods):
        beam_use[(beam,rod)] = m.addVar(name = str((beam +1,rod +1)), vtype = gp.GRB.BINARY)
        
# Number of welds
rod_welds = {}
for rod in range(num_rods):
    rod_welds[rod] = m.addVar(name = str((rod +1)), vtype = gp.GRB.INTEGER)
    
    
# Length of rod within a specific beam
rod_partial_lengths = {}
for beam in range(num_beams):
    for rod in range(num_rods):
        rod_partial_lengths[(beam,rod)] = m.addVar(name = str((beam +1,rod +1)), lb = 0)
        


# OBJECTIVE FUNCTION
# Minimize beams used or cost of beams
m.setObjective(sum(cost_beam*beam_purchase[beam] for beam in range(num_beams)) + 
                   sum(cost_weld*rod_welds[rod] for rod in range(num_rods)), gp.GRB.MINIMIZE)

# CONSTRAINTS
# Beam cannot be used for more than 12005mm of length and cannot be used if not purchased
for beam in range(num_beams):
    m.addConstr(sum(rod_partial_lengths[(beam,rod)] + 5*beam_use[(beam,rod)] for rod in range(num_rods)) <= 
                initial_length*beam_purchase[beam])

# Added segments must equal finished rod order length
for rod in range(num_rods):
    m.addConstr(sum(rod_partial_lengths[(beam,rod)] for beam in range(num_beams)) == rod_lengths[rod])

# Can only use beam to produce a segment if it is selected
for beam in range(num_beams):
    for rod in range(num_rods):
        m.addConstr(rod_partial_lengths[(beam,rod)] <= initial_length*beam_use[(beam,rod)])

# Number of welds is 1 less than number of segments for a rod
for rod in range(num_rods):
        m.addConstr(sum(beam_use[(beam,rod)] for beam in range(num_beams)) - 1 == rod_welds[rod])
        
# Beam purchase happens sequentially
for beam in range(num_beams-1):
    m.addConstr(beam_purchase[beam+1] <= beam_purchase[beam])

m.Params.TimeLimit = 60*60

m.optimize()