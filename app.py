import streamlit as st

st.set_page_config(page_title="Perfume Lab", page_icon="🌸")

st.title("🌸 PERFUME LAB")
st.write("Ứng dụng thiết kế nước hoa cá nhân hóa")
st.write("Dự án nghiên cứu nước hoa mùa hè")

st.divider()

st.header("1. Sản phẩm của nhóm")

st.success("Mẫu B - Sản phẩm đã pha chế thành công!")

st.write("Công thức thực hành của nhóm:")

st.table({
    "Nguyên liệu": [
        "Tinh dầu chanh",
        "Tinh dầu bạc hà",
        "Tinh dầu cỏ hương bài",
        "Ethanol",
        "Nước cất"
    ],
    "Lượng sử dụng": [
        "7 giọt",
        "5 giọt",
        "3 giọt",
        "18.6 ml",
        "3 giọt"
    ]
})

st.caption("Theo phép đo của nhóm: 1 giọt ≈ 0.04 ml.")

st.divider()

st.header("2. Cá nhân hóa nước hoa")

mua = st.selectbox(
    "Chọn mùa sử dụng",
    ["Xuân", "Hạ", "Thu", "Đông"]
)
if mua == "Xuân":
    st.info("🌸 Mùa Xuân: Gợi ý hương hoa và cam chanh nhẹ nhàng.")
elif mua == "Hạ":
    st.info("☀️ Mùa Hạ: Gợi ý tăng cảm giác tươi mát với chanh và bạc hà.")
elif mua == "Thu":
    st.info("🍂 Mùa Thu: Gợi ý mùi hương dịu nhẹ, cân bằng.")
else:
    st.info("❄️ Mùa Đông: Gợi ý mùi hương ấm, sâu với cỏ hương bài.")

the_tich = st.number_input(
    "Nhập thể tích mong muốn (ml)",
    min_value=1.0,
    max_value=100.0,
    value=20.0
)

st.subheader("Điều chỉnh 3 tầng hương")

chanh = st.slider("🍋 Hương đầu - Chanh (%)", 0.0, 10.0, 1.45, 0.05)
bac_ha = st.slider("🌿 Hương giữa - Bạc hà (%)", 0.0, 10.0, 1.05, 0.05)
vetiver = st.slider("🌳 Hương cuối - Cỏ hương bài (%)", 0.0, 10.0, 0.60, 0.05)

tong_tinh_dau = chanh + bac_ha + vetiver

st.write(f"Tổng tinh dầu: {tong_tinh_dau:.2f}%")

if tong_tinh_dau > 6:
    st.error("Tổng tinh dầu vượt mức 6% của công thức lý thuyết!")
else:
    st.success("Tổng tinh dầu không vượt mức tham chiếu 6%.")

st.divider()

st.header("3. Kết quả tính toán")

nuoc_cat = 0.60
ethanol = 100 - tong_tinh_dau - nuoc_cat

ket_qua = {
    "Nguyên liệu": [
        "Tinh dầu chanh",
        "Tinh dầu bạc hà",
        "Tinh dầu cỏ hương bài",
        "Ethanol",
        "Nước cất"
    ],
    "Thể tích (ml)": [
        round(the_tich * chanh / 100, 3),
        round(the_tich * bac_ha / 100, 3),
        round(the_tich * vetiver / 100, 3),
        round(the_tich * ethanol / 100, 3),
        round(the_tich * nuoc_cat / 100, 3)
    ]
}

st.table(ket_qua)

st.info("Đây là công cụ tính toán phục vụ học tập, không xác nhận công thức an toàn để sử dụng trên da.")
import csv
import io

st.header("4. Xuất công thức nước hoa")

output = io.StringIO()
writer = csv.writer(output)

writer.writerow(["Nguyen lieu", "The tich (ml)"])

for ten, ml in zip(
    ket_qua["Nguyên liệu"],
    ket_qua["Thể tích (ml)"]
):
    writer.writerow([ten, ml])

csv_data = output.getvalue().encode("utf-8-sig")

st.download_button(
    label="📥 Tải công thức CSV",
    data=csv_data,
    file_name="cong_thuc_nuoc_hoa.csv",
    mime="text/csv"
)
st.divider()

st.header("5. Kiểm tra công thức")

tong_cong = chanh + bac_ha + vetiver + ethanol + nuoc_cat

st.write(f"Tổng tỉ lệ nguyên liệu: {tong_cong:.2f}%")

if abs(tong_cong - 100) < 0.01:
    st.success("Tổng tỉ lệ bằng 100%.")
else:
    st.error("Tổng tỉ lệ không bằng 100%!")

if tong_tinh_dau > 6:
    st.warning("Tổng tinh dầu vượt mức tham chiếu 6% của nhóm.")

st.caption(
    "Tổng bằng 100% không đồng nghĩa công thức an toàn. "
    "Cần giáo viên kiểm tra giới hạn sử dụng của từng nguyên liệu."
)

st.divider()

st.header("6. Hồ sơ mùi hương")

if chanh >= bac_ha and chanh >= vetiver:
    st.info("🍋 Hương chanh chiếm ưu thế: định hướng tươi mát.")
elif bac_ha >= chanh and bac_ha >= vetiver:
    st.info("🌿 Hương bạc hà chiếm ưu thế: định hướng thảo mộc.")
else:
    st.info("🌳 Hương cỏ hương bài chiếm ưu thế: định hướng mùi gỗ.")

st.write("Tỉ lệ các tầng hương trong hệ tinh dầu:")

if tong_tinh_dau > 0:
    st.write(f"Hương đầu: {chanh / tong_tinh_dau * 100:.1f}%")
    st.write(f"Hương giữa: {bac_ha / tong_tinh_dau * 100:.1f}%")
    st.write(f"Hương cuối: {vetiver / tong_tinh_dau * 100:.1f}%")
else:
    st.warning("Chưa có tinh dầu để phân tích tầng hương.")

st.caption(
    "Hồ sơ mùi chỉ là mô tả dự kiến dựa trên tỉ lệ, "
    "không thay thế kết quả thử mùi thực tế."
)
