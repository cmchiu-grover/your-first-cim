# frontend/Dockerfile

# 使用一個輕量級的 Nginx 作為基礎映像
FROM nginx:alpine

# 將本地的定制化 nginx.conf 複製到容器中 Nginx 的配置目錄
# 這會替換掉容器中默認的 nginx.conf 文件
COPY nginx.conf /etc/nginx/nginx.conf

# 將本地的 static/ 目錄下的所有靜態文件複製到容器中 Nginx 的默認靜態文件服務目錄
# Nginx 會從 /usr/share/nginx/html/ 這個目錄提供文件服務 (root 指令指定)
COPY static/ /usr/share/nginx/html/

# 暴露容器內部 Nginx 監聽的 80 端口
EXPOSE 80

# CMD 指令不需要，Nginx 基礎映像已經有默認的啟動命令來運行 Nginx 進程
# CMD ["nginx", "-g", "daemon off;"] # 默認 CMD 示例，保持 Nginx 在前台運行