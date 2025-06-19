import { userNameP, funcNavUl } from "./variables.js";

async function renderUserNav(userData) {
  const { name, position } = userData;

  if (userNameP) {
    userNameP.textContent = `Hi ${name}`;
  }

  const funcNavUlLi = document.createElement("li");
  funcNavUlLi.id = "funcNavUlLi";
  funcNavUlLi.className = "function_nav_ul_li";

  const funcNavUlLiA = document.createElement("a");
  funcNavUlLiA.id = "funcNavUlLiA";
  funcNavUlLiA.textContent = `${position} 維護`;

  if (position === "IE") {
    funcNavUlLiA.href = "/iemaintain";
    renderEqpStatusQueryNav();
  } else if (position === "MFG") {
    funcNavUlLiA.href = "/mfgmaintain";
  } else {
    funcNavUlLiA.href = "/eqmaintain";
  }

  funcNavUlLi.appendChild(funcNavUlLiA);
  funcNavUl.appendChild(funcNavUlLi);
}

async function renderEqpStatusQueryNav() {
  const eqGanttLi = [...funcNavUl.children].find(
    (li) => li.textContent.trim() === "機況圖"
  );

  if (eqGanttLi) {
    const eqStatusLi = document.createElement("li");
    eqStatusLi.className = "function_nav_ul_li";
    eqStatusLi.id = "eqStatusLi";

    const eqStatusA = document.createElement("a");
    eqStatusA.id = "eqStatusA";
    eqStatusA.href = "eqpstatusquery";
    eqStatusA.textContent = "機況查詢";

    eqStatusLi.appendChild(eqStatusA);
    eqGanttLi.insertAdjacentElement("afterend", eqStatusLi);
  }
}

async function renderIEFunction1() {
  const funcNavUlDiv = document.createElement("div");
  funcNavUlDiv.className = "ie_maintain_div";

  const a1 = document.createElement("a");
  a1.textContent = "工時維護";
  a1.href = "/iemaintain";

  const a2 = document.createElement("a");
  a2.href = "/iequery";
  a2.textContent = "工時查詢";

  const icon = document.createElement("i");
  icon.className = "material-icons";
  icon.textContent = "arrow_right";

  a1.style.color = "#000";
  a1.style.backgroundColor = "#ccc";
  a1.appendChild(icon);

  funcNavUlDiv.appendChild(a1);
  funcNavUlDiv.appendChild(a2);
  funcNavUl.appendChild(funcNavUlDiv);
}

async function renderIEFunction2() {
  const funcNavUlDiv = document.createElement("div");
  funcNavUlDiv.className = "ie_maintain_div";

  const a1 = document.createElement("a");
  a1.textContent = "工時維護";
  a1.href = "/iemaintain";

  const a2 = document.createElement("a");
  a2.href = "/iequery";
  a2.textContent = "工時查詢";

  const icon = document.createElement("i");
  icon.className = "material-icons";
  icon.textContent = "arrow_right";

  a2.style.color = "#000";
  a2.style.backgroundColor = "#ccc";
  a2.appendChild(icon);

  funcNavUlDiv.appendChild(a1);
  funcNavUlDiv.appendChild(a2);
  funcNavUl.appendChild(funcNavUlDiv);
}

export { renderUserNav, renderIEFunction1, renderIEFunction2 };
