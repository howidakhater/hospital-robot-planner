import streamlit as st
from pyswip import Prolog
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

# Fix for numpy >= 2.0
if not hasattr(np, 'alltrue'):
    np.alltrue = np.all

# ------------------------
# Load Prolog
# ------------------------
prolog = Prolog()
prolog.consult("C:\\Users\\Abdel\\PycharmProjects\\app\\robot.pl")

st.title("Hospital Robot Planner with Animation")

# ------------------------
# User Inputs
# ------------------------
initial_location = st.selectbox("Initial Robot Location", ["corridor", "pharmacy", "room3"])
carrying = st.selectbox("Is Robot carrying medicine?", ["no", "yes"])

medloc = "robot" if carrying == "yes" else "pharmacy"
initial_state = f"state({initial_location}, {carrying}, {medloc})"

# ------------------------
# Define map graph
# ------------------------
G = nx.Graph()
G.add_edges_from([("pharmacy", "corridor"), ("corridor", "room3")])
pos = {'pharmacy': (0,0), 'corridor': (1,0), 'room3': (2,0)}

# ------------------------
# Extract locations and actions from plan
# ------------------------
def extract_plan(plan, start_loc):
    locations = [start_loc]
    actions = ["Start"]
    current = start_loc
    for action in plan:
        action_str = str(action)
        if action_str.startswith("move("):
            try:
                inside = action_str[5:-1]  # remove 'move(' and ')'
                src, dest = [x.strip() for x in inside.split(",")]
                current = dest
                locations.append(current)
                actions.append(f"Move to {dest}")
            except Exception as e:
                st.error(f"Failed to parse move action: {action_str}")
        elif "pick_up_medicine" in action_str:
            locations.append(current)          # location unchanged
            actions.append("Pick up medicine")
        elif "drop_medicine" in action_str:
            locations.append(current)          # location unchanged
            actions.append("Drop medicine")
    return locations, actions

# ------------------------
# Animate Plan
# ------------------------
if st.button("Compute Plan and Animate"):
    query = f"plan({initial_state}, [], Plan)"
    result = list(prolog.query(query))

    if result:
        plan = result[0]["Plan"]
        st.write("✅ Raw plan from Prolog:", plan)

        locations, actions = extract_plan(plan, initial_location)
        st.write("📍 Extracted locations:", locations)
        st.write("🔄 Actions:", actions)

        final_query = f"plan({initial_state}, [], _), goal_state(FinalState)"
        final_result = list(prolog.query(final_query))
        if final_result:
            st.write("🏁 Final State:", final_result[0]["FinalState"])

        plot_placeholder = st.empty()

        for i in range(len(locations)):
            plt.figure(figsize=(4,1))
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, font_size=12, width=2)

            if i > 0:
                path_edges = list(zip(locations[:i], locations[1:i+1]))
                if path_edges:
                    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=["red"]*len(path_edges), width=4)

            if i > 0:
                nx.draw_networkx_nodes(G, pos, nodelist=locations[:i], node_color="#FFA500", node_size=1200)

            nx.draw_networkx_nodes(G, pos, nodelist=[locations[i]], node_color="orange", node_size=1500)

            plt.text(pos[locations[i]][0], pos[locations[i]][1]+0.15, actions[i],
                     fontsize=10, fontweight='bold', ha='center')

            plot_placeholder.pyplot(plt)
            plt.close()
            time.sleep(1) 

    else:
        st.error("❌ No plan found. Please check the initial state or goal reachability.")