# Comprobar que existe el cluster
osm k8scluster-list

# Identificador usado para gestionar el cluster
KID=$(osm k8scluster-list | awk 'FNR == 4 {print $4}')
echo $KID

# Mostrar información sober el namespace y guardar este valor
export OSMNS=$(osm k8scluster-show --literal $KID | grep -A1 projects | awk 'FNR == 2 {print $2}')

# Mostrar el valor anterior
echo $OSMNS

# Comprobar que el cliente kubectl está configurado para acceder al cluster
kubectl get namespaces
