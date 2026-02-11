**ORCHESTRATOR + HẠ TẦNG LIÊN KẾT**

**Trọng tâm:** Xây dựng hệ điều hành của hệ thống, luồng dữ liệu và cách
các thành phần giao tiếp.

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 33%" />
<col style="width: 46%" />
</colgroup>
<thead>
<tr>
<th><strong>Folder</strong></th>
<th><strong>File cần build</strong></th>
<th><strong>Nhiệm vụ chi tiết</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>orchestrators/</strong></td>
<td><p>base_orchestrator.py</p>
<p>langgraph_orchestrator.py</p></td>
<td>Thiết lập bộ não điều phối, định nghĩa sơ đồ trạng thái (State
Machine) của toàn hệ thống.</td>
</tr>
<tr>
<td><strong>protocols/</strong></td>
<td><p>base_protocol.py</p>
<p>mcp_protocol.py</p>
<p>a2a_protocol.py</p></td>
<td>Định nghĩa cấu trúc dữ liệu chuẩn (Message Schema) để Người 2 và
Người 3 truyền nhận dữ liệu không bị lỗi.</td>
</tr>
<tr>
<td><strong>workflows/</strong></td>
<td><p>sequential_workflow.py</p>
<p>hybrid_workflow.py</p></td>
<td>Thiết lập trình tự chạy của các Agent (ví dụ: lấy tin trước, phân
tích sau).</td>
</tr>
<tr>
<td><strong>scripts/</strong></td>
<td>run_agent.py</td>
<td>Viết file thực thi chính để khởi động toàn bộ hệ thống từ CLI.</td>
</tr>
<tr>
<td><strong>Root/</strong></td>
<td><p>Dockerfile</p>
<p>docker-compose.yaml</p></td>
<td>Đóng gói ứng dụng để đảm bảo chạy được trên mọi máy tính.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

**AGENTS + TƯ DUY SUY LUẬN**

**Trọng tâm:** Xây dựng sự thông minh, khả năng suy luận và cá nhân hóa
lời khuyên.

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 32%" />
<col style="width: 46%" />
</colgroup>
<thead>
<tr>
<th><strong>Folder</strong></th>
<th><strong>File cần build</strong></th>
<th><strong>Nhiệm vụ chi tiết</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>agents/</strong></td>
<td><p>base_agent.py</p>
<p>planning_agent.py</p>
<p>monitoring_agent.py</p></td>
<td>Tạo lớp cơ sở cho Agent; viết Agent lập kế hoạch nhiệm vụ và Agent
giám sát chất lượng đầu ra.</td>
</tr>
<tr>
<td><strong>agents/custom/</strong></td>
<td>sentiment_agent.py</td>
<td><strong>Quan trọng nhất:</strong> Viết logic suy luận để AI hiểu tin
tức tài chính và tác động của nó lên túi tiền người dùng.</td>
</tr>
<tr>
<td><strong>memory/</strong></td>
<td><p>vector_memory.py</p>
<p>conversation_memory.py</p></td>
<td>Thiết lập cách AI ghi nhớ danh mục đầu tư (Portfolio) và các câu
thoại trước đó của người dùng.</td>
</tr>
<tr>
<td><strong>configs/</strong></td>
<td>model_config.yaml</td>
<td>Tinh chỉnh các tham số AI (Temperature, Max tokens, Model ID) cho
Gemini/GPT.</td>
</tr>
<tr>
<td><strong>services/</strong></td>
<td>llm_service.py</td>
<td>Viết wrapper để kết nối với API của các mô hình ngôn ngữ lớn.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

**Data & Tool Engineer (Kỹ sư Dữ liệu & Công cụ)**

**Trọng tâm:** Cung cấp "nguyên liệu" (dữ liệu) và "vũ khí" (công cụ
thực thi) cho hệ thống.

<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 30%" />
<col style="width: 41%" />
</colgroup>
<thead>
<tr>
<th><strong>Folder</strong></th>
<th><strong>File cần build</strong></th>
<th><strong>Nhiệm vụ chi tiết</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>tools/</strong></td>
<td><p>base_tool.py</p>
<p>search_tool.py</p>
<p>database_tool.py</p></td>
<td>Viết code kết nối API Yahoo Finance để lấy tin và truy vấn database
danh mục đầu tư.</td>
</tr>
<tr>
<td><strong>tools/function_tools/</strong></td>
<td>summarize_tool.py</td>
<td>Viết các hàm tiện ích như tóm tắt văn bản dài thành ý chính.</td>
</tr>
<tr>
<td><strong>data/</strong></td>
<td>embeddings/</td>
<td>Xử lý tập dữ liệu <strong>Kaggle Financial Sentiment</strong>,
chuyển thành vector và lưu trữ để AI so sánh.</td>
</tr>
<tr>
<td><strong>services/</strong></td>
<td>vector_store_service.py</td>
<td>Xây dựng dịch vụ truy vấn cơ sở dữ liệu vector
(ChromaDB/Pinecone).</td>
</tr>
<tr>
<td><strong>utils/</strong></td>
<td><p>logger.py</p>
<p>retry.py</p>
<p>helpers.py</p></td>
<td>Viết các hàm hỗ trợ: ghi log, tự động gọi lại khi lỗi, và xử lý định
dạng tiền tệ/số liệu.</td>
</tr>
<tr>
<td><strong>tests/</strong></td>
<td>Toàn bộ folder</td>
<td>Viết Unit Test để đảm bảo Tool trả về đúng dữ liệu và Agent không
tính toán sai.</td>
</tr>
</tbody>
</table>
