# Simplified Chinese dubbing script review

Status: **localized-mix-with-library-music-awaiting-listening-review**
Voice: **Lan Chen** (`bZtjnyJAFD0Cp3lfNG5g`)
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Simplified Chinese |
|---|---:|---|---|
| seg-01 | 00:00:03.700–00:00:09.669 | We have covered the history and the community. Now let us get hands-on. | 我们已经介绍了历史和社区。现在，让我们进入硬件实践。 |
| seg-02 | 00:00:09.789–00:00:17.580 | This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center. | 这就是 Open Rack 第 3 版，也就是 ORv3。它是现代 AI 数据中心的物理基础。 |
| seg-03 | 00:00:17.700–00:00:24.220 | To understand why it is built this way, you must understand the architecture of power. | 要理解它为何采用这种设计，首先必须理解供电架构。 |
| seg-04 | 00:00:24.340–00:00:33.220 | In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU. | 在传统的 19 英寸机架中，每台服务器都有独立电源，并接入称为 PDU 的大型配电单元。 |
| seg-05 | 00:00:33.340–00:00:41.960 | Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame. | 早期 Open Rack 通过用机架内置的集中式 12V 母线取代配电单元，解决了线缆杂乱问题。 |
| seg-06 | 00:00:42.080–00:00:51.560 | That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack. | 这种方案足以支持功耗为 10 到 15 千瓦的标准云服务器，但今天的 AI 集群每个机架需要 100 千瓦甚至更高功率。 |
| seg-07 | 00:00:51.680–00:01:03.880 | If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss. | 如果在 12V 电压下传输如此高的功率，电流会急剧上升。问题远不只是一般的功率损耗。 |
| seg-08 | 00:01:04.000–00:01:09.240 | Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure. | 12V 母线承受这种大电流会熔化、打火，甚至使系统彻底失效。 |
| seg-09 | 00:01:09.360–00:01:18.829 | So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar. | 因此，机架与电源项目改变了标准。ORv3 使用 48V 直流母线。 |
| seg-10 | 00:01:18.949–00:01:31.049 | By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure. | 提高电压后，热损耗可降至原来的十六分之一。更多电力能够送达芯片，而不是消耗在基础设施中。 |
| seg-11 | 00:01:31.169–00:01:35.890 | We also completely reimagined power delivery. | 我们还彻底重新设计了供电方式。 |
| seg-12 | 00:01:36.010–00:01:46.670 | In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate. | 传统架构中，每台服务器都有冗余电源，但通常工作在利用率低、效率差的区间。 |
| seg-13 | 00:01:46.790–00:01:57.519 | ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers. | ORv3 将这些供电负载集中起来，用一个装有模块化整流器的集中式电源架，取代数十个独立电源。 |
| seg-14 | 00:01:57.639–00:02:06.199 | By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss. | 通过集中完成整个机架的交流到直流转换，我们提高了利用率并降低了功率损耗。 |
| seg-15 | 00:02:06.319–00:02:18.900 | This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow. | 集中式供电也简化了部署。IT 设备滑入机架即可连接供电主干，无需手工布线，也不会有粗电源线阻挡排风气流。 |
| seg-16 | 00:02:19.020–00:02:27.480 | Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow. | 取消服务器内部电源后，主板空间得到释放，可以容纳更高密度的计算，并改善系统气流。 |
| seg-17 | 00:02:27.600–00:02:40.700 | Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis. | 传输如此高的功率还会带来两个挑战：极大的重量和极高的热量。ORv3 机架框架经过加固，可以承受现代 GPU 机箱的巨大重量。 |
| seg-18 | 00:02:40.820–00:03:00.730 | More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD. | 更重要的是，ORv3 为下一代高热负载做好了准备。液冷歧管直接集成到机架架构中，ORv3 还引入了 Open Compute Universal Quick Disconnect 标准，也就是 UQD。 |
| seg-19 | 00:03:00.850–00:03:10.240 | Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips. | 服务器设备直接滑入机架，就能安全、顺畅且无滴漏地连接液冷回路。 |
| seg-20 | 00:03:10.360–00:03:19.720 | We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down. | 我们解决了供电瓶颈，但如何把热量带走是另一项挑战。接下来看看这些机架如何避免过热。 |

Technical values, years, voltages, OCP names, and the confirmed tenet **Scale** are preserved from the reviewed English source.

## Audio mix

Background track: `viacheslavstarostin-educational-learning-study-music-473828.mp3`. The original source audio is excluded. The localized voice-only master remains in the foreground while normalized music ducks smoothly during speech, restores between phrases, and fades over the final four seconds. Listening review is required.
