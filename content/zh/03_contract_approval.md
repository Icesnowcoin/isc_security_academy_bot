# 合约授权风险：别给 DApp "无限额度"

当你使用 DEX 或借贷协议时，必须先进行 "Approve"（授权）。许多项目为了用户体验，默认请求 "无限授权"，这实际上是一把双刃剑。

### 核心风险：
1. **无限授权**：一旦授权，该合约就有权在任何时候移动你钱包中对应的资产，无需再次确认。
2. **合约漏洞/后门**：如果项目方作恶或合约存在漏洞，黑客可以利用你之前的授权直接划走你的资产，即使你当时并未在线。

### 安全建议：
- **按需授权**：在交互时手动修改授权额度，仅允许合约动用本次交易所需的金额。
- **定期清理**：使用 **Revoke.cash** 或区块浏览器（如 BscScan）的 Approval Checker 工具，定期取消不再使用的 DApp 授权。
- **钱包隔离**：将长期持有的资产存放在不参与 DApp 交互的冷钱包或独立钱包中。

权威参考：
- [Revoke.cash: 为什么需要撤销授权？](https://revoke.cash/zh/learn/approvals)
- [Metamask: 什么是代币授权？](https://support.metamask.io/hc/en-us/articles/4405104049819)
- [CertiK: 理解智能合约授权风险](https://www.certik.com/resources/blog)
