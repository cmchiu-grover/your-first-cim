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
        const eqGanttLi = [...funcNavUl.children].find(
          (li) => li.textContent.trim() === "機況圖"
        );

        if (eqGanttLi) {
          const eqStatusLi = document.createElement("li");
          eqStatusLi.className = "function_nav_ul_li";

          const eqStatusA = document.createElement("a");
          eqStatusA.href = "eqpstatusquery";
          eqStatusA.textContent = "機況查詢";

          eqStatusLi.appendChild(eqStatusA);
          eqGanttLi.insertAdjacentElement("afterend", eqStatusLi);
        }
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
      pTagMsg.innerHTML = notification.message.replace(/\n/g, "<br>");
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
