import pyomo.environ as pyo

class ResourceAllocation(pyo.AbstractModel):
    """Pyomo Abstract Model for the Resource Allocation Problem

    :return: A pyomo abstract model with definitions for the Resource Allocation Problem

    See Also
    --------
    Formulation: Documentation with definitions & details of the abstract model.

    Examples
    --------
    Creating abstract model, an instance from data params, & solving instance.

    >>> model = ResourceAllocation()
    >>> instance = model.create_instance(my_params.dat) # AMPL data file
    >>> opt = pyo.SolverFactory("glpk")
    >>> opt.solve(instance)
    """

    def __init__(self):
        """Constructor method - calls create_abstract_model
        """
        super().__init__()
        self.create_abstract_model()

    def create_abstract_model(self):
        """Create the abstract model for Resource Allocation Problem
        """
        self.Activities = pyo.Set()
        self.Resources = pyo.Set()
        self.Values = pyo.Param(self.Activities)
        self.ResourceNeeds = pyo.Param(self.Resources, self.Activities)
        self.MaxResource = pyo.Param(self.Resources)
        self.MaxActivity = pyo.Param(self.Activities)
        self.NumActivity = pyo.Var(self.Activities, within = pyo.NonNegativeIntegers, bounds = self._get_bounds)

        self.OBJ = pyo.Objective(rule = self._obj_expression, sense = pyo.maximize)
        self.ResourceConstraint = pyo.Constraint(self.Resources, rule = self._resource_constraint_rule)

    def _get_bounds(self, model, p):
        """Upper Bounds for the Decision Vars based on Maximum Demand
        """
        return (0, self.MaxActivity[p])

    def _obj_expression(self, model):
        """Objective Expression: Maximizing Profit
        """
        return pyo.summation(self.Values, self.NumActivity)

    def _resource_constraint_rule(self, model, m):
        """Constraints for Scarce Resources"""
        return sum(self.ResourceNeeds[m, p] * self.NumActivity[p] for p in self.Activities) <= self.MaxResource[m]

def print_sol(instance):
    """Print the solution to the solved `instance`
    :param instance: A solved pyomo.environ.ConcreteModel
    """
    print(f"Objective Value: ${instance.OBJ():,}")
    for v in instance.component_objects(pyo.Var, active=True):
        print ("Variable component: ",v)
        for index in v:
            print ("   ", index, v[index].value)