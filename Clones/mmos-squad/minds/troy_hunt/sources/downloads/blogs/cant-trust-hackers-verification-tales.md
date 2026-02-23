# You Can't Trust Hackers, and Other Data Breach Verification Tales
**Date:** January 23, 2025
**Source:** https://www.troyhunt.com/you-cant-trust-hackers-and-other-data-breach-verification-tales/
**Category:** Methodology & Process

Troy Hunt describes a recent attempt to defraud him involving a claimed JB Hi-Fi data breach affecting 12+ million Australian customers. A threat actor contacted Hunt claiming to possess the compromised dataset and demanded $16,000 for access.

Hunt requested verification by asking the attacker to share his own customer record. The individual provided sample records containing 14 data columns including names, emails, addresses, and account information. When Hunt analyzed the email addresses using the Have I Been Pwned API, he discovered a significant red flag: nearly 100% of addresses shared one breach in common.

Upon comparison with the actual Dymocks bookstore breach from mid-2023, Hunt found that the "JB Hi-Fi" dataset was nearly identical to the previously known Dymocks compromise. The threat actor had simply recycled old breach data and rebranded it as a new incident. When Hunt presented this evidence, the conversation ended abruptly and the listing disappeared.

Hunt emphasizes the importance of verifying data breach claims through cross-referencing historical breach data. He notes that recycled datasets frequently circulate through criminal networks, often misrepresented as fresh compromises. This case exemplifies how data security experts can expose fraudulent claims using established breach repositories.
