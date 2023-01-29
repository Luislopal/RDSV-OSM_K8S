# Acceder al directorio de la práctica rdsv-final
cd /media/sf_Practica4/rdsv-final

# Clonar el proyecto en el escritorio de la máquina virtual
sudo cp -r /media/sf_Practica4/rdsv-final /home/upm/Desktop/

# Dar permisos
sudo chmod 777 /home/upm/Desktop/rdsv-final

# Acceder al directorio del escritorio
cd /home/upm/Desktop/rdsv-final

# Configurar la interfaz eth1 en la máquina OSM
ssh upm@192.168.56.12 "sudo ip link set dev eth1 mtu 1400"

#Comprobación
ping -c 3 192.168.56.11
ping -c 3 192.168.56.101

# Permitir acceso a aplicaciones con entorno gráfico (Igual da fallo al hacerlo antes)
xhost +

