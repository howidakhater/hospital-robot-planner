# Hospital Robot Planner with Animation

A Streamlit application for planning a hospital robot's movements using Prolog, with an animated visualization of the plan on a simple graph.

## Features
- Select the robot's initial location and whether it is carrying medicine.
- Compute a plan using Prolog predicates.
- Display the plan step by step with a graph showing the path and actions.
- Show the raw plan, extracted locations, and actions.

## Requirements
- Python 3.8 or later.
- SWI-Prolog installed (required for the `pyswip` library).
- Install the libraries listed in `requirements.txt`:
  ```bash
  pip install -r requirements.txt
