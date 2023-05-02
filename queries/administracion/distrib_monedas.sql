WITH variables (sucursal) as (
   values ({franchise_id})
)
select 
	currency_code, 
	100*count(*) / ( sum(count(*)) over() ) as proporcion

from 
	money_received as mnr 
WHERE 
	franchise_id = (select sucursal from variables)
	and status = 'processed'
group by currency_code
order by count(*) desc