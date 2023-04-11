with variables (sucursal, tiempo) as (values({franchise_id}, '{tiempo}'))

select 
	date_trunc((select tiempo from variables), si.installation_date)::date as fecha_instalacion,
	count(*) as instalaciones
from 
	service_installation as si
join 
	contracts as c 
		on (c.id = si.contract_id)
where 
	c.franchise_id = (select sucursal from variables)
	and installation_date is not null
group by
	date_trunc((select tiempo from variables), si.installation_date)::date
order by
	date_trunc((select tiempo from variables), si.installation_date)::date desc
