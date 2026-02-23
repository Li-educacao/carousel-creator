# Passkeys for Normal People
**Date:** May 5, 2025
**Source:** https://www.troyhunt.com/passkeys-for-normal-people/
**Category:** Technical Deep-Dive

Troy Hunt explains passkeys as a solution to phishing-resistant authentication. He begins by describing a common security scenario: entering credentials and 2FA codes, which are vulnerable to phishing attacks.

## The Problem with Current Authentication

Hunt illustrates how he fell victim to a phishing attack on Mailchimp. The attacker created a fake login page, intercepted his credentials, and captured his two-factor authentication code by proxying the legitimate login process. This demonstrates that "OTPs from authenticator apps (or sent via SMS) is that they're phishable."

## Setting Up Passkeys

**WhatsApp Example (Mobile):** Hunt walks through creating a passkey on iPhone, explaining that passkeys are digital files with cryptographic protections. He opted to store his in 1Password rather than Apple's iCloud Keychain to maintain cross-device compatibility.

**LinkedIn Example (Web):** LinkedIn's implementation required password re-entry and email verification before generating a passkey. However, Hunt notes a significant limitation: "you can still log in with" the password and "2FA, you're still at risk of the same sort of attack."

**Ubiquiti Example (Second Factor):** Ubiquiti allows passkeys to completely replace traditional 2FA, enabling Hunt to delete his authenticator app.

## Physical Security Keys

Hunt demonstrates adding a YubiKey (U2F hardware key) as an additional layer. He explains that while passkeys themselves are non-phishable, "what happens if the place you store that digital key gets compromised?" Physical keys provide offline backup security.

## Finding Support

Hunt references passkeys.directory, which catalogs services supporting passkeys, and encourages users to vote for their preferred services to adopt the technology.

## Conclusion

Hunt emphasizes that "passkeys are one of the few security constructs that make your life easier, rather than harder." He advocates for immediate adoption on essential services and encourages broader implementation, noting Microsoft's recent announcement about passwordless default accounts.
