# 影像增強 #
- 實作各種 filter
  - 將圖片轉灰階 (option, 可用RGB版本，但要額外處理channel)
  - 做二階 filter 找高低頻
  - 做一階 filter 找邊緣
  - 做 sobel filter 找方向
  - 用 mean filter 模糊圖片去除高斯雜訊
- 依說明文件將中間產出圖片合併，便可得到增強後的影像

> 原始圖片若太過銳利，效果會不明顯
