# Incident Investigation Report: Silent Pipeline Stall in Astronomy Shop (orders-validator Poison Pill & accounting OOM)

## Block 01: Question and Scope

* **What is broken:** 
  1. **Sự cố cốt lõi (Silent Critical Outage):** Dịch vụ `orders-validator` bị treo hoàn toàn tiến trình xử lý đơn hàng (pipeline stall) do gặp thông điệp lỗi độc hại (Poison Pill message) tại `offset=20` trên Kafka topic `orders-fulfillment`. Toàn bộ đơn hàng mới (hàng chục nghìn đơn hàng được xuất bản với tốc độ 2 đơn/giây) đều bị kẹt cứng trong hàng đợi và không được xác thực. Dù pod vẫn hiển thị `Running` (1/1 Ready, 0 restarts), chức năng nghiệp vụ đã chết hoàn toàn suốt 12 giờ 44 phút qua.
  2. **Sự cố đi kèm (Co-existing Crash Loop):** Pod `accounting` liên tục bị cgroup OOM Killer tiêu diệt định kỳ (~14.5 phút/lần, 53 lần restart) do cấu hình trần bộ nhớ 120Mi quá thấp.
* **For whom:** Khách hàng đặt hàng nhưng không bao giờ được xác nhận đơn và chuyển sang trạng thái hoàn tất; hệ thống hoàn tất đơn hàng (order fulfillment) bị ngưng trệ 100%.
* **Since when:** Bắt đầu chính xác vào lúc `2026-09-18T15:33:33.952Z` (khi tin nhắn tại offset=20 được đọc).
* **Access limits ([Blocked]):**
  * **RBAC Scope:** ServiceAccount `sandbox-access:sandbox-readonly` chỉ được phân quyền trong namespace `astronomy-shop`. Toàn bộ 6 namespace khác (`default`, `kube-system`, v.v.) trả về `Forbidden` `[Blocked]`.
  * **Container Exec & Service Proxy:** Thao tác `kubectl exec` vào các pod `kafka`, `jaeger`, `opensearch` và `services/proxy` đều bị hệ thống phân quyền từ chối `[Blocked]`.
  * **Metrics Server:** Không có `metrics-server` trên cụm, lệnh `kubectl top` không hoạt động `[Blocked]`.

---

## Block 02: Hypotheses, One Ruled Out

### Giả thuyết A: Sự cố do mạng Kafka broker bị sập hoặc do Feature Flag chaos injection
* **Nội dung:** Kết nối tới Kafka broker bị đứt quãng hoặc cờ `kafkaQueueProblems` trong `flagd-config` được bật làm gián đoạn việc truyền nhận dữ liệu.
* **Truy vấn kiểm tra:** `kubectl get configmap flagd-config -n astronomy-shop -o yaml` và nhật ký của `fraud-detection`.
* **Kết quả đối chiếu:** **[Ruled Out - Đã bị loại trừ hoàn toàn]**
  * Trong `flagd-config`, cờ `kafkaQueueProblems` đặt `defaultVariant: "off"`.
  * Dịch vụ `fraud-detection` vẫn đang kết nối Kafka và tiêu thụ đơn hàng bình thường (số lượng đơn xử lý tăng liên tục từ 4460 lên 4574). Kafka broker hoạt động ổn định.

### Giả thuyết B: Lỗi Poison Pill tại Kafka offset=20 và thiếu cơ chế Dead-Letter Queue (Root Cause)
* **Nội dung:** Một thông điệp sai định dạng JSON rơi vào topic `orders-fulfillment`. Do `orders-validator` không có cơ chế xử lý lỗi/Dead-Letter Queue (DLQ), tiến trình chủ động pause partition và kẹt vĩnh viễn tại `offset=20`.
* **Truy vấn kiểm tra:** `kubectl logs deploy/orders-validator -n astronomy-shop --tail=300`
* **Kết quả đối chiếu:** **[Verified - Đã được xác thực trực tiếp bằng raw log]**
  * Ghi nhận chính xác dòng lỗi parse JSON tại offset 20 lúc `15:33:33.952Z`.
  * Ghi nhận cảnh báo `partition remains paused at offset=20` lặp lại đều đặn mỗi 15 giây liên tục trong suốt 12 giờ 44 phút.

---

## Block 03: Evidence (Source, Scope, Time)

### Bằng chứng 01: Lỗi Poison Pill và phân vùng bị đóng băng (The Poison Pill Log)
* **Source:** `kubectl logs deploy/orders-validator -n astronomy-shop --tail=300 --timestamps`
* **Scope:** Deployment `orders-validator`, namespace `astronomy-shop`
* **Time:** Bắt đầu lúc `2026-09-18T15:33:33.952Z` đến hiện tại
* **Label:** `[Verified]`
* **Raw Output:**
```text
2026-09-18T15:33:33.952Z ERROR record validation failed at offset=20: Expecting value: line 1 column 35 (char 34)
2026-09-18T15:33:33.953Z ERROR partition processing paused at offset=20
...
2026-09-19T04:15:15.102Z ERROR partition remains paused at offset=20
2026-09-19T04:15:30.105Z ERROR partition remains paused at offset=20
```

### Bằng chứng 02: Bề ngoài Healthy nhưng chức năng ngưng trệ (False-Positive Health Check)
* **Source:** `kubectl get pods -n astronomy-shop -l app.kubernetes.io/name=orders-validator`
* **Scope:** Pod `orders-validator`, namespace `astronomy-shop`
* **Time:** `2026-09-19T04:18:00Z`
* **Label:** `[Verified]`
* **Raw Output:**
```text
NAME                                READY   STATUS    RESTARTS   AGE
orders-validator-79c857754d-k8px9   1/1     Running   0          12h
```
* **Phân tích:** Pod có 0 lần restart, probe báo Ready 1/1 khiến mọi dashboard giám sát bề nổi đều báo xanh (Healthy), trong khi thực tế dữ liệu nghiệp vụ đã bị nghẽn hoàn toàn.

