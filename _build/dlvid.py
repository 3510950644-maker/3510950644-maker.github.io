import requests
u="http://www.plusxtech.com/upload/cn/video/2026-04/col7/e43b1384d7e4dd7a3779524a127b2dd8.mp4"
H={"User-Agent":"Mozilla/5.0"}
r=requests.get(u,headers=H,timeout=120,stream=True)
print(r.status_code,r.headers.get("content-length"),r.headers.get("content-type"))
r.raise_for_status()
open("_build/company-source.mp4","wb").write(r.content)
print("saved",len(r.content))
