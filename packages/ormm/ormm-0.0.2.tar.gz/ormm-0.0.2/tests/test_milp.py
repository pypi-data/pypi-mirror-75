import io
import sys

import pyomo.environ as pyo
import pandas as pd

from ormm.mathprog import resource_allocation, \
    print_sol, sensitivity_analysis, blending

MATHPROG_DATA = "../ormm/mathprog/example_data/"
SIMPLE_RES_DATA = MATHPROG_DATA + "resource_allocation.dat"
COMPLEX_RES_DATA = MATHPROG_DATA + "mult_resource_allocation.dat"
BLENDING_DATA = MATHPROG_DATA + "blending.dat"


def create_instance_results(model, data_path):
    instance = model.create_instance(data_path)
    opt = pyo.SolverFactory("glpk")
    results = opt.solve(instance)
    return instance, results


def create_res(data_path, **kwargs):
    """Use exmaple data & return results and solved instance"""
    mod = resource_allocation(**kwargs)
    return create_instance_results(mod, data_path)


def create_blending(data_path, **kwargs):
    mod = blending(**kwargs)
    return create_instance_results(mod, data_path)


def test_simple_resource_allocation_with_data():
    instance, results = create_res(SIMPLE_RES_DATA)
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            assert {index: v[index].value
                    for index in v} == {"P": 100, "Q": 30}
    assert instance.OBJ() == 6300


def test_complex_resource_allocation_with_data():
    instance, results = create_res(
        COMPLEX_RES_DATA, mult_res=True, max_activity=False)
    # Check all variable values
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "NumActivity":
            assert {
                index: round(v[index].value, 2) for index in v} == {
                "Q": 58.96, "W": 62.63, "E": 0, "R": 10.58, "T": 15.64}
    assert round(instance.OBJ(), 0) == 2989


def test_blending():
    instance, results = create_blending(BLENDING_DATA)
    for v in instance.component_objects(pyo.Var, active=True):
        if v.name == "Blend":
            assert {
                index: round(v[index].value, 2) for index in v} == {
                "Limestone": 0.03, "Corn": 0.65, "Soybean": 0.32}
    assert round(instance.OBJ(), 2) == 49.16


def test_print_sol_with_data():
    instance, results = create_res(SIMPLE_RES_DATA)
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


def test_sensitivity_analysis():
    instance, results = create_res(
        COMPLEX_RES_DATA, mult_res=True, max_activity=False)
    sens_analysis_df = sensitivity_analysis(instance)
    test_df = pd.DataFrame({
        "Dual Value": [4.819506, 5.201604, 8.963479, 0.363099],
        "Lower": [None, None, None, None],
        "Upper": [160.0, 200.0, 120.0, 280.0],
        "Slack": [0, 0, 0, 0],
        "Active": [True, True, True, True]
        }, index=[
            "ResourceConstraint[A]",
            "ResourceConstraint[B]",
            "ResourceConstraint[C]",
            "ResourceConstraint[D]"])
    sens_analysis_df["Dual Value"] = \
        sens_analysis_df["Dual Value"].round(decimals=6)
    assert sens_analysis_df.equals(test_df)
