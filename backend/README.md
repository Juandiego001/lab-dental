### Migración base de datos

```bash
# crear una migración vacía
flask --app run db revision -m "Empty revision"

# crear nueva migración
flask --app run db migrate -m "Initial migration."

# aplicar migraciones
flask --app run db upgrade
```


### Internacionalización

```bash
# extraer palabras para ser traducidas
pybabel extract -F babel.cfg -o messages.pot .

# inicializar traducciones por idioma
pybabel init -i messages.pot -d core/translations -l es

# actualizar traducciones
pybabel update -i messages.pot -d core/translations

# compilar traducciones
pybabel compile -d core/translations
```