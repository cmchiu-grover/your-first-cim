import { signout } from "./user.js";
import { NotificationHandler } from "./notification.js";
import { checkUserData } from "./auth.js";
import { renderUserNav, renderIEFunction2 } from "./usernav.js";

document.addEventListener("DOMContentLoaded", () => {
  const queryForm = document.getElementById("ie-query-form");
  const queryResultArea = document.getElementById("ie-query-result-area");
  const queryButton = document.getElementById("ie-query-stdt-button");
  const downloadCsvButton = document.getElementById("downloadCsvButton");

  // 處理表單提交
  queryForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    queryButton.disabled = true;
    queryButton.textContent = "查詢中...";

    const formData = new FormData(queryForm);
    const queryParams = new URLSearchParams();
    console.log("表單數據:", Object.fromEntries(formData.entries()));
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/standard_times_query";
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

      if (data.data && data.data.length > 0) {
        downloadCsvButton.style.cursor = "pointer";
        downloadCsvButton.style.color = " #f99a1e";
        downloadCsvButton.style.backgroundColor = "#000";

        downloadCsvButton.dataset.queryParams = queryParams.toString();
      }

      displayResults(data.data);

      displayPagination(data.totalPages || 1, data.nextPage - 1 || totalPages);
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryButton.disabled = false;
      queryButton.textContent = "查詢";
    }
  });

  function displayResults(results) {
    if (!results || results.length === 0) {
      window.alert("沒有找到符合條件的資料。");
      return;
    }

    const queryResultForm = document.querySelector("#ie-query-result-form");
    for (let i = queryResultForm.children.length - 1; i >= 1; i--) {
      queryResultForm.removeChild(queryResultForm.children[i]);
    }

    results.forEach((row) => {
      const columns = [
        row.standard_time_id,
        row.prod_code,
        row.prod_name,
        row.eqp_type,
        row.module_name,
        row.station_name,
        row.stdt,
        row.updated_time,
        row.description,
      ];
      const parent_div = document.createElement("div");
      parent_div.classList.add("ie_query_result_maintain_div");
      for (let i = 0; i < 9; i++) {
        if (i === 7) {
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_maintain_input";
          input_container.id = "ie_maintain_input_stdt";
          input_container.required = true;
          input_container.value = columns[i] || "";
          parent_div.appendChild(input_container);
        } else if (i === 9) {
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_maintain_input";
          input_container.id = "ie_maintain_input_stdt";
          input_container.required = true;
          input_container.value = columns[i] || "";

          parent_div.appendChild(input_container);
        } else {
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_query_result_input";
          input_container.value = columns[i] || "";
          input_container.readOnly = true;
          parent_div.appendChild(input_container);
        }
      }
      queryResultForm.appendChild(parent_div);
    });
  }

  function displayPagination(totalPages, currentPage) {
    if (currentPage < 1 || currentPage > totalPages) {
      currentPage = totalPages;
    }
    const paginationContainer = document.getElementById(
      "ie-query-result-pagenumber"
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
    const formData = new FormData(queryForm);
    const queryParams = new URLSearchParams();

    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/standard_times_query?page=" + newPage;
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
      queryButton.disabled = false; // 啟用按鈕
      queryButton.textContent = "查詢";
    }
  }
});

downloadCsvButton.addEventListener("click", async () => {
  const queryParams = downloadCsvButton.dataset.queryParams;
  const downloadUrl = `/api/standard_times_download_csv?${queryParams}`;

  console.log("下載 CSV URL:", downloadUrl);

  try {
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = "query_results.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("下載 CSV 時發生錯誤:", error);
    alert("下載 CSV 檔案時發生錯誤。");
  }
});

async function main() {
  const userData = await checkUserData();
  if (!userData) return;

  if (userData.position === "IE") {
    await renderUserNav(userData);
  } else {
    alert("權限不足，無法進入此頁面！");
    window.location.href = "/";
  }
  const funcNavUlLi = document.getElementById("funcNavUlLi");
  const funcNavUlLiA = document.getElementById("funcNavUlLiA");
  if (funcNavUlLi) {
    funcNavUlLi.style.backgroundColor = "#ccc";
    funcNavUlLi.style.borderRadius = "3px";
    funcNavUlLiA.style.color = "#000";
  }

  await renderIEFunction2();
  await NotificationHandler.init({ withSSE: true });
}

main();
signout();
