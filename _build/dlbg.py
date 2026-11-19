import requests
u="http://www.plusxtech.com/upload/cn/image/2025-04/col7/1744102976917.jpg"
r=requests.get(u,headers={"User-Agent":"Mozilla/5.0"},timeout=60)
print(r.status_code,len(r.content),r.headers.get("content-type"))
open("_build/about-bg-source.jpg","wb").write(r.content)
