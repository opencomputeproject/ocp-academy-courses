# Vietnamese dubbing script review

Status: **localized-mix-ready-for-course-build**
Voice: **Nhu** (`A5w1fw5x0uXded1LDvZp`)
Model: **`eleven_flash_v2_5`**
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Vietnamese |
|---|---:|---|---|
| seg-01 | 00:00:03.059–00:00:11.949 | For decades, data centers used a simple principle to keep servers from overheating: push cold air in the front and blow hot air out the back. | Trong nhiều thập kỷ, trung tâm dữ liệu dùng một nguyên tắc đơn giản để máy chủ không quá nóng: đưa không khí lạnh vào phía trước và thổi không khí nóng ra phía sau. |
| seg-02 | 00:00:12.069–00:00:18.289 | But the density of modern AI silicon has pushed air cooling to its limit. | Nhưng mật độ của silicon AI hiện đại đã đẩy công nghệ làm mát bằng không khí đến giới hạn. |
| seg-03 | 00:00:18.409–00:00:30.609 | Heat cannot be captured and transported fast enough. Air is a poor conductor of heat, while liquid can capture and transport heat thousands of times more efficiently. | Nhiệt không thể được thu và vận chuyển đủ nhanh. Không khí dẫn nhiệt kém, trong khi chất lỏng có thể thu và truyền nhiệt hiệu quả hơn hàng nghìn lần. |
| seg-04 | 00:00:30.729–00:00:45.280 | To support AI clusters drawing 100 kilowatts or more, compared with a standard 12-kilowatt rack, the OCP Cooling Environments Project had to shift industry standards. This transition happens in stages. | Để hỗ trợ các cụm AI tiêu thụ 100 kilowatt trở lên, so với rack tiêu chuẩn chỉ 12 kilowatt, dự án Cooling Environments của OCP phải thay đổi tiêu chuẩn ngành. Quá trình chuyển đổi diễn ra theo từng giai đoạn. |
| seg-05 | 00:00:45.400–00:00:54.519 | For facilities not ready to pipe water directly into servers, rear-door heat exchangers, or RDHx, provide the first step. | Với những cơ sở chưa sẵn sàng dẫn nước trực tiếp vào máy chủ, bộ trao đổi nhiệt cửa sau, hay RDHx, là bước đầu tiên. |
| seg-06 | 00:00:54.639–00:01:06.140 | They come in two forms. Passive systems use a liquid-filled coil. Active systems add a fan wall to assist heat transfer, combining air and liquid cooling. | Có hai dạng. Hệ thống thụ động sử dụng cuộn trao đổi nhiệt chứa chất lỏng. Hệ thống chủ động bổ sung vách quạt để hỗ trợ truyền nhiệt, kết hợp làm mát bằng không khí và chất lỏng. |
| seg-07 | 00:01:06.260–00:01:21.509 | Open Rack V3's success rests on three hardware standards: its 21-inch width, centralized power bus bar, and liquid-manifold stay-out zone. | Thành công của Open Rack V3 dựa trên ba tiêu chuẩn phần cứng: chiều rộng 21 inch, thanh cái điện tập trung và vùng chừa trống dành cho ống góp chất lỏng. |
| seg-08 | 00:01:21.629–00:01:37.869 | Every ORv3 rack reserves standardized physical space specifically for liquid manifolds. In an industry with few liquid standards, this creates a predictable, plug-and-play architecture for fluid delivery. | Mỗi rack ORv3 dành sẵn một không gian vật lý tiêu chuẩn cho ống góp chất lỏng. Trong một ngành còn ít tiêu chuẩn về chất lỏng, điều này tạo ra kiến trúc cắm là chạy có tính dự đoán cho hệ thống phân phối chất lỏng. |
| seg-09 | 00:01:37.989–00:01:51.100 | This standardized manifold space enables direct liquid cooling, or DLC. Metal cold plates with microchannels sit directly on CPUs and GPUs. | Không gian tiêu chuẩn dành cho ống góp này cho phép làm mát trực tiếp bằng chất lỏng, hay DLC. Các tấm lạnh kim loại có vi kênh được đặt trực tiếp trên CPU và GPU. |
| seg-10 | 00:01:51.220–00:02:06.369 | Using highly reliable, zero-leak fluid connectors, the rack-mounted manifold pumps a water-and-glycol mixture directly to the silicon. It captures up to 80 percent of the heat where it is generated. | Thông qua các đầu nối chất lỏng không rò rỉ, độ tin cậy cao, ống góp gắn trên rack bơm hỗn hợp nước và glycol trực tiếp tới silicon. Hệ thống có thể thu đến 80 phần trăm nhiệt ngay tại nguồn phát sinh. |
| seg-11 | 00:02:06.489–00:02:18.609 | Liquid cooling maximizes the potential of the standard ORv3 rack. But the ultimate solution requires a completely different physical architecture: immersion cooling. | Làm mát bằng chất lỏng khai thác tối đa tiềm năng của rack ORv3 tiêu chuẩn. Nhưng giải pháp triệt để nhất đòi hỏi một kiến trúc vật lý hoàn toàn khác: làm mát bằng phương pháp ngâm. |
| seg-12 | 00:02:18.729–00:02:39.219 | Instead of sliding servers into a vertical rack, complete servers are submerged in a horizontal tank of nonconductive dielectric fluid. Because the fluid touches every component—CPU, GPU, memory, and networking—no blind-mate manifolds or hoses are required. | Thay vì trượt máy chủ vào rack đứng, toàn bộ máy chủ được ngâm trong một bể nằm ngang chứa chất lỏng điện môi không dẫn điện. Vì chất lỏng tiếp xúc với mọi thành phần—CPU, GPU, bộ nhớ và thiết bị mạng—không cần ống góp ghép nối mù hay ống mềm. |
| seg-13 | 00:02:39.339–00:02:44.799 | In single-phase immersion, the fluid absorbs the heat. | Trong hệ thống ngâm một pha, chất lỏng hấp thụ nhiệt. |
| seg-14 | 00:02:44.919–00:02:56.480 | In two-phase immersion, extreme heat boils the fluid. The phase change lets the vapor condense and cool the hardware at unmatched scale. | Trong hệ thống ngâm hai pha, nhiệt cực cao làm chất lỏng sôi. Quá trình chuyển pha cho phép hơi ngưng tụ và làm mát phần cứng ở quy mô vượt trội. |
| seg-15 | 00:02:56.600–00:03:05.350 | Whether using cold plates or a full immersion tank, liquid cooling is no longer a science experiment. It is a survival requirement. | Dù sử dụng tấm lạnh hay bể ngâm toàn phần, làm mát bằng chất lỏng không còn là thử nghiệm khoa học. Đây là yêu cầu để hệ thống có thể tiếp tục vận hành. |
| seg-16 | 00:03:05.470–00:03:11.310 | The hardware is built and the specifications are published. The only thing left is deployment. | Phần cứng đã sẵn sàng và các đặc tả đã được công bố. Việc còn lại là triển khai. |

Technical values, years, voltages, OCP names, and confirmed source terminology are preserved from the reviewed English source.

## Audio mix

The source audio stream will not be mapped. The aligned Vietnamese voice-only master will be mixed over the same AcademyWizard music asset used by the other language editions.

Narration-time music ducking: threshold **0.003**, ratio **12.0:1**, attack **80.0 ms**, release **500.0 ms**.

The original source-language audio is excluded. The localized video, caption track, and voice timing were validated before publication. Maximum applied tempo adjustment: **1.0000×**.
