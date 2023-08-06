Datawork
==========

Este módulo es una implementación específica de *Tasktools.Scheduler* para
procesar los datos recibidos desde estaciones GNSS y almacenados en una database
*Retrhinkdb*.

El propósito de *Datawork* es realizar el trabajo pesado con la información
nueva que se ha recibido. En primer caso será obtener las diferencias de
posición según *ECEF*. Luego será direccionar la información calculada a
diversos canales:

- geojson
- earlybird
- status

## Instalación

Para instalar *Datawork* será necesario tener instalado *Python v3.7* o
superior. Crear un ambiente virtual.

```bash
pip install datawork
```

O bien, clonando del repositorio e instalando:


```bash
git clone https://gitlab.com/pineiden/datawork.git
cd datawork
python setup.py install
```
## ¿Cómo opera?

Al iniciar recupera la lista de estaciones y su metadata mediante una conexíón
socket al *Collector*.

El TaskAssignator toma la lista y activa las tareas que están a la espera en el
*Scheduler*, al activarse comienza a operar un loop con tres elementos
principales:

- Objecto rethinkdb para fuente
- Objeto rethinkdb para destino ENU
- Procesador de información

También, de forma paralela, permanecen en operación:

- Entrega a distintas colas RabbitMQ de la información procesada
- Cliente socket conectado a Collector
- Servidor socket a la escucha de conexiones.

En operación el sistema rescata desde el momento anterior hasta el presente la
lista de nuevos elementos en la tabla correspondiente a la estación. Si se
obtiene una lista no vacía se procede a transformar y envíar a los diferentes destinos.

## Comando 'Datawork'

Se dispone de un comando *Datawork* para activar el proceso, para casos
particulares revisar la ayuda.

```bash
datawork --help
```

## ¿Qué poner como parámetros de ambiente virtual?


```bash
#!/bin/bash                                                                                   
# This hook is sourced after this virtualenv is activated.                                                                                                                                                      
export COLLECTOR_DBUSER='dbuser'
export COLLECTOR_DBPASS='epdasdasd'
export COLLECTOR_DBNAME='dbname'
export COLLECTOR_DBHOST='localhost'
export COLLECTOR_PORT=2345

# SETTINGS Collector LOCAL                                                                                                                                                                                      
export COLLECTOR_EST_X_PROC=3
export COLLECTOR_TSLEEP=1
export COLLECTOR_WORKERS=6
export GSOF_TIMEOUT=8
export CLL_STATUS="ALL"
export CLL_GROUP='["QSCO"]'
#Datawork                                                                                                         
export DATAWORK_EST_X_PROC=8
export DATAWORK_TSLEEP=2
export DATAWORK_WORKERS=12


export GSOF_TIMEOUT=2
export DW_STATUS="ALL" # OPTIONS: "GROUP" "ALL"                                                                                                                                                                 
export DW_GROUP='["QSCO"]'
export DW_DIR="/home/datawork/datawork_system/datawork/datawork"

export GUI_WORKERS=10
export GUI_STATIONS_BY_WORKER=12
export SELECT_GROUP=4

alias dbus_coords="dbus-monitor type=signal interface=\"csn.coord.interface\""

#export COLLECTOR_SOCKET_IP="10.54.217.15"                                                                                                                                                                      
export COLLECTOR_SOCKET_IP='atlas.csn.uchile.cl'
export COLLECTOR_SOCKET_PORT=6677
#export RDB_SOURCE='atlas.csn.uchile.cl'                                                                                                                                                                        
export RDB_SOURCE='atlas.csn.uchile.cl'
export RDB_ENU='10.54.218.66'
#export DATAWORK_SOCKET_IP="10.54.218.66"                                                                                                                                                                       
export DATAWORK_SOCKET_IP="localhost"
export DATAWORK_SOCKET_PORT=6666


export MQ_HOST="10.54.217.95"
# Es la dirección ip on url del host dónde se ubica el servicio                                                                                                                                                 
#export MQ_NAME="enugeojson_prod"                                                                                                                                                                               
# Es el nombre de usuario que accede a la cola                                                                                                                                                                  
#export MQ_PASS="pwd"                                                                                                                                                                                  
# Es el la password asociada                                                                                                                                                                                    
#export MQ_VHOST="gpsdata"                                                                                                                                                                                      
# Es el nombre del host virtual de la cola                                                                                                                                                                      
#export MQ_CODE="geo_enu_data"                                                                                                                                                                                  
# Es el nombre en código de la cola                                                                                                                                                                             
#export MQ_QUEUE_NAME="gpsstream"                                                                                                                                                                              


echo "Loading Rabbit MQ data"

export MQ_HOST="10.54.217.95"
# Es la dirección ip on url del host dónde se ubica el servicio                                                                                                                                                 
export MQ_NAME="enugeojson_prod"
# Es el nombre de usuario que accede a la cola                                                                                                                                                                  
export MQ_PASS="pwd"
# Es el la password asociada                                                                                                                                                                                    
export MQ_VHOST="gpsdata"
# Es el nombre del host virtual de la cola                                                                                                                                                                      
export MQ_CODE="geo_enu"
export MQ_QUEUE_NAME="gpss"

```