### Bằng chứng 03: Lưu lượng mới liên tục xuất bản nhưng không được xử lý
* **Source:** `kubectl logs deploy/order-stream -n astronomy-shop --tail=50`
* **Scope:** Deployment `order-stream`
* **Time:** `2026-09-19T04:18:00Z`
* **Label:** `[Verified]`
* **Raw Output:** `order-stream` xuất bản đều đặn ~2 đơn hàng/giây vào topic `orders-fulfillment`. Hàng chục nghìn đơn hàng đang bị xếp hàng phía sau offset 20.

### Bằng chứng 04: Sự cố OOMKilled song song trên service `accounting`
* **Source:** `kubectl get pod -n astronomy-shop -l app.kubernetes.io/name=accounting -o yaml`
* **Scope:** Pod `accounting-5897477844-lbn6s`
* **Time:** `2026-09-19T04:02:43Z`
* **Label:** `[Verified]`
* **Raw Output:** `restartCount: 53`, `exitCode: 137`, `reason: OOMKilled`, `limits.memory: 120Mi`.

---

## Block 04: The Mechanism

### Cơ chế tác động dây chuyền (The Causal Mechanism)
```
[order-stream] ──(Xuất bản 2 msg/s)──> [Kafka topic: orders-fulfillment]
                                                    │
                             ┌──────────────────────┴──────────────────────┐
                             ▼                                             ▼
                   [offset=1..19: OK]                            [offset=20: Malformed JSON]
                             │                                             │
                             ▼                                             ▼
                 [orders-validator xử lý]                       [JSON parser văng lỗi char 34]
                                                                           │
                                                                           ▼
                                                             [Logic dừng: partition paused]
                                                                           │
                                                                           ▼
                                                             [Thiếu DLQ / Không skip]
                                                                           │
                                                                           ▼
                                                             [Toàn bộ đơn mới từ offset 21+
                                                              bị tắc nghẽn vô thời hạn]
```

1. **Khởi tạo và chạy bình thường:** Lúc `15:33:30Z`, `orders-validator` xử lý trơn tru các đơn hàng `ORD-100000` đến `ORD-100019` (offsets 1-19).
2. **Kích hoạt Poison Pill:** Đúng `15:33:33.952Z`, một bản ghi hỏng rơi vào offset 20 (`Expecting value: line 1 column 35`).
3. **Phản ứng sai lầm của ứng dụng:** Mã nguồn ứng dụng bắt lỗi bằng cách tạm dừng phân vùng (`partition paused`), nhưng không có cơ chế chuyển bản ghi lỗi sang Dead-Letter Queue (DLQ), không có logic bỏ qua (skip), và cũng không tự sập pod để kích hoạt cảnh báo.
4. **Hậu quả dây chuyền:** Toàn bộ lưu lượng đơn hàng mới từ `order-stream` bị dồn ứ vô hạn trong Kafka topic.

---

## Block 05: Root Cause and Response

### Phân định nguyên nhân
* **Trigger ([Verified]):** Bản ghi lỗi không đúng chuẩn JSON tại `offset=20` trên topic `orders-fulfillment` xuất hiện lúc `2026-09-18T15:33:33.952Z`.
* **Root Cause ([Verified]):** Dịch vụ `orders-validator` thiếu cơ chế xử lý ngoại lệ (Exception Handling) và thiếu hàng đợi thư chết (Dead-Letter Queue - DLQ), dẫn đến việc phân vùng Kafka bị tạm dừng vĩnh viễn ngay khi gặp bản tin độc hại.
* **Contributing Factor ([Inferred]):** Health check (Liveness/Readiness probe) chỉ kiểm tra container có đang chạy hay không mà không kiểm tra tiến độ tiêu thụ offset (consumer lag), tạo ra tín hiệu giả "Healthy" trên dashboard.

### Đề xuất phương án khắc phục (Recommended Response)
1. **Khắc phục khẩn cấp (Immediate Workaround):**
   * Can thiệp Kafka consumer group để commit bỏ qua offset 20 (seek forward to offset 21) nhằm giải phóng hàng chục nghìn đơn hàng đang bị dồn ứ:
     `kafka-consumer-groups.sh --bootstrap-server kafka:9092 --group orders-validator-group --topic orders-fulfillment --reset-offsets --to-offset 21 --execute`
2. **Khắc phục triệt để (Permanent Fix):**
   * Cập nhật mã nguồn `orders-validator`: bổ sung `try/catch` khi parse JSON. Nếu bản ghi lỗi, tự động đẩy vào topic `orders-fulfillment-dlq` kèm cảnh báo và tiếp tục commit offset.
   * Bổ sung Readiness Probe kiểm tra độ trễ Kafka consumer lag thay vì chỉ kiểm tra tiến trình HTTP/TCP đơn thuần.
   * Đồng thời nâng `limits.memory` của `accounting` lên `384Mi` để chấm dứt vòng lặp OOMKilled.
3. **Người chịu trách nhiệm phê duyệt (Named Approver):**
   * Principal Backend Engineer / Lead Platform Engineer.
4. **Tiêu chí kiểm tra sau khắc phục (Post-Remediation Verification):**
   * Log của `orders-validator` không còn dòng `partition remains paused at offset=20`.
   * Offset của consumer group tăng liên tục, số lượng đơn hàng được validate bắt kịp với tốc độ phát sinh của `order-stream`.
