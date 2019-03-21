## ETF爬蟲 教學文件

1. 我們選擇用Selenium套件爬蟲，因為它可以模擬人類做滾動網頁和點擊操作。
  
  
  
2. 流程圖  
     
     ![image](https://github.com/jeffrey1227/Fintech-Text-Mining-and-Machine-Learning/blob/master/img/workflow.jpg)
    
      
      
  
3. 
   - ```module not found```  
   套件未下載，由Terminal輸入```pip install [package name]```下載。  
   - ```FileNotFoundError: File b'../Municipal Bond ETF List (29).csv' does not exist```  
   Excel檔案路徑錯誤，此為將```.csv```檔放在```.ipynb```檔上一層路徑的寫法。  
   - ```FileNotFoundError: [Errno 2] No such file or directory: '/Users/lou_tun_chieh/Desktop/webdriver/chromedriver': '/Users/lou_tun_chieh/Desktop/webdriver/chromedriver'```  
   Chrome Driver放置位置錯誤與程式碼上的路徑不相符，且要注意web driver版本問題。  
   - Time.sleep等待時間要看網速，網路不夠好等待的時間又太短，爬蟲的內容容易有錯，要自己拿捏。
   - 在Yahoo!Finance爬資料時，```request.get()```時需傳遞cookie，這個cookie是main driver在取得下載資料的網址時一起取得的，不是對下載資料的網址使用```request.get()```再取得的cookie，後者的做法會發生```http 401 error```。

