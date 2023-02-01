<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">
<img  align="right" width="60" style="float: right;" src="http://www.dit.upm.es/figures/logos/ditupm-big.gif">

<br/><br/><br/>

# Práctica final de RDSV
Autores: Luis López Álvarez´y Álvaro de Rojas Maraver

<img width="1395" alt="Infraestructura" src="https://user-images.githubusercontent.com/105986456/216118337-e11710e1-2a81-46bf-8f75-eb3921a15caf.png">

### Pasos para el arranque:
1. Máquina OSM > Ejecutar script 0
```
./0_OSM_configuracion.sh
```
2. Máquina OSM: Ejecutar script 0.5
```
./0.5_permisos.sh
```
3. Máquina K8S: Ejecutar script 0
```
./0_K8S_configuracion_on.sh
```
4. Máquina K8S: Ejecutar script 0.5
```
./0.5_permisos.sh
```
5. Máquina OSM: Ejecutar script 1 
```
./1_OSM_installdescriptors.sh
```
6. Máquina OSM: Ejecutar script 2
```
./2_OSM_instanciacion.sh
```
8. Máquina OSM: Ejecutar script 3 
```
./3_OSM_clusterk8s.sh
```
9. Máquina K8S: Ejecutar script 4
```
./4_K8S_iPerf.sh
```

### Scripts adicionales:

Para apagar ejecutar script 0 en K8S
```
./0_OSM_configuracion_off.sh
```
