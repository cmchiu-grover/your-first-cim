import { userNameP, funcNavUl, notificationList } from "./variables.js";
import { signout } from "./user.js";

async function checkSignin() {
  console.log("Checking sign-in status...");
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

async function fetchNotifications() {
  if (!notificationList) return;
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("/api/notifications", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch notifications");
    }

    const data = await response.json();
    console.log("Fetched notifications:", data);

    notificationList.innerHTML = ""; // Clear existing notifications

    data.notifications.forEach((notification) => {
      const li = document.createElement("li");
      const pTagId = document.createElement("p");
      pTagId.className = "notification_list_item_id";
      const pTagMsg = document.createElement("p");
      pTagMsg.className = "notification_list_item_msg";
      const pTagCT = document.createElement("p");
      pTagCT.className = "notification_list_item_ct";
      pTagId.textContent = `${notification.id}`;
      pTagMsg.textContent = `${notification.message}`;
      pTagCT.textContent = `${new Date(
        notification.creation_time
      ).toLocaleString()}`;

      li.appendChild(pTagId);
      li.appendChild(pTagMsg);
      li.appendChild(pTagCT);

      notificationList.appendChild(li);
    });
  } catch (error) {
    console.error("Error fetching notifications:", error);
    const li = document.createElement("li");
    li.textContent = "無法載入通知";
    notificationList.appendChild(li);
  }
}

async function main() {
  await checkSignin();
  await fetchNotifications();
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
    const response = await fetch("/api/oee/yesterday", {
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
  } catch (error) {
    console.error("查詢失敗:", error);

    window.alert(`查詢失敗: ${error.message}`);
  }
});
