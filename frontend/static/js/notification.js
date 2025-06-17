const NotificationHandler = (function () {
  const token = localStorage.getItem("access_token");
  console.log("Token:", token);
  const updateDot = document.querySelector("#updateDot");
  const nofiBell = document.querySelector("#notifications");

  async function fetchUnreadNotifications() {
    try {
      const res = await fetch("/api/notifications/unread", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      console.log("通知查詢結果：", res);
      const data = await res.json();
      console.log("通知數據：", data);
      console.log("通知數據長度：", data.has_unread.length);
      if (data.has_unread.length > 0) {
        console.log("有未讀通知，顯示紅點");
        showRedDot();
        return data.has_unread.map((n) => n.id);
      } else {
        console.log("沒有未讀通知，隱藏紅點");
        hideRedDot();
        return [];
      }
    } catch (err) {
      console.error("通知查詢失敗：", err);
      return [];
    }
  }

  function showRedDot() {
    if (updateDot) updateDot.style.display = "inline-block";
  }

  function hideRedDot() {
    if (updateDot) updateDot.style.display = "none";
  }

  async function markAsRead(ids) {
    if (ids.length === 0) return;
    console.log("Call API", ids);
    try {
      await fetch("/api/notifications/mark_read", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ notification_ids: ids }),
      });
      console.log("hideRedDot");
      hideRedDot();
    } catch (err) {
      console.error("標記通知為已讀失敗：", err);
    }
  }

  function setupRedDotClick() {
    if (nofiBell) {
      nofiBell.addEventListener("click", async () => {
        try {
          const ids = await fetchUnreadNotifications();
          console.log("點擊紅點，未讀通知 ID：", ids);
          await markAsRead(ids);
        } catch (e) {
          console.log(e);
        }
        window.location.href = "/notifications";
      });
    }
  }

  let currentUserId = null;

  async function init(options = { withSSE: true }) {
    fetchUnreadNotifications();
    setupRedDotClick();

    const token = localStorage.getItem("access_token");
    if (token) {
      const response = await fetch("/api/user/auth", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await response.json();
      const currentUserId = result.data.user_id;

      document.addEventListener("visibilitychange", async () => {
        if (document.visibilityState === "visible") {
          await fetchUnreadNotifications();
        }
      });

      if (options.withSSE && currentUserId) {
        const sse = new EventSource("/sse/standard_time");
        sse.onmessage = async function (event) {
          console.log("收到 SSE 通知：", event.data);
          const eventJson = JSON.parse(event.data);

          if (parseInt(currentUserId) === parseInt(eventJson.user_id)) {
            // 自己發起的通知，不開啟紅點
            return;
          }
        };

        showRedDot();
      }
    }
  }

  return { init, fetchUnreadNotifications, markAsRead };
})();
