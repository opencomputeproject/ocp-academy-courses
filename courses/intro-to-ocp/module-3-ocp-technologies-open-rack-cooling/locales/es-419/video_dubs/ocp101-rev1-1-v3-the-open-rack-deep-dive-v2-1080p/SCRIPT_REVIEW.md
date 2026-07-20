# Revisión del guion - ocp101-rev1-1-v3-the-open-rack-deep-dive-v2-1080p

Idioma: Español (Latinoamérica)
Voz: Ninoska (`zl1Ut8dvwcVSuQSB9XkG`)

Revise especialmente la pronunciación de nombres y acrónimos oficiales de OCP.

## seg-01 (00:00:03.700 - 00:00:09.669)

**Fuente:** We have covered the history and the community. Now let us get hands-on.

**Español:** Ya analizamos la historia y la comunidad. Ahora pasemos a la práctica.

## seg-02 (00:00:09.789 - 00:00:17.580)

**Fuente:** This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center.

**Español:** Este es Open Rack versión 3, ORv3: la base física del centro de datos moderno para IA.

## seg-03 (00:00:17.700 - 00:00:24.220)

**Fuente:** To understand why it is built this way, you must understand the architecture of power.

**Español:** Para comprender su diseño, primero debe entender la arquitectura eléctrica.

## seg-04 (00:00:24.340 - 00:00:33.220)

**Fuente:** In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU.

**Español:** En un rack tradicional de 19 pulgadas, cada servidor tenía su propia fuente, conectada a una gran PDU.

## seg-05 (00:00:33.340 - 00:00:41.960)

**Fuente:** Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame.

**Español:** Los primeros diseños de Open Rack resolvieron este enredo de cables al reemplazar las regletas con una barra colectora central de 12 voltios integrada al marco.

## seg-06 (00:00:42.080 - 00:00:51.560)

**Fuente:** That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack.

**Español:** Eso bastaba para servidores de nube de 10 a 15 kilovatios. Hoy, los clústeres de IA exigen 100 kilovatios o más por rack.

## seg-07 (00:00:51.680 - 00:01:03.880)

**Fuente:** If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss.

**Español:** Si se entrega tanta potencia a 12 voltios, la corriente aumenta drásticamente. Las consecuencias van mucho más allá de una simple pérdida de energía.

## seg-08 (00:01:04.000 - 00:01:09.240)

**Fuente:** Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure.

**Español:** A 12 voltios, esa corriente fundiría cobre, produciría arcos y derribaría el sistema.

## seg-09 (00:01:09.360 - 00:01:18.829)

**Fuente:** So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar.

**Español:** Por eso, el proyecto Rack & Power cambió el estándar. ORv3 utiliza una barra colectora de corriente continua de 48 voltios.

## seg-10 (00:01:18.949 - 00:01:31.049)

**Fuente:** By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure.

**Español:** Al elevar el voltaje, reducimos la pérdida térmica por un factor de 16. Más energía llega al silicio, en vez de disiparse en la infraestructura.

## seg-11 (00:01:31.169 - 00:01:35.890)

**Fuente:** We also completely reimagined power delivery.

**Español:** También reinventamos por completo la distribución de energía.

## seg-12 (00:01:36.010 - 00:01:46.670)

**Fuente:** In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate.

**Español:** En una configuración tradicional, cada servidor tiene su propia fuente de alimentación redundante, que suele operar con una utilización baja e ineficiente.

## seg-13 (00:01:46.790 - 00:01:57.519)

**Fuente:** ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers.

**Español:** ORv3 agrupa esa carga. Reemplaza decenas de fuentes individuales con una bandeja de energía central equipada con rectificadores modulares.

## seg-14 (00:01:57.639 - 00:02:06.199)

**Fuente:** By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss.

**Español:** Al centralizar la conversión de corriente alterna a continua para todo el rack, aumentamos la utilización y reducimos la pérdida de energía.

## seg-15 (00:02:06.319 - 00:02:18.900)

**Fuente:** This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow.

**Español:** Este enfoque central simplifica la implementación. El equipo de TI se desliza y conecta a la columna eléctrica sin cableado manual, y ningún cable grueso bloquea el flujo de aire de salida.

## seg-16 (00:02:19.020 - 00:02:27.480)

**Fuente:** Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow.

**Español:** Eliminar las fuentes de alimentación de los servidores libera espacio en la placa base, lo que permite mayor densidad de cómputo y un mejor flujo de aire.

## seg-17 (00:02:27.600 - 00:02:40.700)

**Fuente:** Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis.

**Español:** Entregar tanta potencia crea otros dos desafíos: peso extremo y calor extremo. El marco de ORv3 está reforzado para soportar el enorme peso de los chasis de GPU modernos.

## seg-18 (00:02:40.820 - 00:03:00.730)

**Fuente:** More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD.

**Español:** Más importante aún, ORv3 prepara el centro de datos para el calor de próxima generación. Los colectores de refrigeración líquida se integran directamente al rack. ORv3 incorpora el estándar Open Compute Universal Quick Disconnect, o UQD.

## seg-19 (00:03:00.850 - 00:03:10.240)

**Fuente:** Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips.

**Español:** El equipo de servidores se desliza directamente en el rack y conecta sus circuitos de refrigeración líquida de forma segura, fluida y sin goteos.

## seg-20 (00:03:10.360 - 00:03:19.720)

**Fuente:** We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down.

**Español:** Resolvimos el cuello de botella de la distribución eléctrica, pero extraer el calor es otro desafío. Veamos cómo estos racks evitan fundirse.
