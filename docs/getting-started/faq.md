---
title: Frequently Asked Questions
description: Find answers to common questions about CTFBridge, including installation, supported platforms, usage, contributions, and more.
---

# ❓ Frequently Asked Questions (FAQ)

This page provides answers to common questions about CTFBridge. If you don't find your answer here, feel free to [open an issue on GitHub](https://github.com/bjornmorten/ctfbridge/issues).

---

### **Q1: What is CTFBridge?**

**A:** CTFBridge is a Python library designed to provide a unified, consistent interface for interacting with various Capture The Flag (CTF) platforms. It allows you to automate tasks like fetching challenges, submitting flags, and accessing scoreboard data across different CTF systems without needing to learn each platform's specific API.

---

### **Q2: Which CTF platforms are currently supported?**

**A:** CTFBridge supports several popular platforms, including CTFd, rCTF, HTB (Hack The Box CTF events), Berg, and EPT. For a detailed and up-to-date list, please see our [Supported Platforms](platforms.md) page.

---

### **Q3: How do I install CTFBridge?**

**A:** You can install CTFBridge using pip:

```bash
pip install ctfbridge
```

---

### **Q4: Do I need to know which platform a CTF is running on to use CTFBridge?**

**A:** Not necessarily! CTFBridge includes an automatic platform detection feature. You can usually just provide the base URL of the CTF, and the library will attempt to identify the platform and use the correct adapter. You can also specify the platform manually if you know it.

---

### **Q5: Is CTFBridge synchronous or asynchronous?**

**A:** CTFBridge is designed with an async-first approach, making it suitable for I/O-bound operations typically found in web interactions and ideal for modern automation scripts and tools. All primary interactions with the client will use `async` and `await`.

---

### **Q6: Can I save and load my session (e.g., login cookies)?**

**A:** Yes, CTFBridge provides session management capabilities, including saving your current session (cookies, headers) to a file and loading it later. This allows for persistent sessions across script runs.

---

### **Q7: How can I contribute to CTFBridge?**

**A:** Contributions are very welcome! We appreciate help with bug reports, feature requests, code enhancements, documentation improvements, or adding support for new platforms. Please read our [Contributing Guidelines](https://github.com/bjornmorten/ctfbridge/blob/main/CONTRIBUTING.md) to get started.

---

### **Q8: Where can I find detailed API documentation?**

**A:** You can find detailed documentation for the client interface and data models in the [API Reference section](../api/index.md) of our documentation.

---

### **Q9: What if a CTF platform I use isn't supported?**

**A:** CTFBridge is designed to be extensible. If you'd like to add support for a new platform, please refer to our [Developer Guide on Platform Integration](../dev/platforms.md). You can also open a feature request on our [GitHub issues page](https://github.com/bjornmorten/ctfbridge/issues).

---

### **Q10: What is "Challenge Enrichment"?**

**A:** Challenge enrichment refers to the process where CTFBridge attempts to extract additional useful information from challenge data that might not be explicitly provided by the platform's API in a structured way. This can include parsing authors, attachments, or service details (like `nc host port`) directly from challenge descriptions.
