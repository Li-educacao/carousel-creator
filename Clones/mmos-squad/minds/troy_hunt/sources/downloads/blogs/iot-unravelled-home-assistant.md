# IoT Unravelled Part 1: It's a Mess... But Then There's Home Assistant
**Date:** November 23, 2020
**Source:** https://www.troyhunt.com/iot-unravelled-part-1-its-a-mess-but-then-theres-home-assistant/
**Category:** Communication Style / Misc

Troy Hunt documents his journey attempting to connect garage door openers to a smart home system, discovering that the IoT landscape is fragmented across competing proprietary ecosystems. What he expected to be a straightforward task became a 123-day odyssey involving multiple platforms and technologies.

## The Problem: Everyone Wants to Be "The IoT Solution"

The fundamental challenge stems from competing platforms. Apple's HomeKit, Amazon Alexa, and Google Home each operate as closed ecosystems with limited device support. Hunt notes that "every single one is a proprietary ecosystem with fragmented support by different devices and a kludge of vendor lock-in."

Grid Connect lights he purchased supported only Amazon and Google, excluding HomeKit entirely. Control4 offered another hub option but required professional installation.

## Home Assistant as the Answer

Home Assistant (HA) represents a philosophically different approach. As an open-source project, it "puts local control and privacy first" and runs on Raspberry Pi hardware. Rather than pushing users toward specific vendors, HA integrates disparate devices into a unified system.

However, Hunt acknowledges significant drawbacks: "The learning curve is steep, it has a bunch of rough edges...and by any reasonable measure, it's only usable by geeks."

## Core Concepts: Integrations, Devices, Entities, Automations

HA organizes IoT functionality through distinct layers:

- **Integrations** enable communication with various devices and services
- **Devices** are physical units (motion sensors, lights, relays)
- **Entities** represent individual measurements or controls within devices
- **Automations** define conditional triggers and actions
- **Scenes** group multiple pre-set states for simultaneous activation

Hunt demonstrates this with motion sensors controlling stairwell lights through automated rules.

## Device Compatibility Across Brands

Hunt discovered that seemingly different products often share underlying hardware. Grid Connect and Arlec lights both use Tuya's ESP8266-based platform, making them compatible across multiple apps despite different branding.

This allowed him to control devices through:
- Native manufacturer applications
- Tuya's unified platform
- Home Assistant integrations
- Third-party ecosystems like Alexa and HomeKit

## Multi-Hub Integration

Rather than replacing other platforms, HA bridges between them. Using integrations like the HomeKit Bridge and Amazon Alexa integration, Hunt surfaces HA devices into other ecosystems, enabling voice control through Siri and Alexa despite underlying devices lacking native support.

This creates complexity: "You inevitably end up with multiple different interfaces into the same device be they native interfaces...or those exposed via the HA integration."

## Troubleshooting Challenges

The layered approach creates diagnostic difficulties. When an HS100 smart plug showed "No Response" in HomeKit, Hunt had to trace the issue through multiple systems: HomeKit Bridge integration, HA entity status, native Kasa app responsiveness, and network connectivity—each requiring different troubleshooting approaches.

## Conclusion

Hunt concludes that despite complexity, Home Assistant offers the most cohesive approach to IoT integration. The series continues with networking, Zigbee protocol, custom firmware, and security considerations in subsequent parts.
