"""
Module contains factory methods & other functions
for Mixed Integer Linear Programs (MILP).
"""
import math

import pyomo.environ as pyo
import pyomo
import pandas as pd


def blending(linear=True, **kwargs):
    """
    Factory method returning Pyomo Abstract/Concrete Model
    for the Blending Problem

    Parameters
    ----------
    linear : :py:obj:`bool`, optional
        Determines whether decision variables will be
        Reals (True) or Integer (False).
    **kwargs
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Notes
    -----
    The Blending Problem optimizes the mixing of ingredients
    to satisfy restrictions while minimizing cost.

    .. math::

       \\text{Min}  \\sum_{i \\in I} C_iX_i

       \\text{s.t.} \\enspace Min_p \\leq \\sum_{i \\in I} N_{i,p}X_i
            \\leq Max_p \\quad \\forall p \\in P

       \\sum_{i \\in I} X_i = 1

       X_i \\geq 0 \\quad \\forall i \\in I

    Examples
    --------
    Creating a concrete model from data params & solving instance.

    >>> import pyomo.environ as pyo
    >>> instance = blending("my_params.dat") # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> results = opt.solve(instance)
    """
    def _obj_expression(model):
        """Objective Expression: Maximizing Value"""
        return pyo.summation(model.Cost, model.Blend)

    def _property_constraint_rule(model, p):
        """Constraints for Scarce Resources"""
        return (model.MinProperty[p], sum(
            model.IngredientProperties[i, p]
            * model.Blend[i]
            for i in model.Ingredients
            ), model.MaxProperty[p])

    def _conservation_constraint_rule(model):
        return pyo.summation(model.Blend) == 1

    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Ingredients = pyo.Set()
    model.Properties = pyo.Set()
    model.Cost = pyo.Param(model.Ingredients)
    model.IngredientProperties = pyo.Param(model.Ingredients, model.Properties)
    model.MinProperty = pyo.Param(model.Properties)
    model.MaxProperty = pyo.Param(model.Properties)
    # Define decision variables
    model.Blend = pyo.Var(
        model.Ingredients,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers,
        bounds=(0, None))
    # Define objective & constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.minimize)
    model.PropertyConstraint = pyo.Constraint(
        model.Properties,
        rule=_property_constraint_rule)
    model.ConservationConstraint = pyo.Constraint(
        rule=_conservation_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model


def resource_allocation(
        linear=True, mult_res=False,
        max_activity=True, **kwargs):
    """
    Factory method returning Pyomo Abstract/Concrete Model
    for the Resource Allocation Problem.

    Parameters
    ----------
    linear : :py:obj:`bool`, optional
        Determines whether decision variables will be
        Reals (True) or Integer (False).
    mult_res : :py:obj:`bool`, optional
        Determines whether there are multiple of each resource or not.
    max_activity : :py:obj:`bool`, optional
        Determines whether there is an upper limit on the
        decision variables.
    **kwargs
        Passed into Pyomo Abstract Model's `create_instance`
        to return Pyomo Concrete Model instead.

    Notes
    -----
    The Resource Allocation Problem optimizes
    using scarce resources for valued activities.

    .. math::

       \\text{Max}  \\sum_{a \\in A} V_aX_a

       \\text{s.t.} \\sum_{a \\in A} N_{r,a}X_a \\leq M_r
           \\quad \\forall r \\in R

       0 \\leq X_a \\leq M_a \\quad \\forall a \\in A

    Examples
    --------
    Creating a concrete model from data params & solving instance.

    >>> import pyomo.environ as pyo
    >>> instance = resource_allocation("my_params.dat) # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> results = opt.solve(instance)
    """
    def _get_bounds(model, a):
        """Upper Bounds for the Decision Vars based on Maximum Demand."""
        return (0, model.MaxActivity[a])

    def _obj_expression(model):
        """Objective Expression: Maximizing Value"""
        return pyo.summation(model.Values, model.NumActivity)

    def _resource_constraint_rule(model, r):
        """Constraints for Scarce Resources"""
        return sum(
            model.ResourceNeeds[r, a]
            * model.NumActivity[a]
            for a in model.Activities
            ) <= model.MaxResource[r]

    def _mult_resource_constraint_rule(model, r):
        """Constraints for Scarce Resources"""
        return sum(
            model.ResourceNeeds[r, a]
            * model.NumActivity[a]
            for a in model.Activities
            ) <= model.MaxResource[r] * model.NumResource[r]
    # Create the abstract model & dual suffix
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    # Define sets/params that are always used
    model.Activities = pyo.Set()
    model.Resources = pyo.Set()
    model.Values = pyo.Param(model.Activities)
    model.ResourceNeeds = pyo.Param(model.Resources, model.Activities)
    model.MaxResource = pyo.Param(model.Resources)
    # If multiple resources, load those params
    if mult_res:
        model.NumResource = pyo.Param(model.Resources)
    # If upper bound on dec. vars, load those params
    if max_activity:
        model.MaxActivity = pyo.Param(model.Activities)
    # Define decision variables
    model.NumActivity = pyo.Var(
        model.Activities,
        within=pyo.NonNegativeReals if linear else pyo.NonNegativeIntegers,
        bounds=_get_bounds if max_activity else (0, None))
    # Define objective & resource constraints
    model.OBJ = pyo.Objective(rule=_obj_expression, sense=pyo.maximize)
    model.ResourceConstraint = pyo.Constraint(
        model.Resources,
        rule=_resource_constraint_rule if not mult_res
        else _mult_resource_constraint_rule)
    # Check if returning concrete or abstract model
    if kwargs:
        return model.create_instance(**kwargs)
    else:
        return model


def print_sol(instance):
    """
    Print the solution to the solved `instance`.

    Parameters
    ----------
    instance : :py:class:`pyomo.environ.ConcreteModel`
        A solved model to retrieve objective & variable values.

    Notes
    ----
    Assumes the objective is retrievable by :py:obj:`instance.OBJ()`
    """
    print(f"Objective Value: ${instance.OBJ():,}")
    for v in instance.component_objects(pyo.Var, active=True):
        print("Variable component: ", v)
        for index in v:
            print("   ", index, v[index].value)


def sensitivity_analysis(instance):
    """
    Return dataframe containing sensitivity analysis

    Parameters
    ----------
    instance : :py:class:`pyomo.environ.ConcreteModel`
        A solved model to retrieve dual suffix.

    Returns
    -------
    pandas.DataFrame
        Dataframe with sensitivity analysis information.

    Notes
    -----
    Assumes the dual suffix is retrievable by :py:obj:`instance.dual`.
    """
    # Dual Variable Values
    dual_dict = {str(k): [v] for (k, v) in dict(instance.dual).items()}
    # Constraint Info
    for con in instance.dual:
        lower = con.lower if type(con.lower) \
            is not pyomo.core.expr.numvalue.NumericConstant \
            else con.lower.value
        upper = con.upper if type(con.upper) \
            is not pyomo.core.expr.numvalue.NumericConstant \
            else con.upper.value
        slack = 0 if math.isclose(con.slack(), 0,
                                  abs_tol=1e-5) else con.slack
        active = con.active
        vals = [lower, upper, slack, active]
        # Add constraint info to dual_dict
        dual_dict[con.name].extend(vals)
    # dual_dict to pandas dataframe
    sens_analysis = pd.DataFrame.from_dict(dual_dict,
                                           orient="index",
                                           columns=[
                                               "Dual Value",
                                               "Lower",
                                               "Upper",
                                               "Slack",
                                               "Active"])
    # Name the index and return the dataframe
    sens_analysis.index.name = "Constraint"
    return sens_analysis
