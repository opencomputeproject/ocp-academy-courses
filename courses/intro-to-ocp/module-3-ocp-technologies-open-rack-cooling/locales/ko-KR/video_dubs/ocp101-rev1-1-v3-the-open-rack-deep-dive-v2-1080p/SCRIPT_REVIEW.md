# Korean dubbing script — ocp101-rev1-1-v3-the-open-rack-deep-dive-v2-1080p

Status: **localized-mix-with-library-music-awaiting-listening-review**

Source video: `ocp101-rev1-1-v3-the-open-rack-deep-dive-v2-1080p.mp4`

Voice: **Chris - Warm and clear** (`PDoCXqBQFGsvfO0hNkEs`)

Clear speech-recognition errors were normalized before translation. Technical values, acronyms, product names, and the OCP Scale/확장성 tenet are preserved. Narration timing windows must not be crossed.

## Generated-media checks

- Utterances: 20
- Timing overruns: 0
- Korean caption cues: 50

## 01 · 00:00:03,700–00:00:09,669

**English:** We have covered the history and the community. Now let us get hands-on.

**Korean:** 지금까지 역사와 커뮤니티를 살펴보았습니다. 이제 하드웨어를 직접 살펴보겠습니다.

## 02 · 00:00:09,789–00:00:17,580

**English:** This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center.

**Korean:** 이것이 Open Rack 버전 3, 즉 ORv3입니다. 현대적인 AI 데이터센터를 지탱하는 물리적 기반입니다.

## 03 · 00:00:17,700–00:00:24,220

**English:** To understand why it is built this way, you must understand the architecture of power.

**Korean:** 왜 이런 구조로 만들어졌는지 이해하려면 전력 아키텍처부터 이해해야 합니다.

## 04 · 00:00:24,340–00:00:33,220

**English:** In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU.

**Korean:** 기존 19인치 랙에서는 모든 서버에 PDU라는 대형 전원 스트립에 연결되는 자체 전원 공급 장치가 있었습니다.

## 05 · 00:00:33,340–00:00:41,960

**English:** Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame.

**Korean:** 초기 Open Rack 설계는 전원 스트립을 프레임에 내장된 중앙형 12볼트 버스바로 바꾸어 복잡한 케이블 문제를 해결했습니다.

## 06 · 00:00:42,080–00:00:51,560

**English:** That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack.

**Korean:** 이는 10~15kW를 소비하는 표준 클라우드 서버에서 작동했습니다. 그러나 오늘날의 AI 클러스터는 랙당 100kW 이상을 요구합니다.

## 07 · 00:00:51,680–00:01:03,880

**English:** If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss.

**Korean:** 12V에서 그 정도의 전력을 공급하면 전류가 극적으로 증가합니다. 이는 단순한 전력 손실을 훨씬 넘어서는 것입니다.

## 08 · 00:01:04,000–00:01:09,240

**English:** Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure.

**Korean:** 이 전류는 구리를 녹이고 불꽃을 일으켜 시스템 전체를 멈출 수 있습니다.

## 09 · 00:01:09,360–00:01:18,829

**English:** So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar.

**Korean:** 그래서 Rack & Power 프로젝트는 표준을 바꾸었습니다. ORv3는 48볼트 DC 버스바를 사용합니다.

## 10 · 00:01:18,949–00:01:31,049

**English:** By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure.

**Korean:** 전압을 높이면 열 손실을 16분의 1로 줄일 수 있습니다. 인프라에서 소모되는 전력은 줄고, 더 많은 전력이 실리콘에 도달합니다.

## 11 · 00:01:31,169–00:01:35,890

**English:** We also completely reimagined power delivery.

**Korean:** 우리는 또한 전력 공급을 완전히 재구상했습니다.

## 12 · 00:01:36,010–00:01:46,670

**English:** In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate.

**Korean:** 기존 설정에서는 모든 서버에 자체 중복 전원 공급 장치가 있어 일반적으로 낮고 비효율적인 활용률로 작동합니다.

## 13 · 00:01:46,790–00:01:57,519

**English:** ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers.

**Korean:** ORv3는 전력 변환 부하를 한곳에 모읍니다. 수십 개의 개별 전원 공급 장치를 모듈식 정류기가 장착된 하나의 중앙 전원 선반으로 대체합니다.

## 14 · 00:01:57,639–00:02:06,199

**English:** By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss.

**Korean:** 전체 랙에 대해 AC-to-DC 변환을 통합함으로써 활용도를 높이고 전력 손실을 줄입니다.

## 15 · 00:02:06,319–00:02:18,900

**English:** This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow.

**Korean:** 이 중앙형 구조는 설치를 단순화합니다. IT 장비를 밀어 넣으면 수동 배선 없이 전력 스파인에 연결되고, 두꺼운 전원 케이블이 배기 공기 흐름을 막지도 않습니다.

## 16 · 00:02:19,020–00:02:27,480

**English:** Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow.

**Korean:** 서버 전원 공급 장치를 제거하면 마더보드 공간이 확보되어 밀도가 높은 컴퓨팅과 더 나은 시스템 공기 흐름이 가능해집니다.

## 17 · 00:02:27,600–00:02:40,700

**English:** Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis.

**Korean:** 그 정도의 전력을 공급하려면 극도의 무게와 극심한 열이라는 두 가지 과제가 더 발생합니다. ORv3 프레임은 최신 GPU 섀시의 엄청난 무게를 위해 강화되었습니다.

## 18 · 00:02:40,820–00:03:00,730

**English:** More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD.

**Korean:** 더 중요한 것은 ORv3 프레임이 차세대 열에 대비하여 데이터센터를 준비한다는 것입니다. 액체 냉각 매니폴드는 랙 아키텍처에 직접 통합됩니다. ORv3는 Open Compute Universal Quick Disconnect 표준, 즉 UQD를 도입했습니다.

## 19 · 00:03:00,850–00:03:10,240

**English:** Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips.

**Korean:** 서버 장비를 랙에 밀어 넣으면 액체 냉각 회로가 누수 없이 안전하고 원활하게 연결됩니다.

## 20 · 00:03:10,360–00:03:19,720

**English:** We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down.

**Korean:** 우리는 전력 공급 병목 현상을 해결했지만 열을 추출하는 것은 다른 과제입니다. 이 랙이 어떻게 녹는 것을 방지하는지 살펴보겠습니다.

## Audio mix

Background track: `viacheslavstarostin-educational-learning-study-music-473828.mp3`. The original source audio is excluded. The localized voice-only master remains in the foreground while normalized music ducks smoothly during speech, restores between phrases, and fades over the final four seconds. Listening review is required.
