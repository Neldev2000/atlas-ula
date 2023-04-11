with variables (sucursal) as ( values({franchise_id}) )
select 
	count(*) as pendientes
from contracts as c 
where 
	c.franchise_id = (select sucursal from variables) and
	c.status = 'awaiting_installation' 
