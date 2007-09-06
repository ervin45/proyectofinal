--- Al parecer relaciona cliente con la unidad que compro

SELECT *
FROM 
 IVF_CLUNI0 C,
 IVF_ITMOP0 I
WHERE
 C.UNI_NUMOPE = I.OPE_NUMERO;