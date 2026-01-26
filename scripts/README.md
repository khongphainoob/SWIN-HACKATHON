# scripts

Script khởi chạy hệ thống và các demo. Hỗ trợ kiểm thử và trình diễn chức năng hệ thống.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseScript`) để các script chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_script import BaseScript

class DemoScript(BaseScript):
	def run(self):
		# Logic chạy demo
		pass
```

Tạo file `base_script.py` để định nghĩa class nền cho các script.