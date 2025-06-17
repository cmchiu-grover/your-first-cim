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

      if (userData.position === "IE") {
        // 這邊放IE維護
        // console.log("放IE維護");
        funcNavUlLiA.href = "/iemaintain";
        let funcNavUlDiv = document.createElement("div");
        let funcNavUlDivA1 = document.createElement("a");
        let funcNavUlDivA2 = document.createElement("a");
        let funcNavUlDivI = document.createElement("i");
        funcNavUlDivI.className = "material-icons";
        funcNavUlDivI.style.color = "#000";
        funcNavUlDivI.textContent = "arrow_right";
        // funcNavUlDivI.style.fontSize = "16px";
        funcNavUlDivA1.appendChild(funcNavUlDivI);
        funcNavUlDiv.className = "ie_maintain_div";
        funcNavUlDivA1.appendChild(document.createTextNode("工時維護"));
        funcNavUlDivA1.href = "/iemaintain";
        funcNavUlDivA1.style.color = "#000";
        funcNavUlDivA1.style.backgroundColor = "#ccc";
        funcNavUlDivA2.textContent = "工時查詢";
        funcNavUlDivA2.href = "/iequery";
        // funcNavUlDivA2.style.color = "#e4e6ea";
        funcNavUlDiv.appendChild(funcNavUlDivA1);
        funcNavUlDiv.appendChild(funcNavUlDivA2);
        funcNavUl.appendChild(funcNavUlDiv);

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
    }
  } else {
    window.alert("請先登入");
    window.location.href = "/";
  }
}

const updateSTDTButton = document.getElementById("update_stdt_btn");

updateSTDTButton.addEventListener("click", async () => {
  updateSTDTButton.disabled = true;
  updateSTDTButton.textContent = "查詢中...";
  const token = localStorage.getItem("access_token");
  let counter = 0;
  let inputArray = [];
  const data = Array.from(document.querySelectorAll(".ie_update_div"));
  for (let i = 0; i < data.length; i++) {
    // console.log(`第 ${i} 個 div`);
    const input = data[i].querySelectorAll("input");
    let input_counter = 0;
    for (let j = 0; j < input.length; j++) {
      // console.log(`第 ${j} 個 input: ${input[j].value}`);
      if (input[j].value.trim() !== "") {
        input_counter++;
      }
    }
    // console.log(`input_counter: ${input_counter}`);
    if (input_counter === 4) {
      inputArray.push(i);
      counter++;
    }
  }
  // console.log(`counter: ${counter}`);
  // console.log(`inputArray: ${inputArray}`);

  // console.log(`data: ${data}`);

  // console.log(`data: ${JSON.stringify(data)}`);
  // console.log(`data.length: ${data.length}`);

  if (counter === 0) {
    window.alert("請至少填寫一組資料");
    updateSTDTButton.disabled = false;
    updateSTDTButton.textContent = "更新工時";
    return;
  }

  const inputData = [];

  inputArray.forEach((index) => {
    const temp_div = data[index];
    const temp_inputs = temp_div.querySelectorAll("input");
    inputData.push({
      prod_code: temp_inputs[0].value.trim(),
      eqp_type: temp_inputs[1].value.trim(),
      station_name: temp_inputs[2].value.trim(),
      stdt: parseFloat(temp_inputs[3].value.trim()),
    });
    // console.log(`inputData for index ${index}:`, inputData);
  });

  console.log(inputData);

  try {
    const response = await fetch("/api/ie_maintain_stdt", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(inputData),
    });

    const result = await response.json();
    console.log("更新結果:", result);

    if (result.ok) {
      window.alert("更新成功");
      window.location.reload();
    } else {
      window.alert(result.message);
    }
  } catch (error) {
    console.error("Error updating STDT:", error);
    window.alert("更新失敗，請稍後再試");
  } finally {
    updateSTDTButton.disabled = false;
    updateSTDTButton.textContent = "更新工時";
  }
});

async function main() {
  await checkSignin();
}

main();
signout();
