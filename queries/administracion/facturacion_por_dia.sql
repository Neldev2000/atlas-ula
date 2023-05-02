with variables (sucursal, dia) as (values({franchise_id}, '{dia}')),

facturas_usd as (select 
	cd.created_at::date as fecha_facturado, 
	document_number as factura, 
	CD.AMOUNT as monto,
	(cd.amount) / ((cd.exchange_rate->>'rate')::float) as monto_usd,
	CASE WHEN cd.exchange_rate->>'rate' = '1' then 'USD' END as divisa,
	sum(cd.amount) over(order by cd.document_number) as suma_monto
	
from 
	client_documents as cd

join
	proof_payments 
		using(client_document_id)
join 
	contracts 
		on(contracts.id = cd.contract_id)

where
	cd.type = 'invoice'
	and cd.status = 'paid'
	and cd.created_at::date   = (select to_date(dia, 'YYYY-MM-DD') from variables)
	and franchise_id = (select sucursal from variables)
	and cd.document_number  not like 'VT-%'
	AND cd.exchange_rate->>'rate' = '1'

order by cd.document_number 
),
facturas_ves as (
	select 
	cd.created_at::date as fecha_facturado, 
	document_number as factura, 
	CD.AMOUNT as monto,
	(cd.amount) / ((cd.exchange_rate->>'rate')::float) as monto_usd,
	CASE WHEN cd.exchange_rate->>'rate' != '1' then 'VES' END as divisa,
	sum(cd.amount) over(order by cd.document_number) as suma_monto
from 
	client_documents as cd

join
	proof_payments 
		using(client_document_id)
join 
	contracts 
		on(contracts.id = cd.contract_id)

where
	cd.type = 'invoice'
	and cd.status = 'paid'
	and cd.created_at::date   = (select to_date(dia, 'YYYY-MM-DD') from variables)
	and franchise_id = (select sucursal from variables)
	and cd.document_number  not like 'VT-%'
	AND cd.exchange_rate->>'rate' != '1'

order by cd.document_number 
)
(select * from facturas_ves
union
select * from facturas_usd

order by divisa, factura)