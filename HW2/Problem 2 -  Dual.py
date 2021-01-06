import gurobipy as gp

# First, we define a variable that contains the optimization model
m = gp.Model("dual")

# Next, we define the three decision variables with their respective lower and upper bounds
A = m.addVar(lb = 0) # 0<= A
B = m.addVar(lb = 0) # 0<= B
C = m.addVar(lb = 0) # 0<= C
D = m.addVar(lb = 0) # 0<= D
E = m.addVar(lb = 0) # 0<= E



# Then, we add the other constraints
x = m.addConstr(3*A + B + D >= 1) # 3x + y + 5z<=10
y = m.addConstr(A + 3*B + E >= 3) # x + 3y<=12
z = m.addConstr(5*A - 3*C >= 2) # 3*z>=6

# Next, we set our objective: maximizing x+3y+2z
m.setObjective(10*A + 12*B -6*C + 10*D + 12*E, gp.GRB.MINIMIZE)

m.optimize()

# Then we print the solution values for each variable
print(A.x,B.x,C.x,D.x,E.x)
print(x.pi, y.pi, z.pi)