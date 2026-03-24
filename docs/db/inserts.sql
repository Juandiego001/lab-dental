-- Inserción de datos de prueba de Usuarios
INSERT INTO users(
    full_name,
    email,
    password
)
VALUES (
    'Administrador',
    'juandiego14012003@gmail.com',
    '$2b$12$MXknq8MdOIZIpwnAVNRZD.rM3iWzWPCB.c5vohyqQo8N2Qd03WhyO',
);


-- Inserción de grupo administradores
INSERT INTO groups(name) VALUES ('Administradores');

-- Inserción de módulos
INSERT INTO modules(name) VALUES ('users'), ('groups'), ('forums'), ('strapi');

-- Inserción de permisos
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES
(1, 1, true, true, true, true),
(1, 2, true, true, true, true);

-- Inserción de user_groups
INSERT INTO user_groups(user_id, group_id)
VALUES (3, 1);

-- Inserción de módulo de brands
INSERT INTO modules(name) VALUES ('brands');

-- Inserción de módulo de categories
INSERT INTO modules(name) VALUES ('categories');

-- Inserción de módulo de zones
INSERT INTO modules(name) VALUES ('zones');

-- Inserción de módulo de installations
INSERT INTO modules(name) VALUES ('installations');

-- Inserción de módulo de equipments
INSERT INTO modules(name) VALUES ('equipments');

-- Inserción de módulo de warranties
INSERT INTO modules(name) VALUES ('warranties');

-- Inserción de módulo de distributors
INSERT INTO modules(name) VALUES ('distributors');

-- Inserción de módulo de manuals
INSERT INTO modules(name) VALUES ('manuals');

-- Inserción de módulo de configuration
INSERT INTO modules(name) VALUES ('configuration');

-- Inserción de módulo de forums
INSERT INTO modules(name) VALUES ('forums');

-- Inserción de módulo de strapi
INSERT INTO modules(name) VALUES ('strapi');

-- Inserción de permiso de visualización de searches
-- Validar ID del módulo y del grupo!
-- Inserción de permiso de visualización de zones
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 5, true, true, true, true);

-- Inserción de permiso de visualización de categories
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 6, true, true, true, true);

-- Inserción de permiso de visualización de installations
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 7, true, true, true, true);

-- Inserción de permiso de visualización de equipments
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 8, true, true, true, true);

-- Inserción de permiso de visualización de warranties
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 9, true, true, true, true);

-- Inserción de permiso de visualización de distributors
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 10, true, true, true, true);

-- Inserción de permiso de visualización de manuals
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 11, true, true, true, true);

-- Inserción de permiso de visualización de forums
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 3, true, true, true, true);

-- Inserción de permiso de visualización de brands
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 12, true, true, true, true);

-- Inserción de permiso de visualización de strapi
INSERT INTO permissions(group_id, module_id, 'read', 'create', 'update', 'delete')
VALUES (1, 4, true, true, true, true);


-- Nuevas categorias de Pipe
INSERT INTO categories(name, slug, status, created_at, updated_at) VALUES ('TRUCK WHEEL ALIGNERS', 'Truck-aligner', 'ACTIVE', NOW(), NOW());
INSERT INTO categories(name, slug, status, created_at, updated_at) VALUES ('ATF', 'Atf-machine', 'ACTIVE', NOW(), NOW());


-- Equipos instalados por Pipe
/*
Sun, ATF, Y1ATF020S000  , ATF GEARKARE, 
Ecotechnics, ATF, Y1ATF0000000, ATF MOOVETECH, 
Ecotechnics, AIR CONDITIONERS, Y3NP40000000, ECK NEXT PRO HYBRID, 
Ecotechnics, AIR CONDITIONERS, K5V2A000000H, ECK LAND HFO, 
Ecotechnics, AIR CONDITIONERS, K5V2A000000A, ECK LAND, 
Ecotechnics, AIR CONDITIONERS, K6T5A000000B, ECK TWIN12, 
Ecotechnics, AIR CONDITIONERS, XK456A170S51, KOOLKARE HD S / SUN ECK BUS-PRO, 
Ecotechnics, AIR CONDITIONERS, XK456A000051, ECK BUS-PRO N2, 
Ecotechnics, AIR CONDITIONERS, K6T5A090S00B, SUN DUAL GAS 12, 
Ecotechnics, AIR CONDITIONERS, Y2F20020S000, QTECH IV 230V, 
Ecotechnics, AIR CONDITIONERS, Y2F200000000, ECK FLAG 230V, 
Ecotechnics, AIR CONDITIONERS, Y2N20020S000, BREEZE IV 230V + PRINTER, 
Ecotechnics, AIR CONDITIONERS, Y2N200000000, ECK NEXT WITH PRINTER ASSEMBLED 230V
*/



