import streamlit as st
import pandas as pd
from scrapling import Fetcher

st.set_page_config(page_title="Công cụ Tìm Khách Hàng", layout="wide")

st.title("🔎 Trình Quét Dữ Liệu Khách Hàng")
st.write("Nhập địa chỉ trang web và thông tin cần lấy bên dưới.")

# Cấu hình bên trái màn hình
with st.sidebar:
    st.header("Cài đặt")
    url = st.text_input("1. Nhập Link trang web:")
    container = st.text_input("2. Mã vùng chứa (Container):", value=".business-card")
    name_tag = st.text_input("3. Mã tên khách hàng:", value="h2")
    phone_tag = st.text_input("4. Mã số điện thoại:", value=".phone")
    submit = st.button("Bắt đầu quét dữ liệu")

# Xử lý khi nhấn nút
if submit and url:
    with st.spinner("Đang lấy dữ liệu, vui lòng đợi..."):
        try:
            fetcher = Fetcher()
            page = fetcher.get(url)
            items = page.css(container)
            
            results = []
            for item in items:
                name = item.css_first(name_tag).text.strip() if item.css_first(name_tag) else "Không tìm thấy"
                phone = item.css_first(phone_tag).text.strip() if item.css_first(phone_tag) else "Không tìm thấy"
                results.append({"Tên": name, "Liên hệ": phone})
            
            if results:
                df = pd.DataFrame(results)
                st.success(f"Tìm thấy {len(results)} kết quả!")
                st.table(df) # Hiển thị kết quả ra bảng
                
                # Nút tải về máy
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Tải file Excel (CSV) về máy", data=csv, file_name="khach_hang.csv")
            else:
                st.warning("Không tìm thấy dữ liệu. Hãy kiểm tra lại các mã ở bước 2, 3, 4.")
        except Exception as e:
            st.error(f"Lỗi rồi: {e}")
