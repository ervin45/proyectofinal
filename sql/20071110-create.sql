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
    id_octosis integer NOT NULL,
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
   costo_pesos numeric(14,2),
   precio_vta numeric(14,2),
   compras integer,
   devoluciones integer,
   ventas integer, 
   ventas_por_taller integer,
   PRIMARY KEY (fk_tiempo, fk_pieza, fk_proveedor)

);

CREATE TABLE ft_compras (
   fk_tiempo integer,
   fk_pieza integer,
   fk_proveedor integer,
   fk_tipo_pieza integer,
   cantidad  integer,
   costo_pesos numeric(14,2),
   costo_dolar numeric(14,2),
   PRIMARY KEY (fk_tiempo, fk_pieza, fk_proveedor, fk_tipo_pieza)

);


CREATE TABLE td_tipo_venta (
    id serial CONSTRAINT tipo_venta_id_primary PRIMARY KEY,
    tipo_venta varchar(255)
) WITHOUT OIDS;


CREATE TABLE ft_ventas (
   fk_tiempo integer,
   fk_pieza integer,
   fk_proveedor integer,
   fk_tipo_venta integer,
   fk_tipo_pieza integer,
   cantidad  integer,
   precio_venta_pesos numeric(14,2),
   margen_pesos numeric(14,2),
   PRIMARY KEY (fk_tiempo, fk_pieza, fk_proveedor, fk_tipo_venta)
);

CREATE TABLE td_tipo_pieza (
    id serial CONSTRAINT td_tipo_pieza_id_primary PRIMARY KEY,
    tipo_pieza varchar(255)
) WITHOUT OIDS;

INSERT INTO td_tipo_pieza (tipo_pieza) VALUES ('Original');
INSERT INTO td_tipo_pieza (tipo_pieza) VALUES ('Alternativo');

update ft_ventas   set fk_tipo_pieza=1 where fk_proveedor =  1;
update ft_ventas   set fk_tipo_pieza=2 where fk_proveedor <> 1;
update ft_compras  set fk_tipo_pieza=1 where fk_proveedor =  1;
update ft_compras  set fk_tipo_pieza=2 where fk_proveedor <> 1;


CREATE TABLE ft_test (
   fk_tiempo integer,
   fk_pieza integer,
   fk_tipo_pieza integer,
   cantidad  integer,
   costo numeric(14,2),
   PRIMARY KEY (fk_tiempo, fk_pieza, fk_tipo_pieza)
);
