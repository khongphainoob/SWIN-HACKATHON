# data

Kho lưu trữ dữ liệu như Kaggle dataset, Embeddings. Dùng cho huấn luyện và truy vấn.

## Sử dụng class base để kế thừa và phát triển

Nên định nghĩa một class nền (ví dụ: `BaseDataStore`) để các loại kho dữ liệu chuyên biệt kế thừa và mở rộng.

### Ví dụ kế thừa
```python
from base_datastore import BaseDataStore

class KaggleDataStore(BaseDataStore):
	def load(self):
		# Logic tải dữ liệu
		pass
```

Tạo file `base_datastore.py` để định nghĩa class nền cho các kho dữ liệu.