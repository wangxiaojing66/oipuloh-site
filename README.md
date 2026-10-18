# Oipuloh 品牌官网

为 Amazon Ads API 申请准备的公司网站。静态站点，无追踪脚本、无购物车；商品页链接回 Amazon 完成购买。

## 本地预览

```bash
cd "/Users/q/Music/Codex/Codex 亚马逊/Oipuloh_官网"
python3 -m http.server 4173
```

打开 http://localhost:4173

## 修改联系信息与域名

编辑 `site.config.json`：

- `domain`：正式域名，必须带 `https://`，用于 canonical、sitemap、OG。
- `email`：真实可收信邮箱。当前为 `wangxiaojing66@outlook.com`。
- `legalName`：与 Ads API 表单中“公司法定名称”一致。当前为 `衡阳燧石蜂贸易有限公司`。
- `amazonSearch`：品牌 Amazon 搜索链接；可替换为 Amazon Storefront 链接。

改完运行：

```bash
python3 build.py
```

## 已上线预览

- 预览地址：https://wangxiaojing66.github.io/oipuloh-site/
- 仓库：https://github.com/wangxiaojing66/oipuloh-site
- GitHub Pages 已开启并强制 HTTPS。
- 预览构建使用 `SITE_DOMAIN=https://wangxiaojing66.github.io/oipuloh-site`，canonical 与 sitemap 指向预览地址。

后续更新：

```bash
cd "/Users/q/Music/Codex/Codex 亚马逊/Oipuloh_官网"
SITE_DOMAIN='https://wangxiaojing66.github.io/oipuloh-site' python3 build.py
git add .
git commit -m "Update site"
git push
```

## 绑定自有域名（推荐）

1. 注册 `oipuloh.com`（当前未注册）。
2. 在 GitHub Pages 设置里填 Custom domain，并按提示添加 DNS：
   - `A` 记录到 GitHub Pages 的四个 IP；
   - `CNAME` 将 `www` 指向 `<username>.github.io`。
3. 开启 Enforce HTTPS。
4. 把 `site.config.json` 的 `domain` 改为 `https://oipuloh.com`，运行 `python3 build.py`（不要带 `SITE_DOMAIN`），提交并推送。

## Ads API 表单填写建议

- 公司法定名称：`衡阳燧石蜂贸易有限公司`。
- 公司网站：最终用 `https://oipuloh.com`；审核前不建议用 github.io 预览地址。
- 品牌名称：`Oipuloh`。
- 国家/地区：按注册主体选择。
- 广告账户所在站点：勾选 `美国`。

## 内容事实来源

- 商品标题、材质、尺寸、包含物、卖点：SP-API Catalog Items（2026-09-27 快照，`_analysis/current_20260927/*_catalog.json`）。
- 主图与细节图：SP-API Catalog Images，下载后仅做尺寸压缩，未改变产品外观。
- 站点文案只使用可核实的描述；没有虚构评价、销量、认证、折扣或价格。
