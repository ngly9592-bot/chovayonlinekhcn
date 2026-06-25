import streamlit as st

# Cấu hình trang web
st.set_page_config(page_title="Công cụ Đánh giá Khoản Vay", layout="centered")

st.title("🏦 ỨNG DỤNG ĐÁNH GIÁ KHOẢN VAY")
st.write("Nhập các thông tin dưới đây để kiểm tra điều kiện vay vốn.")
st.markdown("---")

# --- KHU VỰC NHẬP DỮ LIỆU ---
st.header("📋 Thông tin khách hàng & Khoản vay")

col1, col2 = st.columns(2)

with col1:
    STV = st.number_input("Số tiền muốn vay (Triệu đồng):", min_value=0.0, value=500.0, step=10.0)
    TGV = st.number_input("Thời gian vay (Số năm):", min_value=0.5, value=5.0, step=0.5)
    # Thay vì bắt nhập thập phân khó hiểu, dùng % cho thân thiện rồi chia 100 ở background
    LSV_percentage = st.number_input("Lãi suất cho vay (%/năm):", min_value=0.0, value=8.5, step=0.1)
    LSV = LSV_percentage / 100
    STKH = st.number_input("Tuổi của khách hàng (Tuổi):", min_value=0, max_value=100, value=30)

with col2:
    TN = st.number_input("Thu nhập hàng tháng (Triệu đồng/tháng):", min_value=0.0, value=30.0, step=1.0)
    SNTGD = st.number_input("Số người trong gia đình (Người):", min_value=1, value=4, step=1)
    PTMC = st.number_input("Số tiền phải trả cho khoản vay cũ (Triệu đồng):", min_value=0.0, value=0.0, step=0.5)
    GTTSDB = st.number_input("Giá trị tài sản đảm bảo (Triệu đồng):", min_value=1.0, value=1000.0, step=10.0)

CPSH = 5  # Chi phí sinh hoạt mặc định

st.markdown("---")

# --- KHU VỰC TÍNH TOÁN ---
if st.button("📊 Kiểm tra kết quả", type="primary"):
    
    # Tính toán các chỉ số
    PTMM = (STV / (TGV * 12)) + (STV * (LSV / 12))
    
    # Tránh lỗi chia cho 0 hoặc thu nhập ròng âm
    thu_nhap_rong = TN - (SNTGD * CPSH)
    if thu_nhap_rong <= 0:
        st.error("🚨 Thu nhập hàng tháng không đủ bù đắp chi phí sinh hoạt tối thiểu của gia đình!")
    else:
        DTI = (PTMC + PTMM) / thu_nhap_rong
        LTV = STV / GTTSDB

        # Hiển thị kết quả chỉ số
        st.subheader("📈 Kết quả phân tích chỉ số")
        
        c1, c2 = st.columns(2)
        c1.metric(label="Chỉ số DTI (Nợ / Thu nhập)", value=f"{DTI * 100:.2f} %")
        c2.metric(label="Chỉ số LTV (Vay / Tài sản đảm bảo)", value=f"{LTV * 100:.2f} %")
        
        st.write(f"**Tuổi khách hàng:** {STKH} tuổi")
        
        st.markdown("---")
        
        # Kiểm tra điều kiện cho vay
        st.subheader("📢 Quyết định")
        if DTI <= 0.7 and LTV <= 0.7 and 18 <= STKH <= 70:
            st.success("✅ **ĐƯỢC CHO VAY**")
            st.balloons()  # Hiệu ứng bong bóng chúc mừng
        else:
            st.error("❌ **KHÔNG ĐƯỢC CHO VAY**")
            
            # Gợi ý lý do từ chối
            st.write("**Lý do không đạt (nếu có):**")
            if DTI > 0.7:
                st.write("- Chỉ số DTI vượt quá giới hạn cho phép (> 70%)")
            if LTV > 0.7:
                st.write("- Chỉ số LTV vượt quá giới hạn cho phép (> 70%)")
            if not (18 <= STKH <= 70):
                st.write("- Độ tuổi khách hàng không nằm trong độ tuổi quy định (18 - 70 tuổi)")
