# 页面响应与阅览工具

capture_probe 现有功能仅保存顶层导航原始响应，页面脚本渲染后读取 main；不捕获依赖，不提供离线重写。
AssetStore 用内容摘要保存字节，同时为各 URL 独立记接收事件。EvidenceView 仅提供证据索引和原始字节下载。
本地课程站包含 CSS import、相对背景图、重定向图片、另一来源的 iframe 和 POST lesson。
两个来源均有 /shared/badge.svg，但字节不同。/lesson 的请求体 lesson 会影响响应。
来源授权以 scheme/host/port 为单位；入口清单不隐含授权页面引用的所有其他来源。
Cookie 和 Set-Cookie 是合成会话资料，不能进入可携出的响应头、日志或脚本数据。
原始响应体、导航最终 DOM 和可离线重放交互是三个不同对象，不应互相冒充。
