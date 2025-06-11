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
      funcNavUlLi.style.backgroundColor = "#ccc";
      funcNavUlLi.style.borderRadius = "3px";

      // console.log(userData.position);

      let funcNavUlLiA = document.createElement("a");
      funcNavUlLiA.textContent = `${userData.position} 維護`;
      funcNavUlLiA.style.color = "#000";

      funcNavUlLi.appendChild(funcNavUlLiA);
      funcNavUl.appendChild(funcNavUlLi);

      if (userData.position === "MFG") {
        // 這邊放IE維護
        // console.log("放IE維護");
        funcNavUlLiA.href = "/mfgmaintain";
        let funcNavUlDiv = document.createElement("div");
        funcNavUlDiv.className = "ie_maintain_div";

        // funcNavUlDivA1.style.color = "#e4e6ea";

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
  const eqQueryForm = document.getElementById("eq-query-form");
  const queryStatusButton = document.getElementById("eq-query-status-button");
  const updateEQButton = document.getElementById("updateMFGButton");
  updateEQButton.disabled = true;

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

    const apiUrl = "/api/eqp_status_query/mfg";
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
        updateEQButton.style.cursor = "pointer";
        updateEQButton.style.color = " #f99a1e";
        updateEQButton.style.backgroundColor = "#000";
        updateEQButton.disabled = false;
      }

      displayResults(data.data);

      // 綁定輸入事件：只要填寫 comment 就自動勾選該行 checkbox
      const resultRows = document.querySelectorAll(
        ".eq_query_result_maintain_div"
      );

      resultRows.forEach((rowDiv) => {
        const commentInput = rowDiv.querySelector(".eq_maintain_input");
        const checkbox = rowDiv.querySelector(".eq_query_checkbox");

        if (commentInput && checkbox) {
          commentInput.addEventListener("input", () => {
            checkbox.checked = commentInput.value.trim() !== "";
          });
        }
      });

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

    const queryResultForm = document.querySelector("#eq-query-result-form");
    for (let i = queryResultForm.children.length - 1; i >= 1; i--) {
      queryResultForm.removeChild(queryResultForm.children[i]);
    }

    let num_j = 1;

    results.forEach((row) => {
      const columns = [
        "",
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
      parent_div.classList.add("eq_query_result_maintain_div");
      for (let i = 0; i < 12; i++) {
        if (i === 0) {
          const input_container = document.createElement("input");
          input_container.type = "checkbox";
          input_container.className = "eq_query_checkbox";
          parent_div.appendChild(input_container);
        } else if (i === 11) {
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "eq_maintain_input";
          input_container.id = "eq_maintain_input_comment" + num_j;
          input_container.required = true;
          input_container.value = columns[i] || "";

          parent_div.appendChild(input_container);
        } else {
          const input_container = document.createElement("input");
          input_container.type = "text";
          input_container.className = "eq_query_result_input";
          input_container.value = columns[i] || "";
          input_container.readOnly = true;
          parent_div.appendChild(input_container);
        }
      }
      queryResultForm.appendChild(parent_div);
      num_j++;
    });
  }

  function displayPagination(totalPages, currentPage) {
    if (currentPage < 1 || currentPage > totalPages) {
      currentPage = totalPages;
    }
    const paginationContainer = document.getElementById(
      "eq-query-result-pagenumber"
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

    const apiUrl = "/api/eqp_status_query/eq?page=" + newPage;
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

  updateEQButton.addEventListener("click", async () => {
    const selectedRows = document.querySelectorAll(
      ".eq_query_result_maintain_div"
    );

    const updateData = [];

    selectedRows.forEach((row) => {
      const checkbox = row.querySelector(".eq_query_checkbox");
      if (checkbox.checked) {
        const inputs = row.querySelectorAll("input");
        const rowData = {
          id: inputs[1].value,
          work_date: inputs[2].value,
          module_name: inputs[3].value,
          station_name: inputs[4].value,
          eqp_type: inputs[5].value,
          eqp_code: inputs[6].value,
          comment: inputs[11].value,
        };
        updateData.push(rowData);
      }
    });

    if (updateData.length === 0) {
      alert("請至少填寫一筆資料後再點更新！");
      return;
    }

    console.log("即將送出的資料：", updateData);

    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("/api/eqp_status_update", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const result = await response.json();
      alert("更新成功！");
    } catch (error) {
      console.error("更新失敗:", error);
      alert("更新失敗: " + error.message);
    }
  });
});

async function main() {
  await checkSignin();
}

main();
signout();
