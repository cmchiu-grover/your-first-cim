// import { checkSignin } from "./dashboard.js";
import { userNameP, funcNavUl } from "./variables.js";
import { signout } from "./user.js";

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
signout();

document.addEventListener("DOMContentLoaded", async function () {
  const imgElement = document.getElementById("eq_gantt_chart_img");
  const loadingMessage = document.getElementById("loading_message");
  const container = document.getElementById("eq_gantt_chart_fig");
  const queryGanttForm = document.getElementById("gantt-chart-query-form");
  const queryButton = document.getElementById("query-gantt-button");

  try {
    const response = await fetch("/api/chart/ganttchart/yesterday", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log("查詢結果:", data);
    const yesterdaySrc = data.url;

    imgElement.src = yesterdaySrc;

    // console.log(imgElement.src);
  } catch (error) {
    console.error("查詢失敗:", error);

    window.alert(`查詢失敗: ${error.message}`);
  }

  queryGanttForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    queryButton.disabled = true;
    queryButton.textContent = "查詢中...";

    const formData = new FormData(queryGanttForm);
    const queryParams = new URLSearchParams();
    console.log("表單數據:", Object.fromEntries(formData.entries()));
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/chart/ganttchart";
    const fullUrl = `${apiUrl}?${queryParams.toString()}`;

    console.log("查詢 URL:", fullUrl);

    try {
      const response = await fetch(fullUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      console.log("查詢結果:", data);

      imgElement.src = `${data.url}`;

      console.log(imgElement.src);

      imgElement.onerror = function () {
        // 圖片載入失敗時
        loadingMessage.textContent = "甘特圖載入失敗，請稍後再試。";
        loadingMessage.style.color = "red";
        container.style.background = "#ffe0e0"; // 顯示錯誤背景
      };
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryButton.disabled = false; // 啟用按鈕
      queryButton.textContent = "查詢";
    }
  });
});
