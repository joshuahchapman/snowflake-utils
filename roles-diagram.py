from os import getenv
import snowflake.connector
import pandas as pd
from diagrams import Diagram
from diagrams.saas.analytics import Snowflake


def get_roles_from_file():
    df = pd.read_csv('roles.csv')
    return df


def get_roles_from_snowflake():
    ctx = snowflake.connector.connect(
        host=getenv("SNOWFLAKE_HOST"),
        user=getenv("SNOWFLAKE_USER"),
        password=getenv("SNOWFLAKE_PASSWORD"),
        role="ACCOUNTADMIN",
        account=getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=getenv("SNOWFLAKE_WAREHOUSE"),
        database="SNOWFLAKE",
        schema="ACCOUNT_USAGE",
        protocol='https',
        port=443)

    cur = ctx.cursor()
    sql = "select name as child_role, grantee_name as parent_role from snowflake.account_usage.grants_to_roles " \
          "where granted_on = 'ROLE' and privilege = 'USAGE'"
    cur.execute(sql)
    df = cur.fetch_pandas_all()
    return df


roles_df = get_roles_from_file()
# roles_df = get_roles_from_snowflake()
hierarchy = {}
for index, row in roles_df.iterrows():
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
