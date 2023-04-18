with variables (sucursal) as (values({franchise_id}))


select
	count(*) as ventas
from 
	service_installation as si 
join
	contracts as c on ( c.id = si.contract_id )
where
	c.franchise_id = (select sucursal from variables)
	and date_trunc('month',si.installation_date)::date = date_trunc('month',c.created_at  +1*interval '1 month' )::date 
	and date_trunc('month',si.installation_date)::date = date_trunc('month',now())::date
limit 1