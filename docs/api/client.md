---
title: Client API Reference
description: Explore the unified client interface in CTFBridge. Learn how to initialize the client and access services like authentication, challenges, scoreboard, and more via a structured API.
---

# API Reference

This page documents the unified interface available via the `ctfbridge` client.

All functionality is grouped by feature and accessed through submodules of the client object.

---

## 🚀 Initializing the Client

::: ctfbridge.factory

---

## 🔑 `client.auth`

::: ctfbridge.base.services.auth.AuthService

---

## 📋 `client.challenges`

::: ctfbridge.base.services.challenge.ChallengeService

---

## 📎 `client.attachments`:

::: ctfbridge.base.services.attachment.AttachmentService

---

## 🏆 `client.scoreboard`:

::: ctfbridge.base.services.scoreboard.ScoreboardService

---

## 🌐 `client.session`

::: ctfbridge.base.services.session.SessionHelper

## ✨ `client.capabilities`

The `capabilities` property provides a synchronous way to check which features are supported by the current platform client. It returns a `Capabilities` object.

::: ctfbridge.models.capability.Capabilities
