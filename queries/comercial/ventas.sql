with variables (sucursal, tiempo) as (values({franchise_id}, '{tiempo}'))

select 
	date_trunc( (select tiempo from variables), c.created_at )::date as fecha_venta,
	count(*) as ventas 
from contracts as c
where 
	c.franchise_id = (select sucursal from variables)
group by
	date_trunc( (select tiempo from variables), c.created_at )::date 
order by 
	date_trunc( (select tiempo from variables), c.created_at )::date desc