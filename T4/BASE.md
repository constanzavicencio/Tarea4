# Tarea 3: DCCome Lechuga 🐢🍉🥬


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Entidades: 18.5 pts (21%)
##### ✅ Pepa
##### ✅ Sandías

#### Interfaz gráfica: 27 pts (30%)
##### ✅ Ventana Inicio
##### ✅ Ventana Juego
##### ✅ Fin del *puzzle*

#### Interacción: 13 pts (14%)
##### ✅ *Cheatcodes*
##### 🟠 Sonidos (hechos con _pygame_)

#### *Networking*: 20.5 pts (23%)
##### 🟠 Arquitectura
##### ✅ *Networking*
##### ✅ Codificación y decodifición

#### Archivos: 11 pts (12%)
##### 🟠 *sprites*
##### ✅ *puzzle*
##### ✅ JSON
##### ✅ parámetros.py


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` de ```cliente```, mediante el comando ```python main.py 8000``` desde la terminal. Además se debe contar con los siguientes archivos y directorios adicionales:
1. ```frontend.py``` en ```cliente```
2. ```backend.py``` en ```cliente```
3. ```config.json``` en ```cliente```
4. ```parametros.py``` en ```cliente```
5. ```main.py``` en ```servidor```
6. ```config.json``` en ```servidor```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```pygame```: se importa completo (debe instalarse)
2. ```PyQt6```: ```QtWidgets```, ```QtCore```, ```QtGui``` (debe instalarse ````PyQt6```)
3. ```socket```: se importa completo
4. ```sys```: se importa completo
5. ```numpy```: se importa completo
6. ```os```: se importa completo
7. ```random```: se importa completo
8. ```threading```: módulos ```Thread``` y ```Event```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```backend```: Contiene al backend de cliente
2. ```frontend```: Contiene al frontend de cliente

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para los cheatcodes hay que presionar las teclas en orden, manteniéndolas presionadas.
2. En mi computador se activa bloquea el teclado de Windows si aprieto 4 teclas a la vez, por lo que no pude testear el cheatcode MUTE :c pero estimo que debiera funcionar.
3. Para el usuario de juego se requiere un nombre alfanumérico con al menos un número y una mayúscula (ejemplo: Coni1).

PD: Dado que no logré implementar los sonidos con PyQt6, lo hice con pygame. Entiendo que esto no está permitido y entiendo si no se me llega a dar puntaje con ello. Lo aclaro para que no se malentienda que pretenda disimularlo :c lo hice con eso porque quedaba más cute que sin sonido.


-------