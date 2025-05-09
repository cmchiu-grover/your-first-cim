const messageImgForm = document.getElementById("messageImgForm");
messageImgForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(messageImgForm);
  const res = await fetch("/api/posting", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  let messageImgDiv = document.createElement("div");
  messageImgDiv.className = "messageImgDiv";
  let messageText = document.createElement("div");
  messageText.className = "messageText";
  messageText.textContent = data.text;
  let messageFigure = document.createElement("figure");
  let figureImg = document.createElement("img");
  figureImg.src = data.img_url;
  messageFigure.appendChild(figureImg);
  messageImgDiv.appendChild(messageText);
  messageImgDiv.appendChild(messageFigure);
  document.getElementById("messageImgDisplayZone").prepend(messageImgDiv);
});

async function getPosts() {
  const res = await fetch(`/api/posts`);
  const resJSON = await res.json();
  const textImgList = resJSON.data;
  const articleZone = document.querySelector("#messageImgDisplayZone");

  textImgList.forEach((textImgData) => {
    let messageImgDiv = document.createElement("div");
    messageImgDiv.className = "messageImgDiv";
    let messageText = document.createElement("div");
    messageText.className = "messageText";
    let messageFigure = document.createElement("figure");
    let figureImg = document.createElement("img");
    messageText.textContent = textImgData.text;
    figureImg.src = textImgData.img_url;
    messageFigure.appendChild(figureImg);
    messageImgDiv.appendChild(messageText);
    messageImgDiv.appendChild(messageFigure);
    articleZone.appendChild(messageImgDiv);
  });
}

async function main() {
  await getPosts();
}

main();
