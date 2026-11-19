# 正宇新材中英双语静态网站

纯静态网站，中文内容来自 <https://www.plusxtech.com/>，英文内容来自其英文站 <https://www.plusxtech.cn/>。沿用原静态站模板的视觉体系（奶油底色、深蓝主色、橙色强调、DM Sans / Noto Sans SC 字体），并扩展为完整的中英双语站点。

## 快速预览

直接双击 `index.html`；或在本目录启动本地服务器：

```powershell
python -m http.server 8080
```

访问 <http://127.0.0.1:8080/>，点击页头右侧的 **中 / EN** 即可切换语言。

## 本次调整

- 已删除「关于我们 → 品质认证」页面及全部入口。
- 已删除「新闻动态」页面及全部新闻文章。
- 已删除「招贤纳士 / 人才理念 / 加入我们」页面及全部入口。
- 已删除「薄膜知识 → 卷取直径/重量计算」页面及全部入口。
- 已删除「薄膜知识 → 视频中心」页面及全部入口（导航、页脚、知识页工具卡）。
- 页头新增 **中 / EN 语言切换**按钮：中文页面对应 `en/` 下的同名英文页，英文页可切回中文。
- 英文文案、产品资料与应用领域内容直接抓取自英文站 plusxtech.cn。

## 页面结构（中英各 30 页）

| 板块 | 页面 |
| --- | --- |
| 首页 | `index.html` |
| 关于我们 | `about.html` |
| 产品中心 | `product-center.html` + 13 个产品详情页（`product-*.html`） |
| 应用领域 | `applications.html` + 10 个行业详情页（`application-*.html`） |
| 薄膜知识 | `knowledge.html`、`faq.html` |
| 其他 | `privacy.html` |

英文页面位于 `en/`，文件名与中文页面一一对应。产品详情覆盖：PSU、PTFE、PFA、FEP、ETFE、PVDF、PEEK 七种原膜，EC 系列、ETFE、PTFE、压敏胶带四种胶带，FP、EP 两种复合膜。

## 内容来源与处理

- 中文：抓取源站 75 个页面（含重复入口），正文逐页抽取。
- 英文：抓取英文站对应页面；英文站没有 **PSU 膜**、**FP 复合膜** 两个产品页，这两页的英文文案由中文内容人工翻译补齐。
- 图片使用本次提供的 `images/` 资源，已压缩为 WebP/JPEG 并输出到 `assets/images/`；关于页宣传片另行放置于 `assets/video/`。
- 产品系列 PDF 保留原站下载链接。
- 关于我们页新增全宽宣传片区：背景为工厂实拍图，左侧公司介绍，右侧播放按钮；中文页播放 `assets/video/company.mp4`，英文页播放 `assets/video/company-en.mp4`。
- 图片放置：产品图用于产品卡片与详情页主视觉；`应用行业页` 各文件夹的产品系列图用于行业页「产品系列」画廊；10 张行业封面图用于应用领域卡片；薄膜知识图用于加工方法卡片；`公司图片` 用作宣传片封面；`产品总图` 用于首页与产品中心页头背景；品牌 Logo 用于页头与页脚（深色/白色两版）。
- 10 张行业封面图取自官网应用领域配图，保存在 `_build/appimg_src/`，由 `prepare_images.py` 统一压缩。
- 常见问题：中文 264 条、英文 232 条，均支持关键词搜索。

## 校验

```text
中文：30 页，缺失正文行 0
英文：30 页，缺失正文行 0
内部链接错误：0
重复 ID：0
语言切换异常：0
标签闭合问题：0
缺失图片：0
iframe：0
宣传片：2（中文 1 个、英文 1 个）
```

校验脚本：`_build/verify.py`（正文逐行比对）、`_build/check.py`（链接、ID、图片文件、标签平衡与语言切换检查）。

## 目录说明

```
index.html …            中文页面
en/                     英文页面（30 页）
styles.css              全站样式
script.js               移动端导航
faq.js                  常见问题搜索（中英双语）
_backup-original/       改造前的旧模板文件（备份）
_build/
  source-pages.json     中文源站页面正文缓存
  en_pages.json         英文源站页面正文缓存
  content.json          中文结构化内容
  content-en.json       英文结构化内容
  extract.py            中文正文抽取
  extract_en.py         英文正文抽取
  build.py              中英双语页面生成
  verify.py             正文完整性校验
  check.py              链接 / 结构 / 图片 / 语言切换检查
  appimg_src/           官网行业封面原图（10 张）
  about-bg-source.jpg   关于页宣传片区背景原图
  company-source.mp4    中文宣传片源文件（26MB）
  company-en-source.mp4 英文宣传片源文件（19MB）
  prepare_images.py     从 images/ 与 appimg_src/ 生成 assets/images/ 与 images.json
  images.json           图片路径与中英文名称清单
```

## 重新生成

```powershell
# 如 images/ 有更新，先重新生成优化后的站点图片
python _build/prepare_images.py

# 再生成中英文页面
python _build/build.py
```

页面会同时输出到根目录（中文）和 `en/`（英文）。

## 说明

- 页面中的电话、邮箱、地址、备案号、版权信息均取自源站。
- 英文站部分原文存在拼写或空格问题（例如 `film.By`、`ngineered`），为保持“原文照录”未作改写。
- 字体通过 Google Fonts 引入，离线时回退到系统中文字体。
- 旧版文件已备份在 `_backup-original/`。
# 3510950644-maker.github.io
