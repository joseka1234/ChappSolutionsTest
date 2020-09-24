# Prueba Candidatos ChappSolutions

Código buscador y reserva de habitaciones de hotel para la prueba de candidatos de ChappSolutions

# Puesta en marcha

Instalar los requisitos

````
pip install -r requirements.txt
python manage.py runserver 8000
````

# Tests

Para ejecutar los tests:

````
python manage.py test
````

# Documentación

La documentación ya está generada dentro del directorio docs.

### Documentación HTML

Está ubicada dentro de `docs/build/html` abriendo el archivo `index.html`.

### Documentación PDF

Está ubicada dentro de `docs/build/rinoh` abriendo el archivo `buscador.pdf`.

### Generar documentación

En caso de querer generar la documentación basta con ejecutar el archivo make situado dentro de `docs`

**Para generar documentación en HTML**:

````
make.bat html # En Windows
make html # En Linux
````
**Para generar documentación en PDF**:

````
make.bat pdf # En Windows
make pdf # En Linux
````