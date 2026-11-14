---
name: billing-automation
description: abonelik, stripe/iyzico faturalama, webhook isleme ve kurumsal odeme otomasyonu.
when_to_use: "tekrarlayan odemeler, fatura yonetimi ve e-ticaret odeme boru hatlari kurulurken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# billing-automation — kurumsal sistem, yapay zeka ve otomasyon standardi

> 46 p0 kuralina ve sifir varsayim ilkesine bagli kurumsal sistem kalibi.

# Billing Automation

Master automated billing systems including recurring billing, invoice generation, dunning management, proration, and tax calculation.

## Use this skill when

- Implementing SaaS subscription billing
- Automating invoice generation and delivery
- Managing failed payment recovery (dunning)
- Calculating prorated charges for plan changes
- Handling sales tax, VAT, and GST
- Processing usage-based billing
- Managing billing cycles and renewals

## Do not use this skill when

- You only need a one-off invoice or manual billing
- The task is unrelated to billing or subscriptions
- You cannot change pricing, plans, or billing flows

## Instructions

- Define plans, pricing, billing intervals, and proration rules.
- Map subscription lifecycle states and renewal/cancellation behavior.
- Implement invoicing, payments, retries, and dunning workflows.
- Model taxes and compliance requirements per region.
- Validate with sandbox payments and reconcile ledger outputs.
- If detailed templates are required, open `resources/implementation-playbook.md`.

## Safety

- Do not charge real customers in testing environments.
- Verify tax handling and compliance obligations before production rollout.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and examples.
