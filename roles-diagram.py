from diagrams import Diagram
from diagrams.saas.analytics import Snowflake
import pandas as pd

# Read in Snowflake role relationships
df = pd.read_csv('roles.csv')

hierarchy = {}
for index, row in df.iterrows():
    if row["PARENT_ROLE"] not in hierarchy:
        hierarchy[row["PARENT_ROLE"]] = [row["CHILD_ROLE"]]
    else:
        hierarchy[row["PARENT_ROLE"]].append(row["CHILD_ROLE"])

# Create diagram
node_attr = {
    "fontsize": "10"
}

with Diagram("Snowflake Role Hierarchy", direction='TB', node_attr=node_attr) as diag:

    nodes = {}
    for parent, children in hierarchy.items():
        if parent.lower() + '_node' not in nodes:
            nodes[parent.lower() + '_node'] = Snowflake(parent)
        for child in children:
            if child.lower() + '_node' not in nodes:
                nodes[child.lower() + '_node'] = Snowflake(child)
            nodes[parent.lower() + '_node'] >> nodes[child.lower() + '_node']
