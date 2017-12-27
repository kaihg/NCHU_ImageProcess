# 尋找直線 #

1. 從原圖找出邊緣
  - 可用 Sobel filter or Canny
  - 此次使用 PIL 內建的 FIND_EDGE 功能
2. 設定下限值，去除不夠明顯的線條(視為雜訊)
3. 對所有點找 Hough Transform 的結果
  - Hough Transform : x * cos(θ) + y * sin(θ) = p
  - 實作時，對 (x,y) = (x0, y0)，給予 [-π , π] 的值 (1000等分)，得到 p
  - 所以最後會得到一個三維陣列 (x0,y0) = [ all p for [-π , π] ]
4. 在 θp 空間內，累計每一個 block 內通過的數量
5. 產生 hough tranform 的圖片，其 x y 軸要先轉換到 N
  - pixel 亮度 = 累計數量 / total * 255 : 正規化到 0 ~ 255
  - 可以考慮增加中間值域的亮度 (未實作)，看起來會比較明顯
6. 找出最多線通過的 block，並找出是哪些線
7. 在原圖上畫出上述找出的原點，將其連線，得到結果圖
