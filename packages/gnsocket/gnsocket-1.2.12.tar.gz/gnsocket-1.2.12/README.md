GPS Network Socket
======================

Este módulo habilita la operación de un socket como *cliente* o *servidor*, soporta:

- socket unix
- socket tcp/ip
- ssl

Comunica la información serializada en estruturas de datos JSON. Permite tamaños grandes de información ya que empaqueta en pequeños trozos la información.

La clase principal, que puede ser utilizada para diversas implementaciones, es: *GNCSocket*.

Además, considerando que socket es una estructura para comunicar y usualmente deba ser usada de manera parmente y conexión continua, se implementan las siguientes clases.

- GNCSocketBase, que habilita métodos asíncronos para leer y escribir entre sockets, tomando información de colas o entregando a colas. Para comunicar con otros bloques.

Para esto, se heredan dos clases específicas que implementan de manera sencillas un *servidor* y un *cliente*.

- GNCSocketServer
- GNCSocketClient

En ambos casos, para cualquier programa, como por ejemplo una interfaz gráfica, bastará con entregarle una cola para recibir y una para entregar información (de estructuras Queue de python).


## Instalar

Para instalar será suficiente con pip

```bash
pip install gnsocket
```

Pero también, clonando el repositorio e instalando.

```bash
git clone https://gitlab.com/pineiden/gus.git
python setup.py install
```

## Habilitar los puertos para TCP

En caso de habilitar el *socket* como *server* en producción, será necesario que habilites el puerto seleccionado en firewall (si es que está habilitado).

## Realizar algunas pruebas

Dentro de la carpeta test, están los directorios *advance_x*, para probar los scripts basta ejecutar en dos terminales diferentes *server* y *client*.

Te recomiendo probar *test/advance* y *test/advance_ssl*.

## Más información, en la documentación

En el directorio doc existe un documento con información mas descriptiva.
