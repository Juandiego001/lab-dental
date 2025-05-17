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
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
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
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 5, true, true, true, true);

-- Inserción de permiso de visualización de categories
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 6, true, true, true, true);

-- Inserción de permiso de visualización de installations
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 7, true, true, true, true);

-- Inserción de permiso de visualización de equipments
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 8, true, true, true, true);

-- Inserción de permiso de visualización de warranties
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 9, true, true, true, true);

-- Inserción de permiso de visualización de distributors
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 10, true, true, true, true);

-- Inserción de permiso de visualización de manuals
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 11, true, true, true, true);

-- Inserción de permiso de visualización de forums
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 3, true, true, true, true);

-- Inserción de permiso de visualización de brands
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 12, true, true, true, true);

-- Inserción de permiso de visualización de strapi
INSERT INTO permissions(group_id, module_id, "read", "create", "update", "delete")
VALUES (1, 4, true, true, true, true);