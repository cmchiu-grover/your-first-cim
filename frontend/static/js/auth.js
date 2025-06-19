export async function checkUserData() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    alert("請先登入");
    window.location.href = "/";
    return null;
  }

  try {
    const res = await fetch("/api/user/auth", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) throw new Error("Token invalid");

    const result = await res.json();
    return result.data;
  } catch (err) {
    console.error("使用者驗證失敗:", err);
    alert("請重新登入");
    window.location.href = "/";
    return null;
  }
}
