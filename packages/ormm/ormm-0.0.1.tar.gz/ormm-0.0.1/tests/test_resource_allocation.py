import io
import sys

import pyomo.environ as pyo
from ormm.opt.mathprog.problems import ResourceAllocation, print_sol

def create_cm_with_data():
    """Use exmaple data & return results and solved instance"""
    data_path = "../ormm/opt/mathprog/problems/example_data/resource_allocation.dat"
    mod = ResourceAllocation()
    instance = mod.create_instance(data_path)
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results

def test_resource_allocation_with_data():
    instance, results = create_cm_with_data()
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            print({index: v[index].value for index in v})
            assert {index: v[index].value for index in v} == {"P": 100, "Q": 30}
    assert instance.OBJ() == 6300
def test_print_sol_with_data():
    instance, results = create_cm_with_data()
    # Redirect output to StringIO object
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_sol(instance)
    sys.stdout = sys.__stdout__  # reset stdout
    test_string = (
        "Objective Value: $6,300.0\n"
        "Variable component:  NumActivity\n"
        "    P 100.0\n"
        "    Q 30.0\n"
    )
    assert captured_output.getvalue() == test_string