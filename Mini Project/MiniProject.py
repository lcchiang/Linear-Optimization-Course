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
num_beams = 251
num_orders = df_read.shape[0]


# Initializing rod lengths and number of rods to produce
rod_lengths = {}
num_rods = 0
for order in range(num_orders):
    for rod in range(int(df_read.iloc[order][0])):
        rod_lengths[num_rods] = df_read.iloc[order][1]
        num_rods +=1



## WARM START INFO
warm_partial_rod_length = {}
warm_beam_use = {}
warm_beam_purchase = {}
warm_welds = {}
df_warm = pd.read_csv('partB_res_12h.csv')
for (rod,beam) in df_warm.iterrows():
    pieces = 0
    welds = 0
    for num_beam in range(len(beam)):        
        warm_partial_rod_length[(num_beam,rod)] = beam[num_beam]
        if beam[num_beam] > 0:
            warm_beam_use[(num_beam,rod)] = 1
            pieces += 1
        else:
            warm_beam_use[(num_beam,rod)] = 0
    warm_welds[rod] = pieces - 1

for beam in range(num_beams):
    if sum(warm_beam_use[beam,rod] for rod in range(num_rods)) > 0:
        warm_beam_purchase[beam] = 1
    else:
        warm_beam_purchase[beam] = 0



# DECISION VARIABLES
# Whether or not we purchase a beam
beam_purchase = {}
for beam in range(num_beams):
    beam_purchase[beam] = m.addVar(name = "Beam #" + str(beam+1), vtype = gp.GRB.BINARY)
    beam_purchase[beam].start = warm_beam_purchase[beam]

# Whether or not a beam is used to produce a rod
beam_use = {}
for beam in range(num_beams):
    for rod in range(num_rods):
        beam_use[(beam,rod)] = m.addVar(name = str((beam +1,rod +1)), vtype = gp.GRB.BINARY)
        beam_use[(beam,rod)].start = warm_beam_use[(beam,rod)]

# Number of welds
rod_welds = {}
for rod in range(num_rods):
    rod_welds[rod] = m.addVar(name = str((rod +1)), vtype = gp.GRB.INTEGER)
    rod_welds[rod].start = warm_welds[rod]
    
# Length of rod within a specific beam
rod_partial_lengths = {}
for beam in range(num_beams):
    for rod in range(num_rods):
        rod_partial_lengths[(beam,rod)] = m.addVar(name = str((beam +1,rod +1)), lb = 0)
        rod_partial_lengths[(beam,rod)].start = warm_partial_rod_length[(beam,rod)]


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

m.Params.TimeLimit = 60*5

m.optimize()

print(sum(beam_purchase[beam].x for beam in range(num_beams)))

f = open("partB_res.csv","w")
for rod in range(num_rods):
    temp_str = ''
    for beam in range(num_beams):
        temp_str += str(max(rod_partial_lengths[(beam,rod)].x,0)) + ","
    temp_str = temp_str[0:-1]
    f.writelines(temp_str)
    f.write('\n')

f.close()
