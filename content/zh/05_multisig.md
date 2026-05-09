# 多签安全：ISC 国库的集体守护机制

单签钱包（普通钱包）存在单点故障风险：私钥丢失或被盗即意味着资产永久归零。为了保障国库安全，ISC 采用了多重签名（Multisig）技术。

### 什么是多签？
多签钱包要求多个独立私钥共同签署才能发起交易。例如 ISC 的国库管理，通常采用 "M-of-N" 模式（如 3/5 模式），即 5 位私钥持有人中必须有 3 位同意，资金才能动用。

### 核心优势：
1. **防止单点故障**：即使其中一个私钥泄露，黑客也无法转走资金。
2. **权力制衡**：避免任何单一成员私自挪用资金，确保国库用于社区建设。
3. **透明可追溯**：每一笔多签操作都在链上公开，社区成员可以随时审计。

**ISC 国库地址**：0x3B79D4A0bd73FCaB12DFEd34dA830b376A50e019
*注：该国库由多签钱包管理，密钥由社区推选的受信成员共同保管。*

权威参考：
- [Safe (Gnosis Safe): 什么是多签钱包？](https://safe.global/)
- [Binance Academy: 什么是多签钱包？](https://academy.binance.com/zh/articles/what-is-a-multisig-wallet)
- [Ethereum.org: 智能合约钱包](https://ethereum.org/zh/dao/#multisig)
