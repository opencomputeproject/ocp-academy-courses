# Japanese dubbing script — ocp101-rev1-1-v3-the-open-rack-deep-dive-v2-1080p

Status: **localized-mix-with-library-music-awaiting-listening-review**

Voice: **Japanese** (`b34JylakFZPlGS0BnwyY`)

Technical values, acronyms, product names, and the OCP Scale/スケール tenet are preserved. Narration timing windows must not be crossed.

## 01 · 00:00:03,700–00:00:09,669

**English:** We have covered the history and the community. Now let us get hands-on.

**Japanese:** これまでに歴史とコミュニティを学びました。ここからは、実際のハードウェアを見ていきます。

## 02 · 00:00:09,789–00:00:17,580

**English:** This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center.

**Japanese:** これが Open Rack バージョン3、ORv3 です。AI 主導の現代的なデータセンターを支える物理基盤です。

## 03 · 00:00:17,700–00:00:24,220

**English:** To understand why it is built this way, you must understand the architecture of power.

**Japanese:** なぜこの構造になっているのかを理解するには、電力アーキテクチャを理解する必要があります。

## 04 · 00:00:24,340–00:00:33,220

**English:** In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU.

**Japanese:** 従来の19インチラックでは、各サーバーが個別の電源装置を持ち、PDU と呼ばれる大型の電源タップに接続されていました。

## 05 · 00:00:33,340–00:00:41,960

**English:** Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame.

**Japanese:** 初期の Open Rack は、電源タップをフレーム内蔵の集中型12ボルトバスバーに置き換え、複雑なケーブル配線を解消しました。

## 06 · 00:00:42,080–00:00:51,560

**English:** That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack.

**Japanese:** 10から15キロワットの一般的なクラウドサーバーには十分でした。しかし今の AI クラスターは、ラック当たり100キロワット以上を必要とします。

## 07 · 00:00:51,680–00:01:03,880

**English:** If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss.

**Japanese:** 12ボルトのまま大電力を供給すると、電流が急激に増えます。問題は、単なる電力損失にとどまりません。

## 08 · 00:01:04,000–00:01:09,240

**English:** Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure.

**Japanese:** 12ボルトで大電流を流せば、銅が溶け、火花が飛び、システムが故障します。

## 09 · 00:01:09,360–00:01:18,829

**English:** So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar.

**Japanese:** そこで Rack & Power プロジェクトは標準を変更しました。ORv3 は48ボルト直流バスバーを使用します。

## 10 · 00:01:18,949–00:01:31,049

**English:** By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure.

**Japanese:** 電圧を上げることで、熱損失を16分の1に抑えられます。インフラ内で熱として失われる電力が減り、より多くの電力がシリコンへ届きます。

## 11 · 00:01:31,169–00:01:35,890

**English:** We also completely reimagined power delivery.

**Japanese:** さらに、電力供給の仕組みそのものを全面的に見直しました。

## 12 · 00:01:36,010–00:01:46,670

**English:** In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate.

**Japanese:** 従来の構成では、各サーバーが冗長電源を個別に備え、多くの場合、使用率が低く非効率な状態で動作します。

## 13 · 00:01:46,790–00:01:57,519

**English:** ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers.

**Japanese:** ORv3 はその負荷を集約します。多数の個別電源を、モジュラー整流器を搭載した一つの集中型電源シェルフに置き換えます。

## 14 · 00:01:57,639–00:02:06,199

**English:** By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss.

**Japanese:** ラック全体の交流から直流への変換を集約することで、使用率を高め、電力損失を減らします。

## 15 · 00:02:06,319–00:02:18,900

**English:** This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow.

**Japanese:** この集中型方式は導入も簡素化します。IT 機器を差し込むだけで、手作業の配線なしに電源スパインへ接続でき、太い電源ケーブルが排気の流れを妨げることもありません。

## 16 · 00:02:19,020–00:02:27,480

**English:** Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow.

**Japanese:** サーバーごとの電源装置をなくすことで、マザーボード上のスペースが空き、より高密度なコンピューティングと良好なシステムエアフローを実現できます。

## 17 · 00:02:27,600–00:02:40,700

**English:** Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis.

**Japanese:** 大電力の供給には、さらに二つの課題があります。非常に大きな重量と、非常に高い発熱です。ORv3 フレームは、最新の GPU シャーシの大重量を支えられるよう強化されています。

## 18 · 00:02:40,820–00:03:00,730

**English:** More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD.

**Japanese:** さらに重要なのは、ORv3 フレームが次世代の発熱に備えていることです。液冷マニホールドをラック構造へ直接統合し、Open Compute Universal Quick Disconnect、UQD 標準を導入しています。

## 19 · 00:03:00,850–00:03:10,240

**English:** Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips.

**Japanese:** サーバー機器をラックへ差し込むと、液冷回路が安全かつシームレスに接続され、液漏れもありません。

## 20 · 00:03:10,360–00:03:19,720

**English:** We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down.

**Japanese:** 電力供給のボトルネックは解決しました。しかし、熱を取り除くことは別の課題です。次に、ラックの過熱を防ぐ方法を見てみましょう。

## Audio mix

Background track: `viacheslavstarostin-educational-learning-study-music-473828.mp3`. The original source audio is excluded. The localized voice-only master remains in the foreground while normalized music ducks smoothly during speech, restores between phrases, and fades over the final four seconds. Listening review is required.
