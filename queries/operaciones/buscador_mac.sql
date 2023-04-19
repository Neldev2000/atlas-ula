with variables (MAC) as (values('{MAC}'))

select 
	concat_ws(' ', first_name, last_name) as nombre,
	local_phone as telefono_fijo, 
	cellphone as telefono_celular,
	ca.address as direccion

from contract_services as cs
cross join json_array_elements(wan_config) as elm
join contract_contacts as cc using(contract_id)
join contract_addresses as ca using(contract_id)
where 
	lower((select MAC from variables)) like concat('%',lower(elm->>'MAC_ONU\/ONT'))
	and concat('%',lower(elm->>'MAC_ONU\/ONT')) != '%'
	and ca.type = 'tech'