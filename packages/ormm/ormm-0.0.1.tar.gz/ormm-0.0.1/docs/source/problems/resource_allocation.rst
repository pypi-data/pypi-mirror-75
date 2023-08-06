Problem Description
===================

Objective
---------
Maximize total profit of selling products produced.

Constraints
-----------
- A Product p cannot be sold more than its Max Demand
- To sell 1 unit of a product, it must undergo all processing for each machine.  In other words, `sum(ProcessTimes[m,p] for m in Machines)` must happen per product produced. This is implied by the problem parameters and the next constraint.
- The amount of processing time for a machine m must not exceed `MaxTimes[m]`, or `sum(ProcessTimes[m,p] * Produce[p] for p in Products) <= MaxTimes[m]` for all m in machines.

Definitions
-----------
Sets:
- `Products`: Set of products that are available to produce ⟶ `p in Products`
- `Machines`: Set of machines that are used to produce products ⟶ `m in Machines`

Parameters:
- `Profits`: amount of profit made from producing one unit of Product p ⟶ `Profits[p] for p in Products`
- `ProcessTimes`: amount of time it takes to process Product p on Machine m ⟶ `ProcessTimes[m, p] for m in Machines for p in Products`
- `MaxTimes`: maximum amount of time available to use each Machine m ⟶ `MaxTimes[m] for m in Machines`
- `MaxDemand`: maximum amount of demand for Product p ⟶ `MaxDemand[p] for p in Products`

Decision Variables:
- `Produce`: number of units to produce of Product p ⟶ `Produce[p] for p in Products`

API Reference
-------------
See the corresponding section on its class