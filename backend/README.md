### Migración base de datos

```bash
# aplicar migraciones
flask --app run db upgrade

# crear nueva migración
flask --app run db migrate -m 'Initial migration.'
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