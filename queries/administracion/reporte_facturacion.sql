with variables (sucursal, tiempo) as (values({franchise_id}, '{tiempo}')),
tasas as (
	select distinct  
	cd.created_at::date , 
	avg((exchange_rate->>'rate')::float) as tasa
	from client_documents as cd
join contracts on (contracts.id = cd.contract_id)
where 
	cd.created_at::date = (exchange_rate->>'created_at')::date 
	and franchise_id = (select sucursal from variables)
	and cd.type = 'invoice'
	and cd.status = 'paid'
	and cd.document_number  not like 'VT-%'
group by cd.created_at::date
order by cd.created_at::date desc
), 
factura_bs as (
	-- DINERO FACTURADO EN bs
select  
	cd.created_at::date,
	sum(amount) as monto_bs
from 
	client_documents as cd
join contracts on (contracts.id = cd.contract_id)
where
	(exchange_rate->>'rate')::float > 1
--	and cd.created_at::date = '2022-08-04'
	and franchise_id = (select sucursal from variables)
	and cd.type = 'invoice'
	and cd.status = 'paid'
	and cd.document_number  not like 'VT-%'
group by cd.created_at::date
order by cd.created_at::date desc
),
factura_usd as (
	-- DINERO FACTURADO EN USD
with variables (sucursal) as (values(1))
select  
	cd.created_at::date,
	sum(amount) as monto_usd
from 
	client_documents as cd
join contracts on (contracts.id = cd.contract_id)
where
	(exchange_rate->>'rate')::float = 1
	and franchise_id = (select sucursal from variables)
	and cd.type = 'invoice'
	and cd.status = 'paid'
	and cd.document_number  not like 'VT-%'
group by cd.created_at::date
order by cd.created_at::date desc
)

select 
	date_trunc((select tiempo from variables),factura_bs.created_at)::date as tiempo,
	sum(monto_bs) as  monto_bs,
	sum(monto_usd) as monto_usd,
	avg(tasas.tasa) as tasa_promedio,
	sum((monto_bs / tasas.tasa) + monto_usd) as total_usd
from 
	factura_bs
join
	factura_usd using(created_at)
join
	tasas using(created_at)
group by date_trunc((select tiempo from variables),factura_bs.created_at)::date
order by date_trunc((select tiempo from variables),factura_bs.created_at)::date desc