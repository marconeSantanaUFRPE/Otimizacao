from gurobipy import *


import xlrd
 
def lerdados(arq_xls):
    xls = xlrd.open_workbook(arq_xls)

    plan = xls.sheets()[0]
 
    for i in range(1,plan.nrows):

        yield plan.row_values(i)

a = lerdados('dados.xlsx')
capacidade_servidor = []
demanda_vm = []

for x in a:
        if x[0] != "":
                capacidade_servidor.append(x[0])
        if x[1] != "":
                demanda_vm.append(x[1])

capaci = len(capacidade_servidor)
demand = len(demanda_vm)

model = Model("empacotamento")

x,y = {},{}


for i in range(demand):
        for j in range(capaci):
            x[i,j] = model.addVar(vtype="B", name="x(%s,%s)"%(i,j))

for j in range(capaci):
        y[j] = model.addVar(vtype="B", name="Maquina %s (capacidade: %s)"   %  (j,capacidade_servidor[j]))

model.setObjective(quicksum(y[j] for j in range(capaci)), GRB.MINIMIZE)


for i in range(demand):
        model.addConstr(quicksum(x[i,j] for j in range(capaci)) == 1, "Assign(%s)"%i)

for j in range(capaci):
        model.addConstr(quicksum(demanda_vm[i]*x[i,j] for i in range(demand)) ,GRB.LESS_EQUAL, capacidade_servidor[j]*y[j], "Capac(%s)"%j)




model.optimize()


print(model.objVal)

for v in model.getVars():
    print(v.varName, v.x)
    