INSERT INTO distributors(name) VALUES ('COMERCIALIZADORA DE LLANTAS');
INSERT INTO distributors(name) VALUES ('JOHN CAR ');
INSERT INTO distributors(name) VALUES ('TRIVIUM');
INSERT INTO distributors(name) VALUES ('LUCAS BLANDFORD');
INSERT INTO distributors(name) VALUES ('EMASA CHILE');
INSERT INTO distributors(name) VALUES ('PETINSA');
INSERT INTO distributors(name) VALUES ('HERRACRUZ ');
INSERT INTO distributors(name) VALUES ('AUTOREX');
INSERT INTO distributors(name) VALUES ('TECNOVA');
INSERT INTO distributors(name) VALUES ('LATSY VENEZUELA');
INSERT INTO distributors(name) VALUES ('AUTOTOOLS');
INSERT INTO distributors(name) VALUES ('LATSY PANAMA');
INSERT INTO distributors(name) VALUES ('MYERS PANAMÁ ');
INSERT INTO distributors(name) VALUES ('COÉXITO');
INSERT INTO distributors(name) VALUES ('INNOVATEC');
INSERT INTO distributors(name) VALUES ('COLLISION');
INSERT INTO distributors(name) VALUES ('GN REPRESENTACIONES');
INSERT INTO distributors(name) VALUES ('RJ SOLUCIONES');
INSERT INTO distributors(name) VALUES ('GRUPO COMETA');
INSERT INTO distributors(name) VALUES ('SNAP-ON MÉXICO ');
INSERT INTO distributors(name) VALUES ('PG IMPORT');
INSERT INTO distributors(name) VALUES ('TÉCNICA DE SERVICIOS');
INSERT INTO distributors(name) VALUES ('CENTHRO');
INSERT INTO distributors(name) VALUES ('PREAUTO');
INSERT INTO distributors(name) VALUES ('ALFATEC AUTOMOTRIZ');
INSERT INTO distributors(name) VALUES ('LAUGHLIN & GANNES ');
INSERT INTO distributors(name) VALUES ('ETAPEL');
INSERT INTO distributors(name) VALUES ('OPERADORA DE MERCADO DE LLANTAS');
INSERT INTO distributors(name) VALUES ('VELYMEX');
INSERT INTO distributors(name) VALUES ('MYERS GUATEMALA');
INSERT INTO distributors(name) VALUES ('LA META');
INSERT INTO distributors(name) VALUES ('MYERS SALVADOR');
INSERT INTO distributors(name) VALUES ('REMSA');
INSERT INTO distributors(name) VALUES ('TROPICAL BATTERY');
INSERT INTO distributors(name) VALUES ('MASSY MOTORS');
INSERT INTO distributors(name) VALUES ('NOGUERA AUTOCENTER');
INSERT INTO distributors(name) VALUES ('ACO');
INSERT INTO distributors(name) VALUES ('AMSA COLOMBIA');
INSERT INTO distributors(name) VALUES ('AMSA ECUADOR');
INSERT INTO distributors(name) VALUES ('AMSA PERÙ');
INSERT INTO distributors(name) VALUES ('MANZ');
INSERT INTO distributors(name) VALUES ('AMSA CHILE');
INSERT INTO distributors(name) VALUES ('Test');


INSERT INTO clients(name, phone) VALUES ('PASAJEROS ALLINBUS S.A.C.','+51')



'Juan Cobo', 'juan_diego', 'juan_diego.cobo@uao.edu.co', '$2b$12$RhR6vqbcjkyUxov1ANJYFeS8rYnyuhWs9Zw7vx.TAQ9y4oox7GuFe', 'DISTRIBUTOR', 'es', 'ACTIVE', '2026-03-04 11:20:10.85915', '2026-03-04 11:20:10.859156');
'Andres Felipe Leon Manzano', 'andres.leon', 'andres.leon@snapon.com', '$2b$12$Aa2NIMdaAYPeP4LeiDXbEORVklZCy4r1QIiEB/zk4pUSGsiaRyK8e', 'ADMIN', 'es', 'ACTIVE', '2026-03-04 11:25:26.745353', '2026-03-09 14:41:13.864963');
'MIGUEL HERNAN CORDOBA PREDO', 'miguel.cordoba', 'miguel.cordobaprado@snapon.com', '$2b$12$F9jRsuElQWCUTyV6XPtfkeDkppKCLWig7rtVrph5s4/jXVPvmA4uK', 'ADMIN', 'es', 'ACTIVE', '2026-03-09 14:37:34.459857', '2026-03-10 16:49:56.999245');
'JUAN CARLOS QUIJANDRIA', 'Juan.quijandria', 'logistica@collasac.com', '$2b$12$jFcu0ug2kbr/.yCd8fFKgO51N6ypr0GD17dyqaHUvz3L4Jt1sDCr2', 'DISTRIBUTOR', 'es', 'ACTIVE', '2026-03-09 14:16:42.848469', '2026-03-10 16:52:47.247347');
'Juan Diego Cobo Cabal', 'juan', 'juandiego14012003@gmail.com', '$2b$12$X7dhm0Idj49oUtZvzyJxd.ddFa7rvfilqaW4dzbkz0qYqs16uVrAi', 'ADMIN', 'es', 'ACTIVE', '2026-03-04 11:17:20.828292', '2026-03-15 18:08:31.96055');