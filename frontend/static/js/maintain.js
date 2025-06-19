import { signout } from "./user.js";
import { NotificationHandler } from "./notification.js";
import { checkUserData } from "./auth.js";
import { renderUserNav, renderIEFunction1 } from "./usernav.js";

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

  await renderIEFunction1();

  await NotificationHandler.init({ withSSE: true });
}

main();
signout();
