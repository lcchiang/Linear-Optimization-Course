import gurobipy as gp

# Define price fruits are sold for
sold_price = {'peach': 480, 'pear': 500, 'pineapple': 520}

# Define price fruits are sold for
purchase_cost = {'peach': 110, 'pear': 100, 'pineapple': 90}

# The dictionary below holds the cost of shipping of each fruit to the two plants.
# The cost in position 0 corresponds with Plant South and the cost in position1 corresponds with Plant Central.
ship_cost = {'peach': [30,35],'pear': [20, 25],'pineapple': [60, 40]}
# e.g., the cost of one shipment of peach to Plant South is $30/unit.

# Define max capacity for the two plants. Position 0 is South Plant and Position 1 is Central Plant.
capacity = [460,560]

m = gp.Model("fruits")
units = {}

# Define decision variables to indicate for each supplier/center how much is shipped
for fruit in sold_price:
    for plant in range(2):
        units[(plant,fruit)] = m.addVar(name=str((plant,fruit)))
        
# Next, we set our objective: maximize profit 
m.setObjective(sum(units[(plant,fruit)]*sold_price[fruit] for fruit in sold_price for plant in range(2)) -
               sum(units[(plant,fruit)]*purchase_cost[fruit] for fruit in sold_price for plant in range(2)) -
               sum(units[(plant,fruit)]*ship_cost[fruit][plant] for fruit in sold_price for plant in range(2)) - 
               sum(units[(0,fruit)] for fruit in sold_price)*260 - sum(units[(1,fruit)] for fruit in sold_price)*210 , gp.GRB.MAXIMIZE)

# Set a constraint that we cannot exceen the capacity of the plant.
for plant in range(2):
    m.addConstr(sum(units[(plant,fruit)] for fruit in sold_price) <= capacity[plant])
    

m.optimize()

print(units)