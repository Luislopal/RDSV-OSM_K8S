# Acceder al directorio compartido de la práctica desde la maquina virtual
cd /media/sf_Practica4/rdsv-final/repo-rdsv

# Clonar el proyecto en el escritorio de la máquina virtual
sudo cp -r /media/sf_Practica4/rdsv-final /home/upm/Desktop/

# Dar permisos
sudo chmod 777 /home/upm/Desktop/rdsv-final

# Acceder al directorio del escritorio
cd /home/upm/Desktop/rdsv-final

# Configurar la interfaz eth1 en la máquina K8S
ssh upm@192.168.56.11 "sudo ip link set dev eth1 mtu 1400"

# Comprobación
ping -c 3 192.168.56.12
ping -c 3 192.168.56.101

# Arranque escenario home
sudo vnx -f vnx/nfv3_home_lxc_ubuntu64.xml -t

# Arranque escenario server
sudo vnx -f vnx/nfv3_server_lxc_ubuntu64.xml -t

# Permitir acceso a aplicaciones con entorno gráfico
xhost +




# Actualizar los helm package (Todo esto lo dejamos hecho con la imagen subida a nuestro repositorio de docker)
#helm package helm/accesschart
#helm package helm/cpechart
#helm repo index --url https://github.com/Luislopal/repo-rdsv/ .