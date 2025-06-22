import { signout } from "./user.js";
import { NotificationHandler } from "./notification.js";
import { checkUserData } from "./auth.js";
import { renderUserNav } from "./usernav.js";

async function main() {
  const userData = await checkUserData();
  if (!userData) return;

  await renderUserNav(userData);

  await NotificationHandler.init({ withSSE: true });
}

main();

signout();

document.addEventListener("DOMContentLoaded", async function () {
  function updateOEETable(apiData) {
    if (!apiData.ok || !Array.isArray(apiData.data)) return;

    apiData.data.forEach((item) => {
      const station = item.metrics;
      console.log(station);

      const oeeCell = document.querySelector(
        `#oeeRow td[data-station="${station}"]`
      );
      console.log(oeeCell);
      if (oeeCell) {
        oeeCell.textContent = item.oee_rate.toFixed(2);
        oeeCell.classList.toggle("low-value", item.oee_rate < 72.0);
      }

      const availCell = document.querySelector(
        `#availRow td[data-station="${station}"]`
      );
      if (availCell) {
        availCell.textContent = item.avail_rate.toFixed(2);
        availCell.classList.toggle("low-value", item.avail_rate < 80.0);
      }

      const perfCell = document.querySelector(
        `#perfRow td[data-station="${station}"]`
      );
      if (perfCell) {
        perfCell.textContent = item.perf_rate.toFixed(2);
        perfCell.classList.toggle("low-value", item.perfCell < 90.0);
      }
    });
  }

  try {
    const response = await fetch("/api/oee?date=yesterday", {
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
    updateOEETable(data);
    const dashboardOEETitle = document.getElementById("dashboardOEETile");

    dashboardOEETitle.textContent = `昨日（${data.date}）站點 OEE 資料`;
  } catch (error) {
    console.error("查詢失敗:", error);

    window.alert(`查詢失敗: ${error.message}`);
  }
});
