WITH variables (sucursal) as (
   values ({franchise_id})
),
	clientes_promocion as (
	select 
	now()::date as hoy, 
	count(*) as promocion 
	from contracts as c
	where 
		c.franchise_id = (select sucursal from variables) 
		and date_trunc('month', c.created_at)::date = date_trunc('month', now())::date
	),
	cortados_viejos as (
		SELECT now()::date as hoy, count(*) as cortados_viejos from contracts as c
join contract_services as cs on (cs.contract_id = c.id)
where 
	c.franchise_id = (select sucursal from variables)
	and cs.status like '%suspended%'
	and c.updated_at <= date_trunc('month',now() - 3*interval '1 month')::date 
	),
	cortados_nuevos as (
		SELECT now()::date as hoy, count(*) as cortados_nuevos from contracts as c
join contract_services as cs on (cs.contract_id = c.id)
where 
	c.franchise_id = (select sucursal from variables)
	and cs.status like '%suspended%'
	and c.updated_at > date_trunc('month',now() - 3*interval '1 month')::date 
	),
	exonerados as (
		select 
		now()::date as hoy,
	COUNT(*) as exonerados
from 
	contracts as c
join
	contract_services as cs 
		on (c.id = cs.contract_id)
join service as serv
		on (serv.id = cs.service_id)
where
	c.franchise_id = (select sucursal from variables)
	and upper(serv.name) like '%EXONERADO%' 
	), 
	contratos_totales as (
		select now()::date as hoy,  count(*) as contratos_totales from contracts as c
where
	c.franchise_id = (select sucursal from variables)
	), pendientes as (
		select now()::date as hoy, count(*) as pendientes from contracts
		where 
			franchise_id = (select sucursal from variables)
			and status = 'awaiting_installation'
			
	)



select 
	contratos_totales - exonerados - cortados_viejos - cortados_nuevos as clientes_que_pagan,
	promocion,
	exonerados, 
	cortados_nuevos,
	cortados_viejos,
	pendientes
	
from 
	clientes_promocion 
join
	cortados_nuevos using(hoy)
join 
	cortados_viejos using(hoy)
join
	exonerados using(hoy)
join
	contratos_totales using(hoy)
join
	pendientes using(hoy)