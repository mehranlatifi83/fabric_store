function openTab(tabName) {
    // پنهان کردن تمام محتواهای تب
    var tabcontent = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    // نمایش محتوای تب انتخاب شده
    document.getElementById(tabName).style.display = "block";
  }
  
  // نمایش تب کاربرها به صورت پیش‌فرض هنگام بارگذاری صفحه
  document.addEventListener("DOMContentLoaded", function() {
    openTab('Users');
  });
  