# Smartphone Usage Dashboard

## จัดทำโดย
- ชื่อ: นายพลกฤต บัวลอย
- รหัสนักศึกษา: 6810110223

---

แดชบอร์ดสำหรับวิเคราะห์พฤติกรรมการใช้งานสมาร์ตโฟนและความสัมพันธ์กับตัวชี้วัดด้านการทำงาน/สุขภาพ เช่น
- ชั่วโมงการใช้งานโทรศัพท์ต่อวัน
- ชั่วโมงโซเชียลมีเดีย
- คะแนนประสิทธิภาพการทำงาน
- ชั่วโมงการนอน
- ระดับความเครียด

แอปพัฒนาด้วย **Dash + Plotly** และมีตารางข้อมูลแบบโต้ตอบด้วย **Dash AG Grid**

---

## โครงสร้างโปรเจกต์

```text
Dashboard/
├─ app.py
├─ data.ipynb
├─ README.md
└─ Dataset/
	└─ Smartphone_Usage_Productivity_Dataset_50000.csv
```

---

## ความสามารถหลัก

1. เลือกการจัดกลุ่มข้อมูล (Data Group)
	- Age Group
	- Gender
	- Occupation

2. เลือกตัวชี้วัด (Statistic)
	- Daily Phone Hours
	- Social Media Hours
	- Productivity Score
	- Sleep Hours
	- Stress Level
	- Caffeine Intake
	- Weekend Phone Hours

3. แสดงผลกราฟแบบโต้ตอบ 3 รูปแบบ
	- Bar Chart (ค่าเฉลี่ยตามกลุ่ม)
	- Pie Chart (สัดส่วนการกระจาย)
	- Box Plot (การกระจายค่าและ outliers)

4. ตารางข้อมูลทั้งหมดด้านล่าง

---

## วิธีติดตั้ง

> แนะนำให้ใช้ Python 3.10 ขึ้นไป

1. Install

```bash
# สร้างสภาพแวดล้อมเสมือน
python -m venv .venv
# เปิดใช้งานสภาพแวดล้อมเสมือน
.venv\Scripts\activate
# ติดตั้งแพ็คเกจที่ต้องการ
pip install dash-ag-grid dash pandas plotly statsmodels
```

---

2. วิธีรันโปรเจกต์

```bash
python app.py
```

เมื่อรันสำเร็จ ให้เปิดเบราว์เซอร์ที่ URL:

```text
http://127.0.0.1:8050/
```

---

## ข้อมูลที่ใช้

- ไฟล์ข้อมูล: `Dataset/Smartphone_Usage_Productivity_Dataset_50000.csv`
- จำนวนข้อมูล: 50,000 แถว

มีการสร้างคอลัมน์ `Age_Group` เพิ่มจากคอลัมน์ `Age` เพื่อใช้จัดกลุ่มอายุเป็นช่วง:
- `<20`
- `21-30`
- `31-40`
- `41-50`
- `>50`

---
