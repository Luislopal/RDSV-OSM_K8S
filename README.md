# rdsv-final
Práctica final de RDSV

Pasos para el arranque:

1. Máquina OSM > Ejecutar script 0: ./0_OSM_configuracion.sh
2. Máquina K8S > Ejecutar script 0: ./0_K8S_configuracion_on.sh

Para apagar ejecutar script 0 en K8S: ./0_OSM_configuracion_off.sh
Para dar permisos ejecutar script 0.5 en K8S y OSM: ./0.5_permisos.sh

3. Máquina OSM > Ejecutar script 1: ./1_OSM_installdescriptors.sh
4. Máquina OSM > Ejecutar script 2: ./2_OSM_instanciacion.sh
5. Máquina OSM > Ejecutar script 3: ./3_OSM_clusterk8s.sh

