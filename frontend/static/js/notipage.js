import { notificationList } from "./variables.js";
import { signout } from "./user.js";
import { NotificationHandler } from "./notification.js";
import { checkUserData } from "./auth.js";
import { renderUserNav } from "./usernav.js";

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
  const userData = await checkUserData();
  if (!userData) return;

  await renderUserNav(userData);
  await NotificationHandler.init({ withSSE: true });
  await fetchNotifications();
}

main();

signout();
