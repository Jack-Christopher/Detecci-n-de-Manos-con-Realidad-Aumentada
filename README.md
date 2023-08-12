# Proyecto de Detección de Manos con Realidad Aumentada

¡Bienvenidos al proyecto de Realidad Aumentada con Detección de Manos! Este Readme detalla el desarrollo de un emocionante sistema que combina la visión por computadora y la computación gráfica para crear una experiencia inmersiva de realidad aumentada.

## Descripción

El objetivo principal de este proyecto es permitir la interacción entre el mundo real y un entorno virtual en 3D utilizando tecnologías de vanguardia. Para lograrlo, hemos utilizado las poderosas bibliotecas OpenCV y OpenGL. Hemos implementado un sistema que es capaz de detectar manos en tiempo real mediante OpenCV y luego superponer estas manos en un entorno virtual, generando una experiencia de realidad aumentada única.

## Metodología

**1. Captura de video:** Configuramos una cámara para capturar video en tiempo real utilizando la biblioteca OpenCV. Esto nos proporciona el flujo continuo de imágenes necesario para la detección de manos y la interacción con el entorno virtual.

**2. Detección de manos:** Utilizamos el modelo de detección de objetos MediaPipe de OpenCV para identificar la posición de las manos en cada frame capturado. Esta detección es esencial para la interacción fluida entre el usuario y el entorno 3D.

**3. Preprocesamiento:** Antes de enviar los datos a OpenGL, realizamos un procesamiento en las imágenes de las manos detectadas para ajustar su tamaño y orientación de acuerdo a los requisitos de la renderización en 3D. Esto asegura una integración perfecta de las manos en el entorno virtual.

**4. Renderización con OpenGL:** Creamos un entorno 3D utilizando OpenGL, definiendo los vértices, shaders y otros elementos necesarios. Empleamos la biblioteca GLFW para gestionar ventanas y eventos, y generamos objetos 3D mediante clases que almacenan información sobre vértices y shaders. Además, capturamos frames de OpenCV y los renderizamos como texturas en el entorno 3D, creando así el fondo virtual.

**5. Realidad Aumentada:** Superponemos las imágenes de las manos detectadas en tiempo real sobre el entorno 3D virtual, creando una experiencia de realidad aumentada envolvente. Utilizamos técnicas avanzadas de texturización para combinar los frames de OpenCV con los objetos 3D, logrando una fusión perfecta.

**6. Interacción:** Implementamos colisiones entre las manos detectadas y los objetos renderizados en OpenGL, lo que permite al usuario mover y empujar los objetos virtuales en respuesta a los movimientos detectados. La superposición de las manos en el entorno virtual crea una experiencia inmersiva de realidad aumentada.

**7. Optimización y Pruebas:** Refactorizamos el código para optimizar el rendimiento, eliminando bloques innecesarios y liberando memoria. Ajustamos los parámetros de detección de manos proporcionados por MediaPipe para mejorar la velocidad de detección. Realizamos pruebas exhaustivas para garantizar que la interacción, la detección de manos y la renderización 3D funcionen sin problemas, proporcionando una experiencia de usuario fluida y envolvente.

Este proyecto representa un emocionante paso hacia adelante en la fusión entre el mundo real y el virtual. ¡Esperamos que disfruten explorando esta experiencia de realidad aumentada tanto como nosotros disfrutamos desarrollándola! Siéntase libre de explorar el código y compartir sus comentarios y sugerencias.


## Módulos de proyecto

### Módulo: Background

El archivo `background.py` contiene la implementación de una clase llamada `Background`, que se encarga de crear y mostrar un fondo con una textura. Esta clase es utilizada para establecer un fondo 3D en el entorno virtual y es una parte fundamental del proyecto de realidad aumentada. Las principales responsabilidades de este módulo son:

1. **Carga de Textura:** La clase `Background` carga una imagen desde un archivo y la convierte en una textura utilizada como fondo del entorno 3D.

2. **Creación de Shaders:** Se compilan los shaders (fragmento de código ejecutado en la GPU) necesarios para la renderización del fondo.

3. **Definición de Vértices:** Se establecen los vértices del cuadrado en el que se renderizará la textura, junto con las coordenadas de textura correspondientes.

4. **Creación de VAO:** Se configura el Vertex Array Object (VAO), que es una estructura que almacena la configuración de los datos de vértices para su uso en la renderización.

5. **Renderización:** Se proporciona un método para dibujar el fondo, que utiliza los shaders, la textura y los datos de vértices previamente configurados.

El módulo `Background` es esencial para lograr la experiencia de realidad aumentada, ya que establece el contexto visual en el que se superponen las manos detectadas.



### Módulo: Cube

El archivo `cube.py` contiene la implementación de la clase `Cube`, que representa un cubo en un entorno 3D. Esta clase es esencial para renderizar objetos 3D en el entorno de realidad aumentada. Las principales responsabilidades de este módulo son:

1. **Inicialización del Cubo:** La clase `Cube` se inicializa con las coordenadas del centro del cubo, su lado, y opcionalmente, el color del cubo.

2. **Renderización del Cubo:** El método `draw` permite renderizar el cubo con su respectivo color en el entorno 3D.

3. **Actualización del Cubo:** El método `update` se encarga de actualizar los vértices del cubo, realizar transformaciones (rotaciones) y cargar los datos en la tarjeta gráfica para la renderización.

