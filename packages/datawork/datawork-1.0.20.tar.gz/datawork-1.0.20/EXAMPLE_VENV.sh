#!/bin/bash                                                                                                                                                                                                     
# This hook is sourced after this virtualenv is activated.                                                                                                                                                      
export COLLECTOR_DBUSER='collector'
export COLLECTOR_DBPASS='XdataX'
export COLLECTOR_DBNAME='collector'
export COLLECTOR_DBHOST='localhost'
export COLLECTOR_PORT=2345

# only numbers                                                                                                                                                                                                  

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
#export MQ_PASS="geognss_prod"                                                                                                                                                                                  
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
export MQ_PASS="geognss_prod"
# Es el la password asociada                                                                                                                                                                                    
export MQ_VHOST="gpsdata"
# Es el nombre del host virtual de la cola                                                                                                                                                                      
export MQ_CODE="geo_enu_data"
export MQ_QUEUE_NAME="gpsstream"













