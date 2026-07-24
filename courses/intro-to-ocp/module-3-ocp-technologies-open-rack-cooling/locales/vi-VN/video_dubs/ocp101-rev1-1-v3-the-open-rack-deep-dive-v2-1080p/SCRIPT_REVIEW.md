# Vietnamese dubbing script review

Status: **localized-mix-ready-for-course-build**
Voice: **Nhu** (`A5w1fw5x0uXded1LDvZp`)
Model: **`eleven_flash_v2_5`**
Audio policy: **localized narration with AcademyWizard background music**

| Segment | Window | English | Vietnamese |
|---|---:|---|---|
| seg-01 | 00:00:03.700–00:00:09.669 | We have covered the history and the community. Now let us get hands-on. | Chúng ta đã tìm hiểu lịch sử và cộng đồng. Bây giờ hãy đi sâu vào thực tế. |
| seg-02 | 00:00:09.789–00:00:17.580 | This is Open Rack version 3, or ORv3. It is the physical foundation of the modern AI-driven data center. | Đây là Open Rack phiên bản 3, hay ORv3. Nó là nền tảng vật lý của trung tâm dữ liệu hiện đại được vận hành bởi AI. |
| seg-03 | 00:00:17.700–00:00:24.220 | To understand why it is built this way, you must understand the architecture of power. | Để hiểu vì sao ORv3 được thiết kế như vậy, trước hết cần hiểu kiến trúc phân phối điện. |
| seg-04 | 00:00:24.340–00:00:33.220 | In a traditional 19-inch rack, every server had its own power supply, plugged into a large power strip known as a PDU. | Trong tủ rack 19 inch truyền thống, mỗi máy chủ có bộ nguồn riêng và cắm vào một bộ phân phối điện lớn gọi là PDU. |
| seg-05 | 00:00:33.340–00:00:41.960 | Early Open Rack designs solved this cable mess by replacing the power strips with a centralized 12-volt bus bar built into the frame. | Open Rack đời đầu xử lý mớ cáp bằng thanh cái 12 volt tập trung, tích hợp trong khung thay cho bộ phân phối điện. |
| seg-06 | 00:00:42.080–00:00:51.560 | That worked for standard cloud servers drawing 10 to 15 kilowatts. But today's AI clusters demand 100 kilowatts or more per rack. | Giải pháp đó phù hợp với máy chủ đám mây tiêu chuẩn tiêu thụ từ 10 đến 15 kilowatt. Nhưng các cụm AI hiện nay cần 100 kilowatt trở lên cho mỗi rack. |
| seg-07 | 00:00:51.680–00:01:03.880 | If you push that much power at 12 volts, the current rises dramatically. This goes far beyond simple power loss. | Nếu truyền công suất lớn như vậy ở 12 volt, dòng điện sẽ tăng mạnh. Vấn đề không chỉ là tổn hao công suất. |
| seg-08 | 00:01:04.000–00:01:09.240 | Sending that much current through a 12-volt bus bar would be catastrophic. It could melt the copper, throw sparks, and cause total system failure. | Ở 12 volt, dòng lớn có thể nung chảy đồng, phát tia lửa và phá hỏng hệ thống. |
| seg-09 | 00:01:09.360–00:01:18.829 | So the Rack & Power Project changed the standard. ORv3 uses a 48-volt DC bus bar. | Vì vậy, dự án Rack & Power đã thay đổi tiêu chuẩn. ORv3 sử dụng thanh cái điện một chiều 48 volt. |
| seg-10 | 00:01:18.949–00:01:31.049 | By increasing the voltage, we reduce heat loss by a factor of 16. More power reaches the silicon instead of burning up in the infrastructure. | Khi tăng điện áp, tổn hao do nhiệt giảm 16 lần. Nhiều điện năng đến được silicon hơn thay vì bị tiêu hao trong hạ tầng. |
| seg-11 | 00:01:31.169–00:01:35.890 | We also completely reimagined power delivery. | Chúng tôi cũng thiết kế lại hoàn toàn phương thức cấp điện. |
| seg-12 | 00:01:36.010–00:01:46.670 | In a traditional setup, every server has its own redundant power supply, usually operating at a low and inefficient utilization rate. | Trong cấu hình truyền thống, mỗi máy chủ có bộ nguồn dự phòng riêng, thường vận hành ở mức tải thấp và kém hiệu quả. |
| seg-13 | 00:01:46.790–00:01:57.519 | ORv3 pools that workload. It replaces dozens of individual power supplies with one centralized power shelf loaded with modular rectifiers. | ORv3 gộp nhu cầu cấp điện đó. Hàng chục bộ nguồn riêng lẻ được thay bằng một kệ nguồn tập trung chứa các mô-đun chỉnh lưu. |
| seg-14 | 00:01:57.639–00:02:06.199 | By consolidating AC-to-DC conversion for the entire rack, we increase utilization and reduce power loss. | Bằng cách hợp nhất quá trình chuyển đổi từ điện xoay chiều sang điện một chiều cho toàn bộ rack, chúng tôi tăng mức sử dụng và giảm tổn hao điện năng. |
| seg-15 | 00:02:06.319–00:02:18.900 | This centralized approach simplifies deployment. IT gear slides in and connects to the power spine without manual wiring, and no thick power cords block exhaust airflow. | Cách tiếp cận tập trung này giúp triển khai đơn giản hơn. Thiết bị công nghệ thông tin chỉ cần trượt vào rack và kết nối với trục nguồn, không cần đi dây thủ công; đồng thời không còn dây nguồn dày cản luồng khí thoát. |
| seg-16 | 00:02:19.020–00:02:27.480 | Eliminating server power supplies frees motherboard space, enabling denser compute and better system airflow. | Loại bỏ bộ nguồn riêng của máy chủ cũng giải phóng không gian trên bo mạch chủ, cho phép tăng mật độ tính toán và cải thiện luồng không khí trong hệ thống. |
| seg-17 | 00:02:27.600–00:02:40.700 | Delivering that much power creates two more challenges: extreme weight and extreme heat. The ORv3 frame is reinforced for the massive weight of modern GPU chassis. | Cấp công suất lớn như vậy tạo ra thêm hai thách thức: trọng lượng cực lớn và tải nhiệt cực cao. Khung ORv3 được gia cường để chịu được trọng lượng lớn của các khung máy GPU hiện đại. |
| seg-18 | 00:02:40.820–00:03:00.730 | More importantly, the ORv3 frame prepares the data center for the next generation of heat. Liquid-cooling manifolds integrate directly into the rack architecture. ORv3 introduces the Open Compute Universal Quick Disconnect standard, or UQD. | Quan trọng hơn, khung ORv3 chuẩn bị trung tâm dữ liệu cho thế hệ tải nhiệt tiếp theo. Các ống góp làm mát bằng chất lỏng được tích hợp trực tiếp vào kiến trúc rack. ORv3 cũng giới thiệu tiêu chuẩn Open Compute Universal Quick Disconnect, hay UQD. |
| seg-19 | 00:03:00.850–00:03:10.240 | Server gear slides directly into the rack and connects its liquid-cooling circuits safely, seamlessly, and without drips. | Thiết bị máy chủ trượt trực tiếp vào rack và kết nối với mạch làm mát bằng chất lỏng một cách an toàn, liền mạch và không rò rỉ. |
| seg-20 | 00:03:10.360–00:03:19.720 | We solved the power-delivery bottleneck, but extracting the heat is a different challenge. Let us see how these racks avoid melting down. | Chúng ta đã giải quyết điểm nghẽn trong cấp điện, nhưng tản nhiệt lại là một thách thức khác. Hãy xem những rack này tránh quá nhiệt như thế nào. |

Technical values, years, voltages, OCP names, and confirmed source terminology are preserved from the reviewed English source.

## Audio mix

The source audio stream will not be mapped. The aligned Vietnamese voice-only master will be mixed over the same AcademyWizard music asset used by the other language editions.

Narration-time music ducking: threshold **0.003**, ratio **12.0:1**, attack **80.0 ms**, release **500.0 ms**.

The original source-language audio is excluded. The localized video, caption track, and voice timing were validated before publication. Maximum applied tempo adjustment: **1.0000×**.