4. **Movimiento del Cubo:** El método `move` permite cambiar la posición del cubo en el entorno 3D, lo cual es útil para la interacción con las manos detectadas.

5. **Zoom del Cubo:** El método `zoom` ajusta el tamaño del cubo según su distancia al observador, lo que es importante para crear una experiencia más realista en la realidad aumentada.

Este módulo, junto con la clase `Background` del módulo `Background`, proporciona las bases para la renderización de objetos 3D en el entorno virtual, lo que permite una interacción más inmersiva en la experiencia de realidad aumentada.


### Módulo: Hand

El archivo `hand.py` contiene la implementación de la clase `Hand`, que representa la detección y renderización de una mano en el entorno 3D. Esta clase es esencial para interactuar con objetos virtuales en el proyecto de realidad aumentada. Las principales responsabilidades de este módulo son:

1. **Inicialización de la Mano:** La clase `Hand` se inicializa con una serie de landmarks (puntos característicos) que representan los dedos y la palma de la mano detectada.

2. **Renderización de la Mano:** El método `draw` permite renderizar la mano en el entorno 3D, representando los dedos y la palma con líneas de un color específico.

3. **Actualización de la Mano:** El método `update` se encarga de actualizar las líneas que representan los dedos y la palma de la mano, creando así una representación precisa de la mano en el entorno virtual.

4. **Colisiones:** El método `collides` verifica si una serie de vértices (por ejemplo, los vértices de un objeto virtual) colisiona con alguna parte de la mano detectada. Esta funcionalidad es crucial para lograr interacciones más realistas en la realidad aumentada.

5. **Limpieza:** El método `clean` elimina las líneas previamente creadas para evitar la acumulación de representaciones de la mano en cada actualización.

Este módulo es fundamental para permitir que las manos detectadas interactúen con objetos virtuales y es un componente crucial para crear una experiencia de realidad aumentada inmersiva.


### Módulo: Main

El archivo `main.py` es el punto de entrada principal del proyecto de realidad aumentada. Este módulo se encarga de la integración de las funcionalidades de detección de manos, renderización 3D de objetos (cubos) y la implementación de interacciones en el entorno virtual. A continuación, se presenta un resumen de las principales responsabilidades de este módulo:

1. **OpenGL y GLFW Initialization:** Se inicializa la ventana de OpenGL utilizando las funciones de GLFW para el manejo de las ventanas y eventos. También se preparan las bibliotecas necesarias para OpenGL.

2. **OpenCV Initialization:** Se inicializan las bibliotecas OpenCV y MediaPipe para la detección de manos en tiempo real.

3. **Renderización de Cubos:** Se crean instancias de la clase `Cube` para representar dos cubos en el entorno 3D, cada uno con su propio color y posición.

4. **Detección de Manos:** Se inicia un ciclo que captura imágenes de la cámara utilizando OpenCV y detecta las manos en las imágenes utilizando el modelo de detección de manos de MediaPipe.

5. **Actualización de la Representación de las Manos:** Se actualiza la representación de las manos en el entorno 3D, utilizando instancias de la clase `Hand`. Las posiciones de las manos detectadas se actualizan y se verifica si hay colisiones con los cubos.

6. **Renderización del Fondo:** Se captura una imagen de fondo utilizando OpenCV y se renderiza como fondo del entorno 3D, utilizando una instancia de la clase `Background`.

7. **Interacción:** Se verifica si las manos detectadas colisionan con los cubos, y en caso de colisión, se ajustan las posiciones y tamaños de los cubos, lo que permite la interacción entre las manos y los objetos virtuales.

8. **Limpieza y Terminación:** Se liberan los recursos utilizados, como la cámara y las ventanas, al finalizar la ejecución del programa.

Este módulo es crucial para la integración de todas las partes del proyecto, permitiendo la detección de manos, la renderización de objetos 3D y la interacción entre el mundo real y el entorno virtual de realidad aumentada.



## Requisitos de Instalación

Para configurar y ejecutar el proyecto en tu entorno local, sigue estos pasos:

1. Clona este repositorio en tu máquina local:
   ```
   git clone https://github.com/Jack-Christopher/TCG-Proyecto-Final.git
   ```

2. Accede al directorio del proyecto:
   ```
   cd TCG-Proyecto-Final
   ```

3. Instala las dependencias especificadas en el archivo `requirements.txt` utilizando pip:
   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el código del proyecto:
   ```
   python main.py
   ```

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo [LICENSE](https://opensource.org/license/mit/) para obtener más detalles sobre los términos de la licencia.

## Evidencias del Proyecto

En esta sección, proporcionaremos imágenes y videos que muestran el proyecto en acción. Estas evidencias visuales ayudarán a los usuarios a comprender mejor la funcionalidad y la experiencia que ofrece el sistema de realidad aumentada con detección de manos.

**Capturas de Pantalla:**

![Captura de Pantalla 1](/screenshot1.png)

*Interacción con el cubo virtual.*


![Captura de Pantalla 2](/screenshot2.png)

*Colisión de la mano con el cubo virtual.*


## Contribuciones

Si deseas contribuir a este proyecto, estás más que bienvenido/a. Los usuarios pueden contribuir, ya sea mediante la corrección de errores, la implementación de nuevas características o cualquier otra forma de colaboración.
