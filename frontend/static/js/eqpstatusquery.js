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

      // console.log(userData.position);

      let funcNavUlLiA = document.createElement("a");
      funcNavUlLiA.textContent = `${userData.position} 維護`;

      funcNavUlLi.appendChild(funcNavUlLiA);
      funcNavUl.appendChild(funcNavUlLi);

      if (userData.position === "IE") {
        // 這邊放IE維護
        funcNavUlLiA.href = "/iemaintain";
        const eqGanttLi = [...funcNavUl.children].find(
          (li) => li.textContent.trim() === "機況圖"
        );

        if (eqGanttLi) {
          const eqStatusLi = document.createElement("li");
          eqStatusLi.className = "function_nav_ul_li";
          eqStatusLi.style.backgroundColor = "#ccc";
          eqStatusLi.style.borderRadius = "3px";

          const eqStatusA = document.createElement("a");
          eqStatusA.href = "eqpstatusquery";
          eqStatusA.textContent = "機況查詢";
          eqStatusA.style.color = "#000";

          eqStatusLi.appendChild(eqStatusA);
          eqGanttLi.insertAdjacentElement("afterend", eqStatusLi);
        }
      } else {
        // 這邊放EQ維護
        window.alert("權限不足，無法進入此頁面！");
        window.location.href = "/";
      }
    }
  } else {
    window.alert("請先登入");
    window.location.href = "/";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const eqQueryForm = document.getElementById("eqp-status-query-form");
  const queryStatusButton = document.getElementById("eqp-status-query-button");

  // 處理表單提交
  eqQueryForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    queryStatusButton.disabled = true;
    queryStatusButton.textContent = "查詢中...";

    const formData = new FormData(eqQueryForm);
    const queryParams = new URLSearchParams();
    console.log("表單數據:", Object.fromEntries(formData.entries()));
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/eqp_status_query/ie";
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

      displayResults(data.data);

      displayPagination(data.totalPages || 1, data.nextPage - 1 || totalPages);
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryStatusButton.disabled = false;
      queryStatusButton.textContent = "查詢";
    }
  });

  function displayResults(results) {
    if (!results || results.length === 0) {
      window.alert("沒有找到符合條件的資料。");
      return;
    }

    const queryResultForm = document.querySelector(
      "#eqp-status-query-result-form"
    );
    for (let i = queryResultForm.children.length - 1; i >= 1; i--) {
      queryResultForm.removeChild(queryResultForm.children[i]);
    }

    results.forEach((row) => {
      const columns = [
        row.id,
        row.work_date,
        row.module_name,
        row.station_name,
        row.eqp_type,
        row.eqp_code,
        row.start_time,
        row.end_time,
        row.duration,
        row.status,
        row.comment,
      ];
      const parent_div = document.createElement("div");
      parent_div.classList.add("eqp_status_result_div");
      for (let i = 0; i < 11; i++) {
        const input_container = document.createElement("input");
        input_container.type = "text";
        input_container.className = "eqp_status_result_input";
        input_container.value = columns[i] || "";
        input_container.readOnly = true;
        parent_div.appendChild(input_container);
      }
      queryResultForm.appendChild(parent_div);
    });
  }

  function displayPagination(totalPages, currentPage) {
    if (currentPage < 1 || currentPage > totalPages) {
      currentPage = totalPages;
    }
    const paginationContainer = document.getElementById(
      "eqp-status-query-result-pagenumber"
    );
    paginationContainer.innerHTML = "";
    console.log(currentPage, totalPages);
    const pageInfo = document.createElement("p");
    pageInfo.textContent = `第 ${currentPage} 頁，共 ${totalPages} 頁`;
    paginationContainer.appendChild(pageInfo);

    const nav = document.createElement("div");
    nav.classList.add("pagination-nav");

    const prevBtn = document.createElement("button");
    prevBtn.textContent = "« 上一頁";
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener("click", async () => changePage(currentPage - 1));
    nav.appendChild(prevBtn);

    const start = Math.max(1, currentPage - 2);
    const end = Math.min(totalPages, start + 4);

    for (let i = start; i <= end; i++) {
      const pageBtn = document.createElement("button");
      pageBtn.textContent = i;
      if (i === currentPage) {
        pageBtn.classList.add("active");
      }
      pageBtn.addEventListener("click", async () => changePage(i));
      nav.appendChild(pageBtn);
    }

    const nextBtn = document.createElement("button");
    nextBtn.textContent = "下一頁 »";
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener("click", async () => changePage(currentPage + 1));
    nav.appendChild(nextBtn);

    paginationContainer.appendChild(nav);
  }

  async function changePage(newPage) {
    console.log("切換到第", newPage, "頁");
    const formData = new FormData(eqQueryForm);
    const queryParams = new URLSearchParams();

    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/eqp_status_query/ie?page=" + newPage;
    const fullUrl = `${apiUrl}&${queryParams.toString()}`;
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
      console.log(`changePage(${newPage}) 查詢結果:`, data);

      displayResults(data.data);

      displayPagination(data.totalPages, data.nextPage - 1);
    } catch (error) {
      console.error("查詢失敗:", error);
      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryStatusButton.disabled = false; // 啟用按鈕
      queryStatusButton.textContent = "查詢";
    }
  }
});

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
    element.textContent = `僅支持查詢 work_date：2025/05/01 ~ ${formattedDate}`;
  }
}

async function main() {
  await checkSignin();
  await setYesterdayDateText("dateInfo");
}

main();
signout();
