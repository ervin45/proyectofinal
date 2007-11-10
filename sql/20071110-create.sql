;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

CREATE TABLE td_pieza (
    id serial CONSTRAINT pieza_id_primary PRIMARY KEY,
    grupo_constructivo integer NOT NULL,
    modelo integer NOT NULL,
    modificacion integer NOT NULL,
    pieza integer NOT NULL,
    descripcion varchar(255),
    codigo varchar(255)
) WITHOUT OIDS;

CREATE TABLE td_proveedor (
    id serial CONSTRAINT proveedor_id_primary PRIMARY KEY,
    proveedor varchar(255)
) WITHOUT OIDS;


CREATE TABLE td_tiempo (
    id serial CONSTRAINT tiempo_id_primary PRIMARY KEY,
    anio integer NOT NULL,
    mes integer NOT NULL
) WITHOUT OIDS;

CREATE TABLE ft_movimientos (
   fk_tiempo integer,
   fk_pieza integer,
   fk_proveedor integer,
   stock  integer,
   costo_pesos integer,
   precio_vta integer,
   compras integer,
   devoluciones integer,
   ventas integer, 
   ventas_por_taller integer,
   PRIMARY KEY (fk_tiempo, fk_pieza, fk_proveedor)

);


