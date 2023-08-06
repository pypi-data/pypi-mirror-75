def items(x):
    for name,var in x._naming_var.items():
        yield name,var 
def signals(x):
    for name,var in x._naming_var.items():
        if var.typename in {'wire','reg'}:yield var
def wires(x):
    for name,var in x._naming_var.items():
        if var.typename == 'wire':yield var
def registers(x):
    for name,var in x._naming_var.items():
        if var.typename == 'reg':yield var
def ports(x,force_determined=False):
    for var in signals(x):
        if force_determined:var._auto_port_determined()
        if not var.io is None:yield var
def inner_signals(x):
    for var in signals(x):
        if var.io is None:yield var
def parameters(x):
    for name,var in x._naming_var.items():
        if var.typename == 'parameter' and not var.io is None:yield var
def params(x):
    for name,var in x._naming_var.items():
        if var.typename == 'parameter':yield var
