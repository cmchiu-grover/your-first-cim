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
      funcNavUlLi.style.backgroundColor = "#ccc";
      funcNavUlLi.style.borderRadius = "3px";

      // console.log(userData.position);

      let funcNavUlLiA = document.createElement("a");
      funcNavUlLiA.textContent = `${userData.position} 維護`;
      funcNavUlLiA.style.color = "#000";

      funcNavUlLi.appendChild(funcNavUlLiA);
      funcNavUl.appendChild(funcNavUlLi);

      if (userData.position === "IE") {
        // 這邊放IE維護
        // console.log("放IE維護");
        funcNavUlLiA.href = "/iemaintain";
        let funcNavUlDiv = document.createElement("div");
        let funcNavUlDivA1 = document.createElement("a");
        let funcNavUlDivA2 = document.createElement("a");
        let funcNavUlDivI = document.createElement("i");
        funcNavUlDivI.className = "material-icons";
        funcNavUlDivI.textContent = "arrow_right";
        funcNavUlDivA2.appendChild(funcNavUlDivI);
        funcNavUlDiv.className = "ie_maintain_div";
        funcNavUlDivA1.textContent = "工時維護";
        funcNavUlDivA1.href = "/iemaintain";
        funcNavUlDivA2.style.color = "#000";
        funcNavUlDivA2.style.backgroundColor = "#ccc";
        funcNavUlDivA2.appendChild(document.createTextNode("工時查詢"));
        funcNavUlDivA2.href = "/iequery";
        // funcNavUlDivA1.style.color = "#e4e6ea";
        funcNavUlDiv.appendChild(funcNavUlDivA1);
        funcNavUlDiv.appendChild(funcNavUlDivA2);
        funcNavUl.appendChild(funcNavUlDiv);
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
    console.log("表單數據:", Object.fromEntries(formData.entries())); // 用於調試，查看表單數據
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, ""); // 如果沒有值，則添加空字符串
      }
    }

    // 基本 API URL
    const apiUrl = "/api/standard_times_query";
    const fullUrl = `${apiUrl}?${queryParams.toString()}`;

    console.log("查詢 URL:", fullUrl); // 用於調試，查看最終的查詢 URL

    try {
      const response = await fetch(fullUrl, {
        method: "GET", // 使用 GET 方法
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        // 如果 HTTP 狀態碼不是 2xx
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      console.log("查詢結果:", data);
      // 如果有查詢結果，才顯示下載按鈕
      if (data.data && data.data.length > 0) {
        downloadCsvButton.style.cursor = "pointer"; // 設置為可點擊
        downloadCsvButton.style.color = " #f99a1e"; // 設置為黑色
        downloadCsvButton.style.backgroundColor = "#000"; // 設置為黑色
        // 將當前的查詢參數儲存在一個數據屬性中，以便下載按鈕使用
        downloadCsvButton.dataset.queryParams = queryParams.toString();
      }

      // 顯示查詢結果
      displayResults(data.data);
      // 顯示頁碼資訊 (這裡假設後端會返回總頁數或總筆數)
      displayPagination(data.totalPages || 1, data.nextPage - 1 || totalPages);
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryButton.disabled = false; // 啟用按鈕
      queryButton.textContent = "查詢";
    }
  });

  // 顯示結果的函數
  function displayResults(results) {
    if (!results || results.length === 0) {
      window.alert("沒有找到符合條件的資料。");
      return;
    }
    // 創建結果表格
    const queryResultForm = document.querySelector("#ie-query-result-form");
    for (let i = queryResultForm.children.length - 1; i >= 1; i--) {
      queryResultForm.removeChild(queryResultForm.children[i]);
    }

    results.forEach((row) => {
      // console.log("處理行數據:", row); // 用於調試，查看每行數據
      const columns = [
        "", // 第一列為勾選框，無需從後端獲取
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
      parent_div.classList.add("ie_query_result_maintain_div"); // 添加 class 以便 CSS 樣式化
      for (let i = 0; i < 10; i++) {
        // console.log("列索引:", i); // 用於調試，查看列索引
        // console.log("處理列數據:", columns[i]); // 用於調試，查看每列數據
        if (i === 0) {
          // 第1個
          const input_container = document.createElement("input");
          input_container.type = "checkbox";
          input_container.className = "ie_query_checkbox";
          parent_div.appendChild(input_container);
        } else if (i === 7) {
          // 第7個，STDT
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_maintain_input";
          input_container.id = "ie_maintain_input_stdt";
          input_container.required = true; // 設置為必填
          input_container.value = columns[i] || ""; // 如果沒有值，則設置為空字符串
          parent_div.appendChild(input_container);
        } else if (i === 9) {
          // 第7個，STDT
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_maintain_input";
          input_container.id = "ie_maintain_input_stdt";
          input_container.required = true; // 設置為必填
          input_container.value = columns[i] || ""; // 如果沒有值，則設置為空字符串

          parent_div.appendChild(input_container);
        } else {
          // columns[i] = ""; // 將 null 或 undefined 替換為空字符串
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "ie_query_result_input";
          input_container.value = columns[i] || ""; // 如果沒有值，則設置為空字符串
          input_container.readOnly = true; // 設置為只讀
          parent_div.appendChild(input_container);
        }
      }
      queryResultForm.appendChild(parent_div);
    });
  }

  function displayPagination(totalPages, currentPage) {
    if (currentPage < 1 || currentPage > totalPages) {
      currentPage = totalPages; // 確保當前頁面在有效範圍內
    }
    const paginationContainer = document.getElementById(
      "ie-query-result-pagenumber"
    );
    paginationContainer.innerHTML = ""; // 清空現有內容
    console.log(currentPage, totalPages); // 用於調試，查看當前頁面和總頁數
    const pageInfo = document.createElement("p");
    pageInfo.textContent = `第 ${currentPage} 頁，共 ${totalPages} 頁`;
    paginationContainer.appendChild(pageInfo);

    const nav = document.createElement("div");
    nav.classList.add("pagination-nav");

    // 上一頁按鈕
    const prevBtn = document.createElement("button");
    prevBtn.textContent = "« 上一頁";
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener("click", async () => changePage(currentPage - 1));
    nav.appendChild(prevBtn);

    // 頁碼按鈕（顯示最多 5 個）
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

    // 下一頁按鈕
    const nextBtn = document.createElement("button");
    nextBtn.textContent = "下一頁 »";
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener("click", async () => changePage(currentPage + 1));
    nav.appendChild(nextBtn);

    paginationContainer.appendChild(nav);
  }

  // 假設的換頁函數，你需要根據實際查詢資料的方式來實作
  async function changePage(newPage) {
    console.log("切換到第", newPage, "頁");
    const formData = new FormData(queryForm);
    const queryParams = new URLSearchParams();
    // console.log("表單數據:", Object.fromEntries(formData.entries())); // 用於調試，查看表單數據
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, ""); // 如果沒有值，則添加空字符串
      }
    }

    // 基本 API URL
    const apiUrl = "/api/standard_times_query?page=" + newPage;
    const fullUrl = `${apiUrl}&${queryParams.toString()}`;
    try {
      const response = await fetch(fullUrl, {
        method: "GET", // 使用 GET 方法
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        // 如果 HTTP 狀態碼不是 2xx
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      console.log(`changePage(${newPage}) 查詢結果:`, data);

      // 顯示查詢結果
      displayResults(data.data);
      // 顯示頁碼資訊 (這裡假設後端會返回總頁數或總筆數)

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

// 為下載按鈕新增事件監聽器
downloadCsvButton.addEventListener("click", async () => {
  const queryParams = downloadCsvButton.dataset.queryParams; // 獲取之前儲存的查詢參數
  const downloadUrl = `/api/standard_times_download_csv?${queryParams}`;

  console.log("下載 CSV URL:", downloadUrl);

  try {
    // 使用 window.open 或創建一個隱藏的 A 標籤來觸發下載
    // 這樣瀏覽器會自動處理 Content-Disposition 標頭
    // window.open(downloadUrl, "_blank"); // 在新分頁打開並下載

    // 或者更優雅的觸發下載（如果你不想打開新分頁）
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = "query_results.csv"; // 建議的下載檔名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("下載 CSV 時發生錯誤:", error);
    alert("下載 CSV 檔案時發生錯誤。");
  }
});

// 主函數，確保在頁面加載時檢查用戶登入狀態

async function main() {
  await checkSignin();
}

main();
