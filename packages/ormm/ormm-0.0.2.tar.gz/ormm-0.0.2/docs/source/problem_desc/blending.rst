Blending Problem
================
The Blending Problem optimizes the mixing of ingredients
to satisfy restrictions while minimizing cost.
The restrictions are that certain properties of using the ingredients
must be within their minimum and maximum values allowed.
For example, ingredients in food may have nutrional properties,
and this problem could force Calcium content of the mixture to be within
a lower and upper bound (in terms of proportions).
This problem deals with proportions, so it must another constraint to
ensure that the sum of the decision variables (proportion of each ingredient to use)
equals 1.
A matrix-like parameter shows the numeric properties of each of the ingredients
(:py:obj:`IngredientProperties`).
This type of problem arises often in the food, feed, and oil
refinement industries.

Definitions
-----------

Sets
""""
- :py:obj:`Ingredients` - Set of activities that are available to produce

   - :py:obj:`i in Ingredients` or :math:`i \in I`

- :py:obj:`Properties` - Set of resources that are used to conduct activities

   - :py:obj:`p in Properties` or :math:`p \in P`

Parameters
""""""""""
- :py:obj:`Cost` - measure of value from conducting one unit
  of :py:obj:`Ingredient i`

   - :py:obj:`Cost[i] for i in Ingredients` or :math:`C_i \enspace \forall i \in I`

- :py:obj:`IngredientProperties` - measure of how much :py:obj:`Property p`
  is in :py:obj:`Ingredient i`

   - :py:obj:`IngredientProperties[i, p] for i in Ingredients for p in Properties`
     or :math:`N_{i,p} \enspace \forall i \in I, p \in P`

- :py:obj:`MinProperty` - minimum amount of :py:obj:`Property p` needed
  in the blend

   - :py:obj:`MinProperty[p] for p in Properties` or
     :math:`Min_p \enspace \forall p \in P`

- :py:obj:`MaxProperty` - maximum amount of :py:obj:`Property p` allowed
  in the blend

   - :py:obj:`MaxProperty[p] for p in Properties` or
     :math:`Max_p \enspace \forall p \in P`

Decision Variables
""""""""""""""""""
- :py:obj:`Blend` - proportion of :py:obj:`Ingredient i` to include in the blend.

   - :py:obj:`Blend[i] for i in Ingredients` or
     :math:`X_i \enspace \forall i \in I`

Objective
---------
**Minimize** total cost of the ingredients in the blend.

.. math::

   \text{Min} \sum_{i \in I} C_iX_i

Constraints
-----------
- The Blend must have its Properties within the upper and lower bounds,
  :py:obj:`MinProperty[p]` and :py:obj:`MaxProperty[p]`.

.. math::

   Min_p \leq \sum_{i \in I}N_{i,p}X_i \leq Max_p \quad \forall p \in P

- The Blend decision variables are proportions of the ingredients to include,
  and thus, the decision variables must add up to 1. Additionally, these
  decision variables must all be greater than or equal to zero.

.. math::

    \sum_{i \in I} X_i = 1

    X_i \geq 0 \enspace \forall i \in I

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.