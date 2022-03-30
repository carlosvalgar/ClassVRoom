# Proyecto ClassVRoom

## Descripción de Proyecto
El proyecto trata de hacer una página web que gestione cursos para que profesores puedan colgar material para sus alumnos y los alumnos puedan subir ejercicios y ver el feedback de su profesor.

## Requisitos
El primer requisito que se necesita para poder utilizar este proyecto es tener instalado Python.

  Linux: <br/>
  
    - $ sudo apt-get update<br/>
    - $ sudo apt-get install python3.6<br/>
    El numero del python determina la version de este que vas a instalar.<br/>
  
  Windows:<br/>
  
    - Nos vamos a la página oficial de Python: https://www.python.org/downloads/<br/>
    - Descargar el archivo .exe de Python<br/>
    - Ejecutar el archivo .exe de Python y seguir las instrucciones<br/>
    
    
    

El segundo requisito será instalar pip para python y el enviorment para poder correr el proyecto.
  
  Linux:<br/>
  
    - $ apt install python3-pip<br/>
    - $ apt-get install python3-venv<br/>
    - $ python3 -m venv my_env_project<br/>
    - $ source my_env_project/bin/activate<br/>
    - Nos deberia aparecer la consola con un a aparencia como esta: (my_env_project) oltjano@ubuntu:~$<br/>


## Instalación y uso del proyecto
Para la instalación y uso del pryecto, una vez cumplidos los requisitos, nos descargarmos el proyecto.<br/>
Seguidamente nos posicionaremos en nuestro enviorment:<br/>
  - $ source my_env_project/bin/activate<br/>
 
 Una vez en nuestro entorno, nos dirigiremos a donde nos lo hemos descargado y en la raiz del proyecto podremos ver un archivo llamado "requirements.txt" y "manage.py".

Necesitaremos instalarnos dentro de nuestro entorno los requisitos que estan dentro de nuestro archivo "requirements.txt".
Para ello, ejecutaremos el siguiente comando:<br/>
  - pip install -r requirements.txt<br/>

Y automaticamente nos instalara los requisitos necesarios para correr el proyecto.

Una vez tenemos los requisitos instalados podemos pasar al utlimo paso.

En la misma carpeta que nos hemos posicionado para instalar los requisitos también nos encontramos el archivo "manage.py" y deberemos utilizar dos comandos para iniciar el proyecto correctamente.

  Linux:<br/>
  
    - $ ./manage.py creategroups
    Este comando nos genera los grupos necesarios automaticamente para el proyecto
    
    - $ ./manage.py runserver
    Este segundo comando nos inicia el proyecto.
   
  Windows:<br/>
  
    - py manage.py creategroups
    Este comando nos genera los grupos necesarios automaticamente para el proyecto
    
    - py manage.py runserver
    Este segundo comando nos inicia el proyecto.

Una vez acabados todos los pasos nos saldra una dirección ip en la consola con una apariencia similar a esta: 
  - http://127.0.0.1:8000/
  
Si copiamos esta url en nuestro navegador, ya podremos trabajar sobre el proyecto.

## Equipo
El equipo ha sido compuesto por 3 alumnos de DAW del instituto Esteve Terradas i Illa.

* Carlos Fernández
  * [Github](https://github.com/bycarlos28) 
  * [Discord: bycarlos28#9418]

* Adrián Gomez
  * [Github](https://github.com/AdrianOrea) 
  * [Github: Adgoor#0880]

* Carlos Valenzuela
  * [Github](https://github.com/carlosvalgar) 
  * [Discord: Carvagia#1404]
