import streamlit as st
import pandas as pd
from scrapling import Fetcher

# Cấu hình giao diện
st.set_page_config(page_title="Leads Finder", layout="wide")

def run_scraper(target_url, container, name_sel, phone_sel):
    # Sử dụng network_lib='curl_cffi' để không cần cài đặt Playwright phức tạp trên Cloud
    fetcher = Fetcher(network_lib='curl_cffi')
    try:
        page = fetcher.get(target_url)
        # Sử dụng cấu trúc lọc dữ liệu an toàn
        items = page.css(container)
        data = []
        
        for item in items:
            name = item.css_first(name_sel).text.strip() if item.css_first(name_sel) else "N/A"
            phone = item.css_first(phone_sel).text.strip() if item.css_first(phone_sel) else "N/A"
            data.append({"Tên": name, "Liên hệ": phone})
            
        return data
    except Exception as e:
        st.error(f"Lỗi truy cập: {str(e)}")
        return None

# --- UI ---
st.title("🚀 Công cụ Tìm Kiếm Khách Hàng")

col1, col2 = st.columns([1, 2])

with col1:
    url = st.text_input("Link website mục tiêu:")
    c_tag = st.text_input("Mã vùng chứa (Container):", ".business-card")
    n_tag = st.text_input("Mã Tên:", "h2")
    p_tag = st.text_input("Mã SĐT:", ".phone")
    btn = st.button("Bắt đầu quét", use_container_width=True)

with col2:
    if btn and url:
        with st.spinner("Đang xử lý..."):
            results = run_scraper(url, c_tag, n_tag, p_tag)
            if results:
                df = pd.DataFrame(results)
                st.success(f"Tìm thấy {len(results)} kết quả!")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Tải file CSV", data=csv, file_name="leads.csv")
            else:
                st.warning("Không lấy được dữ liệu. Kiểm tra lại Link hoặc Mã định danh.")
