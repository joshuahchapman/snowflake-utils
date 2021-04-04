select name as child_role, grantee_name as parent_role
from snowflake.account_usage.grants_to_roles
where granted_on = 'ROLE'
and privilege = 'USAGE'
;