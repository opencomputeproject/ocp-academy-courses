# Revisão de roteiro - ocp101-rev1-1-v3-the-open-rack-deep-dive-v2-1080p

Idioma: Português do Brasil (`pt-BR`)
Voz: Carla (`m151rjrbWXbBqyq56tly`)
Status: roteiro traduzido; síntese e mixagem pendentes

| Segmento | Janela | Roteiro em português |
|---|---:|---|
| seg-01 | 00:00:03.700 - 00:00:09.669 | Cobrimos a história e a comunidade. Agora vamos colocar a mão na massa. |
| seg-02 | 00:00:09.789 - 00:00:17.580 | Este é Open Rack versão 3 ou ORv3. É a base física do moderno data center baseado em IA. |
| seg-03 | 00:00:17.700 - 00:00:24.220 | Para entender por que ele foi construído assim, é preciso compreender a arquitetura da alimentação elétrica. |
| seg-04 | 00:00:24.340 - 00:00:33.220 | Em racks tradicionais de 19 polegadas, cada servidor tinha uma fonte ligada a uma grande régua de distribuição, ou PDU. |
| seg-05 | 00:00:33.340 - 00:00:41.960 | Os primeiros Open Rack eliminaram a confusão de cabos ao trocar as réguas por um barramento central de 12 volts na estrutura. |
| seg-06 | 00:00:42.080 - 00:00:51.560 | Isso bastava para servidores em nuvem de 10 a 15 quilowatts. Mas clusters de IA exigem 100 quilowatts ou mais por rack. |
| seg-07 | 00:00:51.680 - 00:01:03.880 | Se você aumentar tanta potência em 12 volts, a corrente aumentará dramaticamente. Isso vai muito além da simples perda de energia. |
| seg-08 | 00:01:04.000 - 00:01:09.240 | Em 12 volts, a corrente derreteria o cobre e causaria falhas. |
| seg-09 | 00:01:09.360 - 00:01:18.829 | Então o Projeto Rack & Power mudou o padrão. ORv3 usa um barramento CC de 48 volts. |
| seg-10 | 00:01:18.949 - 00:01:31.049 | Ao aumentar a tensão, reduzimos a perda de calor por um fator de 16. Mais energia chega ao silício em vez de queimar na infraestrutura. |
| seg-11 | 00:01:31.169 - 00:01:35.890 | Também reinventamos completamente o fornecimento de energia. |
| seg-12 | 00:01:36.010 - 00:01:46.670 | Em uma configuração tradicional, cada servidor tem sua própria fonte de alimentação redundante, geralmente operando com utilização baixa e ineficiente. |
| seg-13 | 00:01:46.790 - 00:01:57.519 | ORv3 agrupa essa carga de trabalho. Ele substitui dezenas de fontes de alimentação individuais por uma prateleira de energia centralizada carregada com retificadores modulares. |
| seg-14 | 00:01:57.639 - 00:02:06.199 | Ao consolidar a conversão CA para CC para todo o rack, aumentamos a utilização e reduzimos a perda de energia. |
| seg-15 | 00:02:06.319 - 00:02:18.900 | Essa abordagem centralizada simplifica a implantação. O equipamento de TI desliza e se conecta à coluna de alimentação sem fiação manual, e nenhum cabo de alimentação grosso bloqueia o fluxo de ar de exaustão. |
| seg-16 | 00:02:19.020 - 00:02:27.480 | Sem fontes nos servidores, sobra espaço na placa-mãe para mais computação e melhor fluxo de ar. |
| seg-17 | 00:02:27.600 - 00:02:40.700 | Fornecer tanta potência cria mais dois desafios: peso extremo e calor extremo. A estrutura ORv3 é reforçada para suportar o enorme peso dos modernos chassis de GPU. |
| seg-18 | 00:02:40.820 - 00:03:00.730 | Mais importante ainda, a estrutura ORv3 prepara o data center para a próxima geração de calor. Os coletores de refrigeração líquida integram-se diretamente na arquitetura do rack. ORv3 apresenta o padrão Open Compute Universal Quick Disconnect, ou UQD. |
| seg-19 | 00:03:00.850 - 00:03:10.240 | O servidor desliza no rack e conecta a refrigeração líquida com segurança, sem gotejamento. |
| seg-20 | 00:03:10.360 - 00:03:19.720 | Resolvemos o gargalo do fornecimento de energia, mas retirar o calor é outro desafio. Vamos ver como esses racks evitam o superaquecimento. |

Verificar pronúncia de OCP, ORv3, nomes próprios, valores e siglas antes da publicação.
