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
    console.log(userData.position);

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

async function main() {
  await checkSignin();
}

main();
signout();

document.addEventListener("DOMContentLoaded", async function () {
  const queryOEEForm = document.getElementById("oee-table-query-form");
  const queryOEEButton = document.getElementById("query-oee-button");
  const queryStationOEEForm = document.getElementById(
    "station-oee-table-query-form"
  );
  const queryStationOEEButton = document.getElementById(
    "station-oee-query-button"
  );

  queryOEEForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    queryOEEButton.disabled = true;
    queryOEEButton.textContent = "查詢中...";

    const formData = new FormData(queryOEEForm);
    const queryParams = new URLSearchParams();
    console.log("表單數據:", Object.fromEntries(formData.entries()));
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/oee";
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

      updateOEETable(data);
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryOEEButton.disabled = false; // 啟用按鈕
      queryOEEButton.textContent = "查詢";
    }
  });

  queryStationOEEForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    queryStationOEEButton.disabled = true;
    queryStationOEEButton.textContent = "查詢中...";

    const formData = new FormData(queryStationOEEForm);
    const queryParams = new URLSearchParams();
    console.log("表單數據:", Object.fromEntries(formData.entries()));
    for (const [key, value] of formData.entries()) {
      if (value) {
        queryParams.append(key, value);
      } else {
        queryParams.append(key, "");
      }
    }

    const apiUrl = "/api/oee/station";
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
      function updateStationOEETable(apiData) {
        if (!apiData.ok || !Array.isArray(apiData.data)) return;

        const table = document.getElementById("stationOEETable");
        const headerRow = table.querySelector("thead tr");
        const oeeRow = document.getElementById("eqp-oee-Row");
        const availRow = document.getElementById("eqp-avail-Row");
        const perfRow = document.getElementById("eqp-perf-Row");

        headerRow.innerHTML = "<th>Metrics</th>";
        oeeRow.innerHTML = "<td>OEE Rate(%)</td>";
        availRow.innerHTML = "<td>Availability Rate(%)</td>";
        perfRow.innerHTML = "<td>Performance Rate(%)</td>";

        apiData.data.forEach((item) => {
          const station = item.metrics;

          const th = document.createElement("th");
          th.textContent = station;
          headerRow.appendChild(th);

          // 新增 OEE Rate 數值
          const oeeTd = document.createElement("td");
          oeeTd.textContent = item.oee_rate.toFixed(2);
          oeeTd.classList.toggle("low-value", item.oee_rate < 72.0);
          oeeRow.appendChild(oeeTd);

          // 新增 Availability Rate 數值
          const availTd = document.createElement("td");
          availTd.textContent = item.avail_rate.toFixed(2);
          availTd.classList.toggle("low-value", item.avail_rate < 80.0);
          availRow.appendChild(availTd);

          // 新增 Performance Rate 數值
          const perfTd = document.createElement("td");
          perfTd.textContent = item.perf_rate?.toFixed(2) ?? "-";
          perfTd.classList.toggle("low-value", item.perf_rate < 90.0);
          perfRow.appendChild(perfTd);
        });
      }

      updateStationOEETable(data);
    } catch (error) {
      console.error("查詢失敗:", error);

      window.alert(`查詢失敗: ${error.message}`);
    } finally {
      queryStationOEEButton.disabled = false; // 啟用按鈕
      queryStationOEEButton.textContent = "查詢";
    }
  });
});
