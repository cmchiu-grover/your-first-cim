// static/js/sse.js

document.addEventListener("DOMContentLoaded", () => {
  const updateDot = document.querySelector("#updateDot");
  if (!updateDot) return; // 若此頁沒有紅點就略過

  const sse = new EventSource("/sse/standard_time");

  sse.onmessage = function (event) {
    console.log("收到 SSE 更新：", event.data);
    updateDot.style.display = "flex";
  };

  // 點擊鈴鐺清除紅點 (簡單示意)
  document.getElementById("notifications").addEventListener("click", () => {
    updateDot.style.display = "none";
    // 在實際應用中，這裡可能還需要標記通知為已讀等操作
  });

  sse.onerror = function () {
    console.error("SSE 連線錯誤，將重試...");
  };
});
