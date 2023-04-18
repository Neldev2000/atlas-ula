with variables (sucursal, tiempo) as (values({franchise_id}, '{tiempo}'))
select 
	date_trunc( (select tiempo from variables), cd.created_at )::date as fecha,
	case
		when exchange_rate->>'rate' = '1' then 'USD'
		else 'VES'
	end as moneda
from 
	client_documents as cd 
join 
	contracts as c on (c.id = cd.contract_id)
where
	c.franchise_id = (select sucursal from variables)
	and document_number like 'VT-%'
order by date_trunc( (select tiempo from variables), cd.created_at )::date desc