# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
#
# Integrantes de la pareja:
#
# LUIS ALBERTO LÓPEZ ÁLVAREZ
# ÁLVARO DE ROJAS MARAVER

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet.ether_types import ETH_TYPE_8021Q
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, vlan
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

portToVLANDict = {1: 2000, 2:500, 3:500, 4:1000, 5:2000, 6:1000}

class VLANSwitch13(app_manager.RyuApp):

    # Especificamos la versión OpenFlow v1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Se declara un diccionario que expresa la asociación entre direcciones MAC y puertos del conmutador.
    def __init__(self, *args, **kwargs):
        super(VLANSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    # Especifica la clase de evento que admite el mensaje recibido y el estado del conmutador OpenFlow para el argumento.
    # La clase CONFIG_DISPATCHER indica que el controlador está esperando recibir el mensaje de switch_features.
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)

    # Se añade la entrada a la tabla de flujos.
    def switch_features_handler(self, ev):
        # En ev.msg se almacena la instancia de la clase de mensaje OpenFlow correspondiente al evento.
        # En msg.datapath la instancia de la clase correspondiente al conmutador OpenFlow que emitió el mensaje.
        # La clase dataPath realiza el procesamiento de comunicación real con el conmutador OpenFlow y la emisión del evento correspondiente al mensaje recibido.
        # datpath referencia al switch que envió el mensaje al controlador.
        # ofproto es el módulo que define constantes de la versión OpenFlow en uso.
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        # Indica el uso del módulo ofproto_parser (para codificar y decodificar mensajes OpenFlow).
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        # Especificamos NO BUFFER al max_len de la acción de salida debido a
        # error de OVS. En este momento, si especificamos un número menor, por ejemplo
        # 128, OVS enviará el Packet-In con un buffer_id inválido y
        # datos del paquete truncados. En ese caso, no podemos enviar paquetes
        # correctamente.  El error ha sido corregido en OVS v2.1.0.
        # OSPFMatch genera una coincidencia vacía para que coincida con todos los paquetes.
        match = parser.OFPMatch()
        #  Se maneja como un evento para obtener el tiempo para agregar la entrada de flujo de la tabla.
        # OSPFActionOutput es una clase empleada para transferir paquetes al puerto del controlador (OFPCML_NO_BUFFER)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        # La entrada de flujo de la tabla que falta tiene la prioridad (0) más baja y coincide con todos los paquetes.
        # El paquete se emite si no coincide con ninguna entrada de flujo normal.
        # Add_flow se ejecuta para enviar el mensaje flow mode.
        # Añade el flujo en la tabla del conmutador.
        self.add_flow(datapath, 0, match, actions)
    
    # Método para agregar entradas de flujo (previo al procesamiento del controlador de paquetes).
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Construye y envía el mensaje flow_mod
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        # Añade una entrada a la tabla de fujo emitiendo el mensaje flow_mod 
        # datapath: Especifica la instancia de la clase Datapath correspondiente al switch OpenFlow.
        # buffer_id: Especifica el ID del búfer de los paquetes almacenados en el OpenFlow. Si no se almacenan en el búfer, se especifica OFP_NO_BUFFER.
        # in_port: Especifica el puerto que recibió los paquetes. Si no es el paquete recibido, se especifica OFPP_CONTROLLER.
        # actions: Especifica la lista de acciones.
        # data: Especifica los datos binarios de los paquetes. Se utiliza cuando se especifica OFP_NO_BUFFER para buffer_id. Cuando se utiliza el búfer del conmutador OpenFlow, se omite.
        # priority: Especifica el valor de prioridad, a mayor valor más prioridad.
        # match especifica coincidencia, instructions especifica una lista de instrucciones.
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
    # Crea el controlador del controlador de eventos de Packet-in para aceptar paquetes recibidos con destino desconocido.
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # Se obtiene el número de puerto recibido del mensaje packet_in
        in_port = msg.match['in_port']
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # aprende una dirección mac para evitar el FLOOD la próxima vez.
        # Con el fin de admitir la conexión con varios conmutadores OpenFlow la tabla de direcciones MAC está diseñada para ser gestionada para cada conmutador de OpenFlow.
        # El dpid se utiliza para identificar los conmutadores OpenFlow.
        self.mac_to_port[dpid][src] = in_port

        # El número de puerto de salida correspondiente se utiliza cuando la dirección MAC de destino existe en la tabla de direcciones MAC. 
        # Si no se encuentra, se genera la instancia de la clase de acción OUTPUT que especifica la inundación (OFPP_FLOOD) para el puerto de salida.
        # Si la dirección de destino está aprendida decidir en qué puerto generar el paquete, de lo contrario FLOOD.
        # Si se encuentra la MAC de destino se añade una entrada a la tabla de flujo del conmutador OpenFlow.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        
        actions = [parser.OFPActionOutput(out_port)]
        if out_port != ofproto.OFPP_FLOOD:
            if portToVLANDict[in_port] != portToVLANDict[out_port]:
                actions = []

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    
