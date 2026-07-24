# Traditional Chinese dubbing script review

Status: **localized-mix-ready-for-course-build**
Voice: **Tiffy** (`1AKkSX7KMPHIWuz76m0n`)
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Traditional Chinese |
|---|---:|---|---|
| seg-01 | 00:00:03.059–00:00:11.949 | For decades, data centers used a simple principle to keep servers from overheating: push cold air in the front and blow hot air out the back. | 幾十年來，資料中心一直用一個簡單原則防止伺服器過熱：冷空氣從前部進入，熱空氣從後部排出。 |
| seg-02 | 00:00:12.069–00:00:18.289 | But the density of modern AI silicon has pushed air cooling to its limit. | 但現代 AI 晶片的功率密度已經把風冷推向極限。 |
| seg-03 | 00:00:18.409–00:00:30.609 | Heat cannot be captured and transported fast enough. Air is a poor conductor of heat, while liquid can capture and transport heat thousands of times more efficiently. | 熱量無法被足夠快地捕獲和輸送。空氣的導熱能力很差，而液體捕獲和輸送熱量的效率可以高出數千倍。 |
| seg-04 | 00:00:30.729–00:00:45.280 | To support AI clusters drawing 100 kilowatts or more, compared with a standard 12-kilowatt rack, the OCP Cooling Environments Project had to shift industry standards. This transition happens in stages. | 標準機架功耗約為 12 千瓦，而 AI 叢集可能達到 100 千瓦甚至更高。為支援這種負載，OCP 冷卻環境專案必須推動行業標準轉型，而且這一轉型會分階段進行。 |
| seg-05 | 00:00:45.400–00:00:54.519 | For facilities not ready to pipe water directly into servers, rear-door heat exchangers, or RDHx, provide the first step. | 對於尚未準備把水直接引入伺服器的設施，後門熱交換器，也就是 RDHx，是邁出的第一步。 |
| seg-06 | 00:00:54.639–00:01:06.140 | They come in two forms. Passive systems use a liquid-filled coil. Active systems add a fan wall to assist heat transfer, combining air and liquid cooling. | 它分為兩種形式：被動系統使用充滿液體的盤管；主動系統增加風扇牆來強化傳熱，將風冷與液冷結合起來。 |
| seg-07 | 00:01:06.260–00:01:21.509 | Open Rack V3's success rests on three hardware standards: its 21-inch width, centralized power bus bar, and liquid-manifold stay-out zone. | Open Rack V3 的成功建立在三項硬體標準之上：21 英寸寬度、集中式供電匯流排，以及液冷歧管預留區。 |
| seg-08 | 00:01:21.629–00:01:37.869 | Every ORv3 rack reserves standardized physical space specifically for liquid manifolds. In an industry with few liquid standards, this creates a predictable, plug-and-play architecture for fluid delivery. | 每個 ORv3 機架都為液冷歧管預留標準化物理空間。在液冷標準仍然有限的行業中，這形成了可預測、即插即用的流體輸送架構。 |
| seg-09 | 00:01:37.989–00:01:51.100 | This standardized manifold space enables direct liquid cooling, or DLC. Metal cold plates with microchannels sit directly on CPUs and GPUs. | 這一標準化歧管空間支援直接液冷，也就是 DLC。帶有微通道的金屬冷板直接安裝在 CPU 和 GPU 上。 |
| seg-10 | 00:01:51.220–00:02:06.369 | Using highly reliable, zero-leak fluid connectors, the rack-mounted manifold pumps a water-and-glycol mixture directly to the silicon. It captures up to 80 percent of the heat where it is generated. | 透過高可靠、零洩漏的流體聯結器，機架式歧管把水和乙二醇混合液直接送到晶片，可在熱量產生處捕獲最多 80% 的熱量。 |
| seg-11 | 00:02:06.489–00:02:18.609 | Liquid cooling maximizes the potential of the standard ORv3 rack. But the ultimate solution requires a completely different physical architecture: immersion cooling. | 液冷最大限度地釋放標準 ORv3 機架的潛力，但終極方案需要完全不同的物理架構：浸沒式冷卻。 |
| seg-12 | 00:02:18.729–00:02:39.219 | Instead of sliding servers into a vertical rack, complete servers are submerged in a horizontal tank of nonconductive dielectric fluid. Because the fluid touches every component—CPU, GPU, memory, and networking—no blind-mate manifolds or hoses are required. | 伺服器不再滑入垂直機架，而是整機浸入裝有不導電介電流體的水平槽中。流體會接觸 CPU、GPU、記憶體和網路等每個元件，因此不需要盲插歧管或軟管。 |
| seg-13 | 00:02:39.339–00:02:44.799 | In single-phase immersion, the fluid absorbs the heat. | 在單相浸沒式冷卻中，流體吸收熱量。 |
| seg-14 | 00:02:44.919–00:02:56.480 | In two-phase immersion, extreme heat boils the fluid. The phase change lets the vapor condense and cool the hardware at unmatched scale. | 在兩相浸沒式冷卻中，極高熱量使流體沸騰。相變產生的蒸汽隨後冷凝，以前所未有的規模為硬體降溫。 |
| seg-15 | 00:02:56.600–00:03:05.350 | Whether using cold plates or a full immersion tank, liquid cooling is no longer a science experiment. It is a survival requirement. | 無論採用冷板還是完整浸沒槽，液冷都已不再是科學實驗，而是維持執行的必要條件。 |
| seg-16 | 00:03:05.470–00:03:11.310 | The hardware is built and the specifications are published. The only thing left is deployment. | 硬體已經建成，規範也已釋出。最後一步就是部署。 |

Technical values, years, voltages, OCP names, and confirmed source terminology are preserved from the reviewed English source.

## Audio mix

The source audio stream is not mapped. The aligned Traditional Chinese voice-only master is mixed over viacheslavstarostin-background-backsound-music-educational-364858.mp3, normalized to -27 LUFS. Music fades in, sidechain-ducks beneath actual narration, restores between phrases, and fades over the video's final four seconds.

The original source-language audio is excluded. The localized video, caption track, and voice timing were validated before publication. Maximum applied tempo adjustment: **1.0000×**.
