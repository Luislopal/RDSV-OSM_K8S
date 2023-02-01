# Detener los escenarios arrancados en K8S
sudo vnx -f vnx/nfv3_home_lxc_ubuntu64.xml -P
sudo vnx -f vnx/nfv3_server_lxc_ubuntu64.xml -P

# Arrancar la imagen con modo directo
vnx --modify-rootfs /usr/share/vnx/filesystems/vnx_rootfs_lxc_ubuntu64-20.04-v025-vnxlab/

# Paramos el contenedor
halt -p

#Arrancar de nuevo (iperf activo)
sudo vnx -f vnx/nfv3_home_lxc_ubuntu64.xml -t
sudo vnx -f vnx/nfv3_server_lxc_ubuntu64.xml -t
