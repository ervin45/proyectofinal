--- Esta MAL el orden de los grupos.
--- M. Benz los realiza de otra manera!

SELECT 
 substring(A.ART_CODIGO, 7, 2)  as Grupo1,
 substring(A.ART_CODIGO, 9, 1)  as Grupo2,
 substring(A.ART_CODIGO, 12, 2) as Grupo3,
 substring(A.ART_CODIGO, 10, 2) as Grupo4,
 substring(A.ART_CODIGO, 4, 2)  as Grupo5,
 substring(A.ART_CODIGO, 6, 1)  as Grupo6,
 substring(A.ART_CODIGO, 20, 3) as Proov,
 A.ART_DESCRI as Descripcion,
 SUM( IF( M.ART_TIPMOV LIKE 'S%', - M.ART_CANTID, M.ART_CANTID ) ) AS Stock
FROM
 `STS_ARTIC0` A 
 Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD` = 'A'
  and substring(A.ART_CODIGO, 7, 2)='72'
  and substring(A.ART_CODIGO, 9, 1) = '7'
GROUP BY 
 A.ART_CODIGO