import streamlit as st
import pandas as pd
import httpx
from selectolax.lexbor import LexborHTMLParser

# Cấu hình giao diện
st.set_page_config(page_title="Leads Finder Pro", layout="wide")

def scrape_data(url, container_sel, name_sel, phone_sel):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Gửi yêu cầu tải trang
        with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            
        # Phân tích cú pháp HTML
        parser = LexborHTMLParser(resp.text)
        results = []
        
        # Tìm các khối dữ liệu
        for node in parser.css(container_sel):
            name_node = node.css_first(name_sel)
            phone_node = node.css_first(phone_sel)
            
            results.append({
                "Tên khách hàng": name_node.text().strip() if name_node else "N/A",
                "Liên hệ": phone_node.text().strip() if phone_node else "N/A"
            })
        return results
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
        return None

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.title("🚀 Hệ Thống Trích Xuất Khách Hàng")
st.markdown("---")

with st.sidebar:
    st.header("Cấu hình mục tiêu")
    target_url = st.text_input("Địa chỉ website (URL):", placeholder="https://example.com")
    c_tag = st.text_input("Mã vùng chứa (Container):", value=".item")
    n_tag = st.text_input("Mã tên khách hàng:", value="h3")
    p_tag = st.text_input("Mã số điện thoại:", value=".phone")
    submit = st.button("QUÉT DỮ LIỆU", use_container_width=True)

if submit:
    if not target_url:
        st.warning("Vui lòng nhập URL!")
    else:
        with st.spinner("Đang thực hiện trích xuất dữ liệu nâng cao..."):
            data = scrape_data(target_url, c_tag, n_tag, p_tag)
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"Hoàn thành! Tìm thấy {len(data)} khách hàng.")
                st.dataframe(df, use_container_width=True)
                
                # Xuất dữ liệu
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="TẢI FILE KẾT QUẢ (CSV)",
                    data=csv,
                    file_name="results.csv",
                    mime="text/csv"
                )
            else:
                st.error("Không có dữ liệu được tìm thấy. Hãy kiểm tra lại các mã định danh HTML.")
