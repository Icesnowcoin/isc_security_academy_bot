# Contract Approval Risks: Don't Give DApps "Unlimited Credit"

When using DEXs or lending protocols, you must first "Approve" the contract. Many projects request "unlimited approval" for a better user experience, but this can be a double-edged sword.

### The Core Risks
An **unlimited approval** allows a contract to move the corresponding asset from your wallet at any time without further confirmation. If a project turns out to be a scam or its contract has a **vulnerability**, hackers can exploit your previous approval to drain your assets even when you are offline.

### Safety Recommendations
- **Custom Spending Limits**: Manually adjust the approval amount during interaction to match only what is needed for the current transaction.
- **Regular Revocation**: Use tools like **Revoke.cash** or block explorer approval checkers (e.g., BscScan) to regularly cancel approvals for DApps you no longer use.
- **Wallet Isolation**: Store long-term holdings in a cold wallet or a separate address that does not interact with DApps.

### Authoritative References
- [Revoke.cash: Why Should I Revoke?](https://revoke.cash/learn/approvals)
- [MetaMask: What is a Token Approval?](https://support.metamask.io/hc/en-us/articles/4405104049819)
- [CertiK: Understanding Smart Contract Approvals](https://www.certik.com/resources/blog)
