# Shellshock Exploit

![Shellshock Exploit](https://img.shields.io/badge/Shellshock%20Exploit-v1.0-brightgreen)

## Descripción

Este proyecto es una implementación de un exploit de Shellshock, una vulnerabilidad de seguridad que afecta al intérprete Bash en sistemas Unix/Linux. El exploit permite ejecutar comandos en el servidor objetivo a través de una inyección de código en las cabeceras HTTP.

## Características

- **Shellshock Exploit**: Permite ejecutar comandos arbitrarios en el servidor objetivo utilizando la vulnerabilidad de Shellshock.

- **Selección de Proxy**: Puede configurarse para utilizar un proxy o conectarse directamente al servidor objetivo.

## Uso

1. Ejecute el programa proporcionando una dirección IP de destino.
2. Elija si desea utilizar un proxy o conectarse directamente al servidor.
3. Si selecciona el uso de un proxy, ingrese la dirección IP y el puerto del proxy.
4. El programa se pondrá a la escucha en el puerto 4443.
5. Ingrese el directorio `/cgi-bin/<dir>` donde se encuentra la vulnerabilidad Shellshock (por defecto: `status`).
6. El exploit se ejecutará y se establecerá una conexión con el servidor objetivo.

## Requisitos

- Python 3.x
- La biblioteca `requests`
- La biblioteca `pwn`

## Ejemplo de Uso

```bash
$ python3 ShellXock.py
or
$ ./ShellXock.py
```

## Notas

- Este programa está destinado únicamente para fines educativos y de investigación. El uso indebido o no autorizado de esta herramienta puede violar la ley.

- Asegúrese de que tiene permisos legales para realizar pruebas de seguridad en el servidor objetivo antes de utilizar este programa.


## Autor

- **B3XAL**


## Licencia

Este proyecto está bajo la Licencia MIT. Consulte el archivo [LICENSE](LICENSE) para obtener más detalles.


