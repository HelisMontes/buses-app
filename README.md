# Entorno donde fue desarrollado:

- OS: Ubuntu 20.04 LTS
- Python: 3.8

### NOTA IMPORTANTE:
Antes de empezar con los comandos en consola se debe copiar el archivo ".env.example" a ".env"
Editar las variables según donde este ubicada la DB y el nombre de usuario que se quiere por defecto para el admin.

Para el admin se creara un usuario con el nombre indicado en el archivo ".env".


## Pasos a seguir:

## Crear el entorno virtual:

```bash
python3 -m venv .venv
```

## Activar el entorno virtual:

```bash
source .venv/bin/activate
```

## Instalar los requerimientos:
```bash
pip3 install -r requirements
```

## Por si hay algun error instalar wheel e intentar el paso anterior de nuevo:

```bash
pip3 install wheel
```

## Ejecutar las migraciones:
```bash
python3 manage.py migrate
```

## Ejecutar el servidor:
```bash
python3 manage.py runserver
```

## Archivos de documentacion:

[Diagrama UML de la DB](/documentation/buses-db-uml.png)
