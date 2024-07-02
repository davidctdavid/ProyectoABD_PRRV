CREATE ROLE rolectura;
GRANT CONNECT ON DATABASE broker TO rolectura;
GRANT USAGE ON SCHEMA public TO rolectura;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rolectura;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO rolectura;
CREATE USER usuariolectura WITH PASSWORD 'lectura';
GRANT rolectura TO usuariolectura;

CREATE ROLE rolsuper;
GRANT CONNECT ON DATABASE broker TO rolsuper;
GRANT USAGE ON SCHEMA public TO rolsuper;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO rolsuper;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, 
DELETE ON TABLES TO rolectura;
CREATE USER usuariosuper WITH PASSWORD 'super';
GRANT rolsuper TO usuariosuper;