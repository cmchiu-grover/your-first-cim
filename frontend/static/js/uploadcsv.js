const updateCSVFileButton = document.getElementById("update_csv_file_btn");
updateCSVFileButton.addEventListener("click", async (e) => {
  e.preventDefault();
  updateCSVFileButton.disabled = true;
  updateCSVFileButton.textContent = "上傳中...";

  const form = document.getElementById("csvFileForm");
  const formData = new FormData(form);
  const fileInput = form.querySelector('input[type="file"]');

  if (!fileInput.files.length) {
    alert("請選擇一個 CSV 檔案！");
    updateCSVFileButton.disabled = false;
    updateCSVFileButton.textContent = "送出檔案";
    return;
  }

  try {
    const res = await fetch("/api/ie_maintain_stdt/upload_csv", {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: formData,
    });

    const result = await res.json();
    if (res.ok) {
      alert("上傳成功：" + result.message);
    } else {
      alert("上傳失敗：" + result.message);
    }
  } catch (err) {
    console.error("上傳錯誤：", err);
    alert("發生錯誤，請稍後再試！");
  } finally {
    updateCSVFileButton.disabled = false;
    updateCSVFileButton.textContent = "送出檔案";
  }
});

const downloadCSVButton = document.getElementById("downCSVButton");
downloadCSVButton.addEventListener("click", async (e) => {
  e.preventDefault();
  downloadCSVButton.disabled = true;
  downloadCSVButton.textContent = "下載中...";

  try {
    function downloadCSV() {
      const url = "https://d1129enkv2st0e.cloudfront.net/example_csv.csv";
      const a = document.createElement("a");
      a.href = url;
      a.download = "example.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
    downloadCSV();
  } catch (err) {
    console.error("錯誤：", err);
    alert("發生錯誤，請稍後再試！");
  } finally {
    downloadCSVButton.disabled = false;
    downloadCSVButton.textContent = "下載 csv example";
  }
});
