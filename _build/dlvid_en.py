import requests
u="http://www.plusxtech.cn/upload/en/video/2025-04/col68/1743582379070.mp4"
r=requests.get(u,headers={"User-Agent":"Mozilla/5.0"},timeout=180,stream=True)
print(r.status_code,r.headers.get("content-length"),r.headers.get("content-type"))
r.raise_for_status(); open("_build/company-en-source.mp4","wb").write(r.content); print("saved",len(r.content))
