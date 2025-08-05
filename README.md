# Tarea 3 - Desarrollo de Apps Web CC5002

## Nombre: Sebastián Bustos Andrade

## Con respecto a la entrega
La entrega contiene los archivos de las tareas anteriores, junto con los nuevos archivos requeridos
en torno a la implementacion de los comentarios y AJAX. Además, debido a la mala o no implementación
de ciertos requerimientos de (principalmente) la tarea anterior, se programó todo lo correspondiente a
la tarea 2 para recien dar comienzo a la realización de la tarea 3, la cual fue lograda exitosamente
segun los requerimientos entregados

## Descripción General
Esta tarea consiste en la creación de una pagina que permita a los usuarios donar
dispositivos, proporcionando información sobre el dispositivo y el contacto; y al
mismo tiempo ver los dispositivos que han sido donados, ademas de la visualización
de ciertas estadisticas de la aplicación por medio de gráficos construidos con AJAX.

## Requisitos del Proyecto
- HTML5, CSS3, JavaScript, Flask, MySQL, AJAX

## Consideraciones
Según lo indicado en la tarea 2, para acceder a la base de datos es necesario utilizar un puerto y credenciales específicos. Para realizar y probar esta tarea, utilicé mis propias credenciales (usuario "root" y una contraseña arbitraria), junto con el puerto 5000, que es el puerto por defecto. Sin embargo, al cambiar el puerto a 3306, recibí el error "Intento de acceso a un socket no permitido por sus permisos de acceso".

Entiendo que este error no debería ocurrir al momento de revisar mi trabajo, pero en caso de que sí se presente, el único cambio realizado fue en las credenciales en el archivo de configuración y en la línea 291 de app.py. Por lo tanto, si el sistema no funciona correctamente, basta con eliminar dicha línea para restaurar la funcionalidad original.

