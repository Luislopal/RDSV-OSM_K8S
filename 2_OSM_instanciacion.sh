# Importamos los paquetes VNF a OSM
chmod 777 /home/upm/Desktop/rdsv-final/pck

echo "Instalamos lo paquetes necesarios: pycurl, prettytable y packaging"

pip install pycurl
pip install prettytable
pip install packaging


cd /home/upm/Desktop/rdsv-final/pck
sudo osm vnfd-create accessknf_vnfd.tar.gz
sudo osm vnfd-create cpeknf_vnfd.tar.gz

echo "Visualizamos los paquetes VNF subidos"
osm vnfd-list

# Importamos los paquetes NS a OSM
sudo osm nsd-create renes_ns.tar.gz
echo "Visualizamos el paquete NS importado"
osm nsd-list

# Instanciación rennes 1
export NSID1=$(osm ns-create --ns_name renes1 --nsd_name renes --vim_account dummy_vim)
echo $NSID1
export NSID1

# Instanciación rennes 2
export NSID2=$(osm ns-create --ns_name renes2 --nsd_name renes --vim_account dummy_vim)
echo $NSID2
export NSID2

# Visualización de las instancias creadas (esperar hasta que esten READY)
echo "Visualizamos las instancias creadas"
watch osm ns-list
