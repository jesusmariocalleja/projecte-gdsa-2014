# projecte-gdsa-2014

###### Xavier Borràs
###### Jesús Mario Calleja
###### Jaume Casafont
###### Eduard Galí
###### Guillermo García

INSTRUCTIONS

First of all you need two csv files with metadata. One with the images that you want to train, and the groundtruth file.

1r --> Copy the images that you want to classify into "images" folder. Open read.py. 
It creates a csv file with the images.

2n --> Open descriptor.py and we have to load the next files: 

- groundtruth.csv
- train.csv (list of train images)
- test.csv (list of test images, generated on the read.py)

The Descriptor will create two files that we will have to use on the Classificador.py.

3r --> Open classificador.py and we have to load two files creates by the descriptor.
The classifier will generate a .txt with classified images.

4rt --> Open avaluador.py and we have to load classified.txt


INSTRUCCIONS

Primer de tot necessites dos arxius csvs amb les metadades. Un amb les imatges que vols entrenar, i l'arxiu groundtruth.

1r --> Copiar les imatges que es volen classificar a la carpeta "images". Obrir l'arxiu read.py 
que crea un csv de les imatges.

2n --> Obrir l'arxiu descriptor.py i li hem de passar els següents arxius: 

- groundtruth.csv
- train.csv (llista imatges d'entrenament)
- test.csv (llista imatges d'imatges de test)

El Descriptor crearà dos arxius.

3r --> Obrim l'arxiu classificador.py i pasar els dos arxius creats al descriptor.
El Classificador generarà un .txt amb totes les imatges classificades.

4rt --> Obrim l'arxiu avaluador.py i li passem el classified.txt.


INSTRUCCIONES

Antes que nada necesitas dos archivos csvs con los metadatos. Uno con las imágenes que quieres entrenar, y el archivo groundtruth.

1º -> Copiar las imagenes que se quieren clasificar a la carpeta "images". Abrir el archivo read.py 
que crea un csv de las imágenes.

2º -> Abrir el archivo descriptor.py y le tenemos que pasar los siguientes archivos:

- groundtruth.csv
- Train.csv (lista imágenes de entrenamiento)
- Test.csv (lista imágenes de imágenes de test)

El Descriptor creará dos archivos.

3º -> Abrir el archivo classificador.py y pasar los dos archivos creados en el descriptor.
El Clasificador generará un .txt con todas las imágenes clasificadas.

4º -> Abrir el arxivo avaluador.py y pasar el classified.txt.
