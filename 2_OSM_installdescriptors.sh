# Importamos los paquetes VNF a OSM
chmod 777 /home/upm/Desktop/rdsv-final/pck

#echo "Creación imagen docker de KNF:access"
#cd /home/upm/Desktop/rdsv-final/img/vnf-img
#sudo docker build -t vnf-img .

#echo "Creación imagen docker de KNF:cpe"
#cd /home/upm/Desktop/rdsv-final/img/vnf-rcpe
#sudo docker build -t vnf-vyos .

# Ver las imagenes docker creadas
#docker images


# Registrar repositorio de helm
osm repo-add --type helm-chart --description "Repositorio Helm" repo-rdsv https://Luislopal.github.io/repo-rdsv

# Importamos los paquetes VNF a OSM
cd /home/upm/Desktop/rdsv-final/pck
echo "Instalamos lo paquetes necesarios: pycurl, prettytable y packaging"

#pip3 install pycurl
#pip3 install prettytable
#pip3 install packaging
sudo apt install python3-pycurl
sudo apt install python3-packaging
sudo apt install python3-prettytable

# osm vnfd-update --content /home/upm/Desktop/rdsv-final/pck/accessknf_vnfd.tar.gz accessknf_vnfd
# osm vnfd-update --content /home/upm/Desktop/rdsv-final/pck/cpeknf_vnfd.tar.gz cpeknf_vnfd
osm vnfd-create /home/upm/Desktop/rdsv-final/pck/accessknf_vnfd.tar.gz
osm vnfd-create /home/upm/Desktop/rdsv-final/pck/cpeknf_vnfd.tar.gz

echo "Visualizamos los paquetes VNF subidos"
osm vnfd-list

# osm vnfd-update --content /home/upm/Desktop/rdsv-final/pck/renes_ns.tar.gz renes_ns
# Importamos los paquetes NS a OSM
osm nsd-create /home/upm/Desktop/rdsv-final/pck/renes_ns.tar.gz

echo "Visualizamos el paquete NS importado"
osm nsd-list

# Instanciación rennes 1
#export NSID1=$(osm ns-create --ns_name renes1 --nsd_name renes --vim_account dummy_vim)
#echo $NSID1
#export NSID1

# Instanciación rennes 2
#export NSID2=$(osm ns-create --ns_name renes2 --nsd_name renes --vim_account dummy_vim)
#echo $NSID2
#export NSID2

# Visualización de las instancias creadas (esperar hasta que esten READY)
#echo "Visualizamos las instancias creadas"
#watch osm ns-list
