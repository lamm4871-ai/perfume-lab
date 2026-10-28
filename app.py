import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from google import genai
from google.genai import types
@st.cache_resource
def tao_gemini():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

st.set_page_config(page_title="Perfume Lab", page_icon="🌸")
gemini = tao_gemini()

st.title("🌸 PERFUME LAB")
st.write("Ứng dụng thiết kế nước hoa cá nhân hóa")
st.write("Dự án nghiên cứu nước hoa mùa hè")

st.divider()

st.header("1. Sản phẩm của nhóm")

st.success("Mẫu B - Sản phẩm chính của nhóm!")

st.write("Công thức thực nghiệm mẫu B (thể tích mục tiêu 20 ml):")

st.table({
    "Nguyên liệu": [
        "Tinh dầu chanh",
        "Tinh dầu bạc hà",
        "Tinh dầu cỏ hương bài",
        "Ethanol 90°",
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

st.caption("Theo phép đo thực tế của nhóm: 1 giọt ≈ 0.04 ml.")

st.info(
    "Mẫu B được chọn làm sản phẩm chính vì có sự cân bằng "
    "giữa hương chanh tươi mát, bạc hà sảng khoái "
    "và cỏ hương bài tạo chiều sâu."
)
st.divider()

st.subheader("🧪 So sánh các mẫu nước hoa")

st.table({
    "Mẫu thử": [
        "Mẫu thử 1",
        "Mẫu thử 2",
        "Mẫu B",
        "Mẫu C"
    ],
    "Kết quả": [
        "Chưa thành công",
        "Thành công",
        "Thành công - được chọn",
        "Thành công"
    ],
    "Nhận xét": [
        "Hương cỏ hương bài quá nồng",
        "Hương giữa chưa nổi bật",
        "Ba tầng hương cân bằng",
        "Hương chanh hơi lấn át"
    ]
})

st.success("🌸 Mẫu B được chọn làm sản phẩm chính của nhóm.")

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

st.subheader("Thiết kế công thức lý thuyết - 3 tầng hương")

chanh = st.slider("🍋 Hương đầu - Chanh (%)", 0.0, 10.0, 3.0, 0.05)
bac_ha = st.slider("🌿 Hương giữa - Bạc hà (%)", 0.0, 10.0, 1.8, 0.05)
vetiver = st.slider("🌳 Hương cuối - Cỏ hương bài (%)", 0.0, 10.0, 1.2, 0.05)

tong_tinh_dau = chanh + bac_ha + vetiver

st.write(f"Tổng tinh dầu: {tong_tinh_dau:.2f}%")

if tong_tinh_dau > 6:
    st.error("Tổng tinh dầu vượt mức 6% của công thức lý thuyết!")
else:
    st.success("Tổng tinh dầu không vượt mức tham chiếu 6%.")

st.divider()

st.header("3. Kết quả tính toán")

nuoc_cat = 1.0
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


st.divider()
st.header("7. 🌸 Trợ lý nước hoa PERFUME LAB")

che_do = st.radio(
    "Bạn muốn tương tác bằng cách nào?",
    ["💬 Chat", "🎙️ Voice"],
    horizontal=True
)

if che_do == "💬 Chat":
    st.subheader("💬 Chat với trợ lý nước hoa")

    cau_hoi = st.chat_input("Hỏi tui về nước hoa nha...")

    if cau_hoi:
        st.chat_message("user").write(cau_hoi)
        try:
            phan_hoi = gemini.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=cau_hoi,
                config=types.GenerateContentConfig(
                                         
                    system_instruction=(
                        "Bạn là trợ lý PERFUME LAB. "
                        "Hãy tư vấn kiến thức nước hoa bằng tiếng Việt, "
                        "thân thiện, dễ hiểu và ngắn gọn. "
                        "Giải thích về hương chanh, bạc hà, cỏ hương bài "
                        "và cách lựa chọn mùi hương. "
                    "Dữ liệu thí nghiệm của nhóm PERFUME LAB: "
                        "Mẫu thử 1 chưa thành công vì cỏ hương bài quá nồng. "
                        "Mẫu thử 2 thành công nhưng hương giữa chưa nổi bật. "
                        "Mẫu B được chọn làm sản phẩm chính vì ba tầng hương cân bằng. "
                        "Mẫu C có hương chanh hơi lấn át. "
                        "Công thức lý thuyết mẫu B gồm 3% chanh, "
                        "1.8% bạc hà, 1.2% cỏ hương bài, "
                        "93% ethanol và 1% nước cất. "
                        "Phân biệt công thức lý thuyết với số liệu pha thực tế. "
                        "Không tự khẳng định công thức pha chế an toàn "
                        "nếu chưa có dữ liệu kiểm định."
                    )
                )
            )

            tra_loi = phan_hoi.text
            st.chat_message("assistant").write(tra_loi)

        except Exception as e:
            st.error(f"Không kết nối được Gemini: {e}")

else:
    st.subheader("🎙️ Trò chuyện bằng giọng nói")
    
    ghi_am = st.audio_input("🎤 Nhấn để nói chuyện")

    if ghi_am is not None:
        st.audio(ghi_am)

        try:
            nhan_dien = sr.Recognizer()

            am_thanh = sr.AudioFile(ghi_am)
            with am_thanh as nguon:
                du_lieu = nhan_dien.record(nguon)

            cau_noi = nhan_dien.recognize_google(
                du_lieu,
                language="vi-VN"
            )

            st.success("🎤 Bạn vừa nói:")
            st.write(cau_noi)

            phan_hoi = gemini.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=cau_noi,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Bạn là trợ lý nước hoa PERFUME LAB. "
                        "Hãy trả lời bằng tiếng Việt, thân thiện, "
                        "ngắn gọn, dễ hiểu, phù hợp để đọc thành tiếng. "
                    "Dữ liệu thí nghiệm của nhóm PERFUME LAB: "
                        "Mẫu thử 1 chưa thành công vì cỏ hương bài quá nồng. "
                        "Mẫu thử 2 thành công nhưng hương giữa chưa nổi bật. "
                        "Mẫu B được chọn làm sản phẩm chính vì ba tầng hương cân bằng. "
                        "Mẫu C có hương chanh hơi lấn át. "
                        "Công thức lý thuyết mẫu B gồm 3% chanh, "
                        "1.8% bạc hà, 1.2% cỏ hương bài, "
                        "93% ethanol và 1% nước cất. "
                        "Phân biệt công thức lý thuyết với số liệu pha thực tế. "
                        "Không khẳng định công thức pha chế an toàn "
                        "nếu chưa có dữ liệu kiểm định."
                    )
                )
            )
            tra_loi = phan_hoi.text
            st.write("🤖 Trợ lý:", tra_loi)
            try:
                giong_noi = gTTS(text=tra_loi, lang="vi")

                am_thanh_mp3 = BytesIO()
                giong_noi.write_to_fp(am_thanh_mp3)
                am_thanh_mp3.seek(0)

                st.audio(am_thanh_mp3, format="audio/mp3")

            except Exception as e:
                st.warning(f"Không tạo được giọng nói: {e}")

        except sr.UnknownValueError:
            st.warning("Không nghe rõ. Bạn thử nói lại nha!")

        except sr.RequestError:
            st.error("Không kết nối được dịch vụ nhận diện giọng nói.")

        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")