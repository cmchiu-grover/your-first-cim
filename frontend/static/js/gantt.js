import { signout } from "./user.js";
import { NotificationHandler } from "./notification.js";
import { checkUserData } from "./auth.js";
import { renderUserNav } from "./usernav.js";

async function setYesterdayDateText(elementId) {
  const now = new Date();
  const utc8Time = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  const yesterday = new Date(utc8Time);
  yesterday.setDate(yesterday.getDate() - 1);

  const yyyy = yesterday.getUTCFullYear();
  const mm = String(yesterday.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(yesterday.getUTCDate()).padStart(2, "0");
  const formattedDate = `${yyyy}/${mm}/${dd}`;

  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = `僅支持查詢 work_date：2025/06/01 ~ ${formattedDate}`;
  }
}

async function main() {
  const userData = await checkUserData();
  if (!userData) return;

  await renderUserNav(userData);
  await NotificationHandler.init({ withSSE: true });
  await setYesterdayDateText("dateInfo");
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
