# Simplified Chinese dubbing script review

Status: **localized-mix-with-library-music-awaiting-listening-review**
Voice: **Lan Chen** (`bZtjnyJAFD0Cp3lfNG5g`)
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Simplified Chinese |
|---|---:|---|---|
| seg-01 | 00:00:03.059–00:00:11.949 | For decades, data centers used a simple principle to keep servers from overheating: push cold air in the front and blow hot air out the back. | 几十年来，数据中心一直用一个简单原则防止服务器过热：冷空气从前部进入，热空气从后部排出。 |
| seg-02 | 00:00:12.069–00:00:18.289 | But the density of modern AI silicon has pushed air cooling to its limit. | 但现代 AI 芯片的功率密度已经把风冷推向极限。 |
| seg-03 | 00:00:18.409–00:00:30.609 | Heat cannot be captured and transported fast enough. Air is a poor conductor of heat, while liquid can capture and transport heat thousands of times more efficiently. | 热量无法被足够快地捕获和输送。空气的导热能力很差，而液体捕获和输送热量的效率可以高出数千倍。 |
| seg-04 | 00:00:30.729–00:00:45.280 | To support AI clusters drawing 100 kilowatts or more, compared with a standard 12-kilowatt rack, the OCP Cooling Environments Project had to shift industry standards. This transition happens in stages. | 标准机架功耗约为 12 千瓦，而 AI 集群可能达到 100 千瓦甚至更高。为支持这种负载，OCP 冷却环境项目必须推动行业标准转型，而且这一转型会分阶段进行。 |
| seg-05 | 00:00:45.400–00:00:54.519 | For facilities not ready to pipe water directly into servers, rear-door heat exchangers, or RDHx, provide the first step. | 对于尚未准备把水直接引入服务器的设施，后门热交换器，也就是 RDHx，是迈出的第一步。 |
| seg-06 | 00:00:54.639–00:01:06.140 | They come in two forms. Passive systems use a liquid-filled coil. Active systems add a fan wall to assist heat transfer, combining air and liquid cooling. | 它分为两种形式：被动系统使用充满液体的盘管；主动系统增加风扇墙来强化传热，将风冷与液冷结合起来。 |
| seg-07 | 00:01:06.260–00:01:21.509 | Open Rack V3's success rests on three hardware standards: its 21-inch width, centralized power bus bar, and liquid-manifold stay-out zone. | Open Rack V3 的成功建立在三项硬件标准之上：21 英寸宽度、集中式供电母线，以及液冷歧管预留区。 |
| seg-08 | 00:01:21.629–00:01:37.869 | Every ORv3 rack reserves standardized physical space specifically for liquid manifolds. In an industry with few liquid standards, this creates a predictable, plug-and-play architecture for fluid delivery. | 每个 ORv3 机架都为液冷歧管预留标准化物理空间。在液冷标准仍然有限的行业中，这形成了可预测、即插即用的流体输送架构。 |
| seg-09 | 00:01:37.989–00:01:51.100 | This standardized manifold space enables direct liquid cooling, or DLC. Metal cold plates with microchannels sit directly on CPUs and GPUs. | 这一标准化歧管空间支持直接液冷，也就是 DLC。带有微通道的金属冷板直接安装在 CPU 和 GPU 上。 |
| seg-10 | 00:01:51.220–00:02:06.369 | Using highly reliable, zero-leak fluid connectors, the rack-mounted manifold pumps a water-and-glycol mixture directly to the silicon. It captures up to 80 percent of the heat where it is generated. | 通过高可靠、零泄漏的流体连接器，机架式歧管把水和乙二醇混合液直接送到芯片，可在热量产生处捕获最多 80% 的热量。 |
| seg-11 | 00:02:06.489–00:02:18.609 | Liquid cooling maximizes the potential of the standard ORv3 rack. But the ultimate solution requires a completely different physical architecture: immersion cooling. | 液冷最大限度地释放标准 ORv3 机架的潜力，但终极方案需要完全不同的物理架构：浸没式冷却。 |
| seg-12 | 00:02:18.729–00:02:39.219 | Instead of sliding servers into a vertical rack, complete servers are submerged in a horizontal tank of nonconductive dielectric fluid. Because the fluid touches every component—CPU, GPU, memory, and networking—no blind-mate manifolds or hoses are required. | 服务器不再滑入垂直机架，而是整机浸入装有不导电介电流体的水平槽中。流体会接触 CPU、GPU、内存和网络等每个组件，因此不需要盲插歧管或软管。 |
| seg-13 | 00:02:39.339–00:02:44.799 | In single-phase immersion, the fluid absorbs the heat. | 在单相浸没式冷却中，流体吸收热量。 |
| seg-14 | 00:02:44.919–00:02:56.480 | In two-phase immersion, extreme heat boils the fluid. The phase change lets the vapor condense and cool the hardware at unmatched scale. | 在两相浸没式冷却中，极高热量使流体沸腾。相变产生的蒸汽随后冷凝，以前所未有的规模为硬件降温。 |
| seg-15 | 00:02:56.600–00:03:05.350 | Whether using cold plates or a full immersion tank, liquid cooling is no longer a science experiment. It is a survival requirement. | 无论采用冷板还是完整浸没槽，液冷都已不再是科学实验，而是维持运行的必要条件。 |
| seg-16 | 00:03:05.470–00:03:11.310 | The hardware is built and the specifications are published. The only thing left is deployment. | 硬件已经建成，规范也已发布。最后一步就是部署。 |

Technical values, years, voltages, OCP names, and the confirmed tenet **Scale** are preserved from the reviewed English source.

## Audio mix

Background track: `viacheslavstarostin-background-backsound-music-educational-364858.mp3`. The original source audio is excluded. The localized voice-only master remains in the foreground while normalized music ducks smoothly during speech, restores between phrases, and fades over the final four seconds. Listening review is required.
