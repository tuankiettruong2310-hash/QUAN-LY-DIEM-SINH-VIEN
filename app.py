import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 1. Hiển thị tiêu đề Web App bằng Streamlit
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Khởi tạo dữ liệu
data = {
    "Họ và tên": [
        "Nguyễn Văn An",
        "Trần Thị Bích",
        "Lê Hoàng Cường",
        "Phạm Minh Đức",
        "Hoàng Thị Giang",
        "Vũ Hải Đăng",
        "Đặng Thu Thảo",
        "Bùi Anh Tuấn",
        "Đỗ Khánh Linh",
        "Ngoại Quốc Hùng",],
    "Điểm chuyên cần": [9.0, 8.5, 7.0, 10.0, 6.5, 8.0, 9.5, 7.5, 9.0, 8.0],
    "Điểm giữa kỳ": [7.5, 8.0, 6.0, 9.0, 5.5, 7.0, 8.5, 6.5, 9.5, 7.0],
    "Điểm cuối kỳ": [8.0, 8.5, 6.5, 9.5, 6.0, 7.5, 9.0, 7.0, 9.0, 8.0],}

# 1. Tạo DataFrame
df = pd.DataFrame(data)

# 2. Tính điểm tổng kết
# Công thức: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
df["Tổng Kết"] = (0.2 * df["Điểm chuyên cần"] + 0.3 * df["Điểm giữa kỳ"]
                         + 0.5 * df["Điểm cuối kỳ"])
# Làm tròn điểm tổng kết đến 2 chữ số thập phân (nếu cần)
df["Tổng Kết"] = df["Tổng Kết"].round(2)

# 3. Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

# Tạo cột Xếp Loại bằng hàm apply
df["Xếp Loại"] = df["Tổng Kết"].apply(xep_loai)

# Hiển thị toàn bộ bảng dữ liệu hoàn chỉnh lên Web
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Thống kê
# Điểm tổng kết trung bình của lớp
dtb_lop = df["Tổng Kết"].mean().round(2)

# Sinh viên có điểm tổng kết cao nhất
idx_max = df["Tổng Kết"].idxmax()
sv_cao_nhat = df.loc[idx_max, "Họ và tên"]
diem_cao_nhat = df.loc[idx_max, "Tổng Kết"]

# Sinh viên có điểm tổng kết thấp nhất
idx_min = df["Tổng Kết"].idxmin()
sv_thap_nhat = df.loc[idx_min, "Họ và tên"]
diem_thap_nhat = df.loc[idx_min, "Tổng Kết"]

# Đếm số sinh viên đạt (điểm tổng kết >= 5.0)
so_sv_dat = (df["Tổng Kết"] >= 5.0).sum()

# Kết quả thống kê (Đã sửa từ print() sang st.write() để hiện lên Web)
st.subheader("📊 THỐNG KÊ")
st.write(f"1. **Điểm tổng kết trung bình của lớp:** {dtb_lop:.2f}")
st.write(f"2. **Sinh viên có điểm tổng kết cao nhất:** {sv_cao_nhat} ({diem_cao_nhat} điểm)")
st.write(f"3. **Sinh viên có điểm tổng kết thấp nhất:** {sv_thap_nhat} ({diem_thap_nhat} điểm)")
st.write(f"4. **Số sinh viên đạt:** {so_sv_dat}/{len(df)} sinh viên")

# 5. Tra cứu sinh viên bằng Selectbox
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn sinh viên:", df["Họ và tên"].tolist())
sv_info = df[df["Họ và tên"] == selected_student].iloc[0]
st.write(f"- Điểm chuyên cần: **{sv_info['Điểm chuyên cần']}**")
st.write(f"- Điểm giữa kỳ: **{sv_info['Điểm giữa kỳ']}**")
st.write(f"- Điểm cuối kỳ: **{sv_info['Điểm cuối kỳ']}**")
st.write(f"- Điểm tổng kết: **{sv_info['Tổng Kết']}**")
st.write(f"- Xếp loại: **{sv_info['Xếp Loại']}**")

# 6. Vẽ biểu đồ
st.subheader("📈 Biểu đồ điểm")
sinh_vien = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Hoàng Cường", 
    "Phạm Minh Đức", "Hoàng Thị Giang", "Vũ Hải Đăng", 
    "Đặng Thu Thảo", "Bùi Anh Tuấn", "Đỗ Khánh Linh", "Ngoại Quốc Hùng"]
diem_tong_ket = [8.05, 8.35, 6.45, 9.45, 5.95, 7.45, 8.95, 6.95, 9.15, 7.70]

# Đảo ngược danh sách để người đầu tiên (Nguyễn Văn An) nằm ở trên cùng biểu đồ
sinh_vien.reverse()
diem_tong_ket.reverse()

# Khởi tạo kích thước biểu đồ
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ cột ngang
bars = plt.barh(sinh_vien, diem_tong_ket, color='#5DADE2', height=0.6)

# Hiển thị số điểm cụ thể ngay trên mỗi cột để dễ nhìn
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
             va='center', ha='left', fontsize=10, fontweight='bold', color='#333333')

# Thêm tiêu đề và tên các trục bằng tiếng Việt
plt.title('Biểu đồ điểm tổng kết của 10 sinh viên', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Điểm số tổng kết', fontsize=12, labelpad=10)
plt.ylabel('Họ và tên sinh viên', fontsize=12, labelpad=10)

# Giới hạn trục X từ 0 đến 11
plt.xlim(0, 11)
plt.xticks([0, 2.5, 5, 7.5, 10])

# Tinh chỉnh giao diện phẳng, hiện đại và sạch sẽ
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

plt.tight_layout()

# Lệnh hiển thị biểu đồ Matplotlib lên Streamlit (Đã sửa từ plt.show() sang st.pyplot())
st.pyplot(plt.gcf())

# 7. Họ tên & MSSV người tạo (chữ nhỏ ở cuối trang)
st.caption("Họ tên: **[Nguyễn Thị Tình]** - MSSV: **[038308019012]**")
