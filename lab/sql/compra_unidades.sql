--- Tabla de Compras.
--- solo 301 y 306, Factura A, hay 29 registros excluidos

--- falta relacionar las ciudad, provincia, pais.

SELECT
   '1' as Cantidad,
   MONTH(D.FAC_FECEMI) as Mes,
   YEAR(D.FAC_FECEMI) as Anio,
   I.OPE_IMPORT as Importe,
   I.OPE_NUMERO,
   D.FAC_NROSUC as Sucursal,
   U.ART_COLOR as Color,
   X.ART_DESCRI as Descripcion,
   X.SUBGRUPO as Subgrupo,
   X.GRUPO as Grupo,
   X.MARCA as Marca,
   H.CLI_NOMBRE as Nombre,
   H.CLI_CIUDAD as Ciudad,
   H.CLI_PROVIN as Provincia,
   H.CLI_PAIS as Pais,
   CONCAT(D.DOC_LETRA,'-',FAC_NROSUC,'-',D.FAC_NROFAC) as Factura
FROM
   PVD4_FACTU D
   JOIN IVF_ITMOP0 I ON (D.FAC_NROINT = I.OPE_NROINT)
   INNER JOIN STS_UNIDA0 U ON (I.OPE_NUMERO = U.OPE_NUMERO)
   JOIN X_PROYECTO_VEHICULOS X ON (X.ART_CODIGO = U.ART_CODIGO)
   INNER JOIN IVF_CLUNI0 C ON (C.UNI_NUMOPE = I.OPE_NUMERO)
   JOIN IVF_CLIEN0 H ON ( C.UNI_NUMOPE = H.CLI_CODIGO )
WHERE
   (FAC_PROVEE =  '00301' OR FAC_PROVEE = '00306')
   AND U.ART_DEFCOD = '3'
   AND D.DOC_LETRA = 'A'