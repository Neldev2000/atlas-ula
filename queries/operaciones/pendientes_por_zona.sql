with variables (sucursal) as ( values({franchise_id}) )
select 
	sec.name as sectores, count(sec.id) as pendientes
from 
	sectors as sec
join
	contract_addresses as ca on (ca.sector_id = sec.id)
join 
	contracts as c on (c.id = ca.contract_id)
where 
	c.franchise_id = (select sucursal from variables) and
	c.status = 'awaiting_installation' and
	ca.type = 'tech'
group by sec.name
order by
	count(sec.id) desc
limit 10