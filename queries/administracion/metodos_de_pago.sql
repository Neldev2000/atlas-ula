WITH variables (sucursal, moneda) as (
   values ({franchise_id}, '{moneda}')
)
select 
	payment_method, 
	100*count(*) / ( sum(count(*)) over() ) as proporcion

from 
	money_received as mnr 
WHERE 
	franchise_id = (select sucursal from variables)
	and currency_code = (select moneda from variables)
	and status = 'processed'
group by payment_method
order by count(*) desc