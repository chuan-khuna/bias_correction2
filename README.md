# Bias Correction v2

```
|- /observed_clean
|       |- TAVG.csv, TMAX.csv ....
|
|- /EC-EARTH
|       |- /hist, /rcp45, /rcp85
|
|- obs_station_rcm.csv
|
|- /BiasCorrectionLib
```

version ที่อ่านข้อมูลจาก nc file และ แก้ไขข้อมูลที่ nc file ได้

## Another Repository by Chuan

#### [BiasCorrectionLib](https://github.com/chuan-khuna/BiasCorrectionLib)

- ไลบรารี่ Bias correction อย่างง่ายที่เขียนเอง สำหรับใช้ใน Bias correction v2

#### [จัดข้อมูลให้อยู่ใน format ที่ต้องการ](https://github.com/chuan-khuna/curation_csv)

- จัดข้อมูลให้อยู่ใน format ตามความต้องการของ อ. แล้วก็ได้นำไปใช้ใน Bias Correction v2

#### [Qmap Bias correction](https://github.com/chuan-khuna/bias_correction_qmap)

- ใช้ Qmap (R Library) ในการทำ Bias Correction

#### [Bias Correction Climdex](https://github.com/chuan-khuna/bias_correction_and_climdex)

- ดูผลลัพธ์ของการทำ Bias correction ในด้านของการนำไปคำนวณ climdex ด้วย
- จัด format ข้อมูลเพื่อให้โปรแกรม Climpact ประมวลผลเป็น index ได้

### [flask-api](https://github.com/chuan-khuna/flask-api)

- web app back-end


### [txt_indices_to_nc](https://github.com/chuan-khuna/txt_indices_to_nc)

- แปลงข้อมูล index จาก text file ให้เป็น nc file

### [repository ตอนเริ่มต้นทำความเข้าใจข้อมูล climate](https://github.com/chuan-khuna/climate-simple-plot)

- repository ตอนเริ่มทำโปรเจคใหม่ๆ ทำความเข้าใจมุมมองต่างๆ ของ climate

### [my lib](https://github.com/chuan-khuna/myproject_lib)
- โค้ดที่ใช้ซ้ำๆ 
- พล็อตแมพด้วย matplotlib
- การ shift ข้อมูล
- การทำให้กริดหยาบมากขึ้น
