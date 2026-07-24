# Traditional Chinese dubbing script review

Status: **localized-mix-ready-for-course-build**
Voice: **Tiffy** (`1AKkSX7KMPHIWuz76m0n`)
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Traditional Chinese |
|---|---:|---|---|
| seg-01 | 00:00:03.700–00:00:09.669 | We have covered the history and the community. Now let us get hands-on. | 我們已經介紹了歷史和社群。現在，讓我們進入硬體實踐。 |
| seg-02 | 00:00:09.789–00:00:17.580 | This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center. | 這就是 Open Rack 第 3 版，也就是 ORv3。它是現代 AI 資料中心的物理基礎。 |
| seg-03 | 00:00:17.700–00:00:24.220 | To understand why it is built this way, you must understand the architecture of power. | 要理解它為何採用這種設計，首先必須理解供電架構。 |
| seg-04 | 00:00:24.340–00:00:33.220 | In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU. | 在傳統的 19 英寸機架中，每臺伺服器都有獨立電源，並接入稱為 PDU 的大型配電單元。 |
| seg-05 | 00:00:33.340–00:00:41.960 | Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame. | 早期 Open Rack 透過用機架內建的集中式 12V 匯流排取代配電單元，解決了線纜雜亂問題。 |
| seg-06 | 00:00:42.080–00:00:51.560 | That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack. | 這種方案足以支援功耗為 10 到 15 千瓦的標準雲伺服器，但今天的 AI 叢集每個機架需要 100 千瓦甚至更高功率。 |
| seg-07 | 00:00:51.680–00:01:03.880 | If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss. | 如果在 12V 電壓下傳輸如此高的功率，電流會急劇上升。問題遠不只是一般的功率損耗。 |
| seg-08 | 00:01:04.000–00:01:09.240 | Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure. | 12V 匯流排承受如此大電流，可能熔化、打火，甚至使系統失效。 |
| seg-09 | 00:01:09.360–00:01:18.829 | So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar. | 因此，機架與電源專案改變了標準。ORv3 使用 48V 直流匯流排。 |
| seg-10 | 00:01:18.949–00:01:31.049 | By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure. | 提高電壓後，熱損耗可降至原來的十六分之一。更多電力能夠送達晶片，而不是消耗在基礎設施中。 |
| seg-11 | 00:01:31.169–00:01:35.890 | We also completely reimagined power delivery. | 我們還徹底重新設計了供電方式。 |
| seg-12 | 00:01:36.010–00:01:46.670 | In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate. | 傳統架構中，每臺伺服器都有冗餘電源，但通常工作在利用率低、效率差的區間。 |
| seg-13 | 00:01:46.790–00:01:57.519 | ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers. | ORv3 將這些供電負載集中起來，用一個裝有模組化整流器的集中式電源架，取代數十個獨立電源。 |
| seg-14 | 00:01:57.639–00:02:06.199 | By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss. | 透過集中完成整個機架的交流到直流轉換，我們提高了利用率並降低了功率損耗。 |
| seg-15 | 00:02:06.319–00:02:18.900 | This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow. | 集中式供電也簡化了部署。IT 裝置滑入機架即可連線供電主幹，無需手工佈線，也不會有粗電源線阻擋排風氣流。 |
| seg-16 | 00:02:19.020–00:02:27.480 | Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow. | 取消伺服器內部電源後，主機板空間得到釋放，可以容納更高密度的計算，並改善系統氣流。 |
| seg-17 | 00:02:27.600–00:02:40.700 | Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis. | 傳輸如此高的功率還會帶來兩個挑戰：極大的重量和極高的熱量。ORv3 機架框架經過加固，可以承受現代 GPU 機箱的巨大重量。 |
| seg-18 | 00:02:40.820–00:03:00.730 | More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD. | 更重要的是，ORv3 為下一代高熱負載做好了準備。液冷歧管直接整合到機架架構中，ORv3 還引入了 Open Compute Universal Quick Disconnect 標準，也就是 UQD。 |
| seg-19 | 00:03:00.850–00:03:10.240 | Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips. | 伺服器裝置直接滑入機架，就能安全、順暢且無滴漏地連線液冷迴路。 |
| seg-20 | 00:03:10.360–00:03:19.720 | We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down. | 我們解決了供電瓶頸，但如何把熱量帶走是另一項挑戰。接下來看看這些機架如何避免過熱。 |

Technical values, years, voltages, OCP names, and confirmed source terminology are preserved from the reviewed English source.

## Audio mix

The source audio stream is not mapped. The aligned Traditional Chinese voice-only master is mixed over viacheslavstarostin-educational-learning-study-music-473828.mp3, normalized to -27 LUFS. Music fades in, sidechain-ducks beneath actual narration, restores between phrases, and fades over the video's final four seconds.

The original source-language audio is excluded. The localized video, caption track, and voice timing were validated before publication. Maximum applied tempo adjustment: **1.1000×**.
