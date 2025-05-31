// import { checkSignin } from "./dashboard.js";
import { userNameP, funcNavUl } from "./variables.js";

async function checkSignin() {
  const token = localStorage.getItem("access_token");

  if (token) {
    const response = await fetch("/api/user/auth", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const result = await response.json();
    const userData = result.data;

    if (userData) {
      const userName = userData.name;
      userNameP.textContent = `Hi ${userName}`;
      //   userNameStrong.textContent = `${userName}`;

      let funcNavUlLi = document.createElement("li");
      funcNavUlLi.className = "function_nav_ul_li";

      console.log(userData.position);

      let funcNavUlLiA = document.createElement("a");
      funcNavUlLiA.textContent = `${userData.position} 維護`;

      if (userData.position === "IE") {
        // 這邊放IE維護
        console.log("放IE維護");
        funcNavUlLiA.href = "/iemaintain";
      } else if (userData.position === "MFG") {
        // 這邊放MFG維護
        funcNavUlLiA.href = "/mfgmaintain";
      } else {
        // 這邊放EQ維護
        funcNavUlLiA.href = "/eqmaintain";
      }

      funcNavUlLi.appendChild(funcNavUlLiA);
      funcNavUl.appendChild(funcNavUlLi);
    }
  } else {
    window.alert("請先登入");
    window.location.href = "/";
  }
}

async function main() {
  await checkSignin();
  // document.getElementById("eq_gantt_chart_img").src = "/api/chart/eqganttchart";
}

main();

document.addEventListener("DOMContentLoaded", function () {
  const imgElement = document.getElementById("eq_gantt_chart_img");
  const loadingMessage = document.getElementById("loading_message");
  const container = document.getElementById("eq_gantt_chart_fig");

  // 假設你圖片的實際 URL 會被設定到 src
  imgElement.src = "/api/chart/eqganttchart"; // 替換成你的圖片 URL

  imgElement.onload = function () {
    // 圖片載入完成後
    loadingMessage.style.display = "none"; // 隱藏載入訊息
    imgElement.style.display = "block"; // 顯示圖片
    container.style.background = "none"; // 移除背景色
    container.style.border = "none"; // 移除邊框
    container.style.minHeight = "auto"; // 恢復高度
  };

  imgElement.onerror = function () {
    // 圖片載入失敗時
    loadingMessage.textContent = "甘特圖載入失敗，請稍後再試。";
    loadingMessage.style.color = "red";
    container.style.background = "#ffe0e0"; // 顯示錯誤背景
  };
});
