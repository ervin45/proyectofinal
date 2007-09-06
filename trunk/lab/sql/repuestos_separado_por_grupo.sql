--- Esta MAL el orden de los grupos.
--- M. Benz los realiza de otra manera!

SELECT
 substring(ART_CODIGO, 7, 2)  as Grupo1,
 substring(ART_CODIGO, 9, 1)  as Grupo2,
 substring(ART_CODIGO, 12, 2) as Grupo3,
 substring(ART_CODIGO, 10, 2) as Grupo4,
 substring(ART_CODIGO, 4, 2)  as Grupo5,
 substring(ART_CODIGO, 6, 1)  as Grupo6,
 substring(ART_CODIGO, 20, 3) as Proov,
 ART_DESCRI as Descripcion
FROM
 `STS_ARTIC0`
WHERE
 `ART_DEFCOD` = 'A'
  and substring(ART_CODIGO, 7, 2)='72'
  and substring(ART_CODIGO, 9, 1) = '7'
Order By Grupo1, Grupo2, Grupo3, Grupo4, Grupo5