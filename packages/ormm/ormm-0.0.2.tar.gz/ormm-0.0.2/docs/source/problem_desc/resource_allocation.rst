Resource Allocation
===================
The Resource Allocation Problem optimizes using scarce resources for valued activities.
The resources are limited by some maximum quantity available,
while the activities have some numeric value assigned to each of them.
A matrix-like parameter shows all of the resources needed to conduct one unit
of that activity (:py:obj:`ResourceNeeds`).
This type of problem is seen often, with a few examples being production management
and budget allocation.

Definitions
-----------

Sets
""""
- :py:obj:`Activities` - Set of activities that are available to produce

   - :py:obj:`a in Activities` or :math:`a \in A`

- :py:obj:`Resources` - Set of resources that are used to conduct activities

   - :py:obj:`r in Resources` or :math:`r \in R`

Parameters
""""""""""
- :py:obj:`Values` - measure of value from conducting one unit
  of :py:obj:`Activity a`

   - :py:obj:`Values[a] for a in Activities` or :math:`V_a \enspace \forall a \in A`

- :py:obj:`ResourceNeeds` - amount of :py:obj:`Resource r` needed
  for :py:obj:`Activity a`

   - :py:obj:`ResourceNeeds[r, a] for r in Resources for a in Activities`
     or :math:`N_{r,a} \enspace \forall r \in R, a \in A`

   .. note::

      To conduct one unit of :py:obj:`Activity a`, you need all resources required.
      For example, to conduct one unit of :py:obj:`Activity a_1`, you need
      :py:obj:`sum(ResourceNeeds[r, a_1] for r in Resources)`

- :py:obj:`MaxResource` - maximum amount of units available of :py:obj:`Resource r`

   - :py:obj:`MaxResource[r] for r in Resources` or
     :math:`M_r \enspace \forall r \in R`

- :py:obj:`MaxActivity` - maximum amount of demand for :py:obj:`Activity a`

   - :py:obj:`MaxActivity[a] for a in Activities` or
     :math:`M_a \enspace \forall a \in A`

Decision Variables
""""""""""""""""""
- :py:obj:`NumActivity` - number of units to conduct of :py:obj:`Activity a`

   - :py:obj:`NumActivity[a] for a in Activities` or
     :math:`X_a \enspace \forall a \in A`

Objective
---------
**Maximize** total value of activities being conducted.

.. math::

   \text{Max} \sum_{a \in A} V_aX_a

Constraints
-----------
- An :py:obj:`Activity a` cannot be conducted more than its :py:obj:`MaxActivity`

.. math::

   0 \leq X_a \leq M_a \quad \forall a \in A

- To conduct 1 unit of an Activity, all :py:obj:`ResourceNeeds` are required.
  In other words, :py:obj:`sum(ResourceNeeds[r,a] for r in Resources)`
  must happen per :py:obj:`Activity a` conducted.
  This is implied by the problem parameters given by the user and the next constraint.
- The amount of resources used for a :py:obj:`Resource r` must not exceed
  :py:obj:`MaxResource[r]`

.. math::

    \sum_{a \in A} N_{r,a}X_a \leq M_r \quad \forall r \in R

API Reference
-------------
See the corresponding section in the :ref:`api_reference` to learn more
about how to use the API for this problem class.