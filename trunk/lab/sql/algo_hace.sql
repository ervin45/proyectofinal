-- IVF_ITAMP0 (Unidades, cada instancia en particular) 
-- STS_ARTIC0 STS_ARTIC0 (Articulos y unidades)

SELECT *
FROM
 IVF_ITAMP0 I,
 STS_ARTIC0 S
WHERE
 I.ART_CODIGO = S.ART_CODIGO


-- IVF_ITAMP0 (Unidades, cada instancia en particular) 
-- IVF_ITMOP0 (Operaciones) OPE_NUMERO OPE_NROINT

SELECT *
FROM 
 IVF_ITMOP0 I,
 IVF_ITAMP0 IT
WHERE 
 I.OPE_NROINT = IT.ART_NUMERO