# Inside the Massive Alleged AT&T Data Breach
**Date:** March 19, 2024
**Source:** https://www.troyhunt.com/inside-the-massive-alleged-att-data-breach/
**Category:** Technical Deep-Dive

Troy Hunt examines a significant data breach involving AT&T customer information that surfaced in August 2021. Initially claimed to contain 70 million records, the dataset was posted to a hacking forum by a threat actor seeking a substantial payment.

## Data Verification

Hunt verified the breach's authenticity by leveraging his Have I Been Pwned (HIBP) subscriber base. Of approximately 4.8 million subscribers, 153,000 appeared in the dataset. He contacted recent subscribers to confirm accuracy and found their personal information was correctly recorded, including names, addresses, phone numbers, and social security numbers.

## Dataset Details

The primary file contained 73.5 million lines with 49.1 million unique email addresses. Supplementary files revealed encrypted social security numbers (43.9 million records) and dates of birth (43,524 entries). The encrypted values in the supplementary files corresponded directly to encrypted data in the main dataset, suggesting whoever obtained the information also possessed the encryption key.

## AT&T's Response

AT&T maintained the data did not originate from their systems. However, Hunt notes that "absence of evidence is not evidence of absence," emphasizing that unproven claims don't negate the breach's reality.

## Public Accessibility

The data appeared on a publicly accessible forum rather than the dark web, making it easily discoverable through standard browsers. This represents a significant escalation in exposure risk.

## Recommendations

Hunt suggested impacted individuals consider identity theft protection services and request personal data copies from AT&T, regardless of the company's denial. He emphasized that HIBP stores only email addresses—never additional personal information—to mitigate risks if the service itself were compromised.

## Update

On March 31, AT&T released a statement acknowledging that "AT&T data-specific fields were contained in a data set," though the source remained unclear. The company estimated the breach affected approximately 7.6 million current account holders and 65.4 million former customers, dating to 2019 or earlier.
