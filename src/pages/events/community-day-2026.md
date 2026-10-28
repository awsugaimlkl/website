---
layout: ../../layouts/CommunityDayLayout.astro
title: "AWS Community Day AI/ML Edition 2026"
description: "A community-led day for AI/ML builders, practitioners, students and technology leaders to learn, share and connect."
date: "2026-11-14"
dateDisplay: "Saturday, 14 November 2026"
time: "9:00 AM – 5:00 PM"
startTime: "09:00"             # the countdown on the page runs to this time
endTime: "17:00"
venue: "Sunway University, Selangor"
address: "No. 5, Jalan Universiti, Bandar Sunway, 47500 Selangor, Malaysia"
mapUrl: "https://www.google.com/maps/search/?api=1&query=Sunway+University"
calendarFile: "/community-day-2026.ics"
featured: true
summary: "The first AWS Community Day AI/ML Edition organized by AWS User Group AI/ML Kuala Lumpur."
photo: "2026-05-meetup-wide"
photoAlt: "A speaker presents to a full room of attendees under hexagon-shaped ceiling lights"
photoCaption: "Our May 2026 meetup at Xendit Malaysia."

# Banner across the top of the page. Put a # in front of these lines to take it down.
# To have it come down by itself, add a last day to show it:   until: "2026-10-31"
banner:
  text: "Event Registration is now Open"
  linkText: "Register now"
  url: "https://forms.gle/PqskpHoJMyNsWRjS6"

# Call for speakers. While this line is here, the page shows "Apply to speak" buttons.
# Put a # in front of it when the call closes.
callForSpeakersUrl: "https://forms.gle/Uf1Hd2cmpmfuyzK88"

# Topics shown under the call for speakers.
topics:
  - "Generative AI"
  - "Agentic AI"
  - "Amazon Bedrock"
  - "Amazon SageMaker"
  - "Machine learning"
  - "MLOps"

# Registration form. While this line is here, Register buttons show at the top of the page
# and in the Registration section. Put a # in front of it when registration closes.
registrationUrl: "https://forms.gle/PqskpHoJMyNsWRjS6"

# Short points shown under the About text.
highlights:
  - title: "Run by the community"
    text: "Planned and delivered by volunteers from the user group."
  - title: "Technical sessions"
    text: "Talks on AI, machine learning, generative AI and agentic AI."
  - title: "Real-world experience"
    text: "AWS architectures and implementations, shared by the people who built them."
  - title: "People to meet"
    text: "Time with speakers, community leaders and fellow AI/ML practitioners."

# Speakers. speakerSlots is how many profiles the page shows. Slots without a speaker
# yet are shown as "Speaker to be announced". Set it to 0 to show only confirmed speakers.
speakerSlots: 6

# One entry per speaker, shown in this order.
# photo is a file name in src/assets/speakers without the extension; leave it out to show initials.
# Example:
#   - name: "Full name"
#     role: "Job title"
#     affiliation: "Company or university"
#     talk: "Talk title"
#     linkedin: "https://www.linkedin.com/in/..."
#     photo: "full-name"
speakers:
  - name: "Mohanahari Mohan"
    role: "Platform Engineer"
    affiliation: "Maybank"
    talk: "AI-Powered API Discovery, the Road to AGI, and Quantum Computing on AWS"
    linkedin: "https://www.linkedin.com/in/czhari/"
    photo: "mohanahari-mohan"
  - name: "Mirza Rayana Sanzana"
    role: "Applied AI Researcher and Lecturer"
    affiliation: "Monash University"
    talk: "Your Model Worked Yesterday: Detecting ML Drift with Amazon SageMaker AI"
    linkedin: "https://www.linkedin.com/in/mirza-rayana-sanzana"
    photo: "mirza-rayana-sanzana"
  - name: "Weiyuan Liu"
    role: "Director of Engineering"
    affiliation: "Ascenda"
    talk: "AWS DevOps Agent, more than just another AI tool"
    linkedin: "https://www.linkedin.com/in/liuweiyuan/"
    photo: "weiyuan-liu"
  - name: "Shah Hassan"
    role: "Head of Engineering"
    affiliation: "NTT Data eCommerce Solutions Sdn Bhd"
    talk: "Can AI Stop Bad Code and Investigate Production Incidents? : From Code Review to Platform Intelligence with Kiro & AWS"
    linkedin: "https://www.linkedin.com/in/tsshahhassan"
    photo: "shah-hassan"
  - name: "Puteri Irene Alia binti Abdul Hadi"
    role: "AI Developer & AI Governance"
    affiliation: "DRB-HICOM"
    talk: "Building Autonomous AI Agents with Amazon Bedrock AgentCore and How to Govern Them Before They Go Live"
    linkedin: "https://www.linkedin.com/in/puteri-irene-alia-abdul-hadi-586a67a7/"
    photo: "puteri-irene-alia"
  - name: "Fahim Surani"
    role: "APJ Head of Solutions Architecture"
    affiliation: "Arize AI"
    talk: "Jev is all you need*"
    linkedin: "https://www.linkedin.com/in/fahim-surani/"
    photo: "fahim-surani"

# Schedule. One entry per slot, in order, from the proposed agenda of 27 October 2026.
# An entry with "placeholder: true" is marked "To be announced" on the page.
# speaker is the line under the title. A talk looks like this:
#   - time: "10:00 AM – 10:45 AM"
#     title: "Talk title"
#     speaker: "Speaker name, Company"
agendaNote: "Session times and the keynote speaker are subject to confirmation."
agenda:
  - time: "9:00 AM – 9:30 AM"
    title: "Registration and welcome"
  - time: "9:30 AM – 10:00 AM"
    title: "Opening remarks and keynote"
    speaker: "Keynote speaker to be announced"
  - time: "10:00 AM – 10:45 AM"
    title: "AWS DevOps Agent, more than just another AI tool"
    speaker: "Weiyuan Liu, Ascenda"
  - time: "10:45 AM – 11:00 AM"
    title: "Morning break"
  - time: "11:00 AM – 11:45 AM"
    title: "Can AI Stop Bad Code and Investigate Production Incidents? : From Code Review to Platform Intelligence with Kiro & AWS"
    speaker: "Shah Hassan, NTT Data eCommerce Solutions Sdn Bhd"
  - time: "11:45 AM – 12:30 PM"
    title: "Building Autonomous AI Agents with Amazon Bedrock AgentCore and How to Govern Them Before They Go Live"
    speaker: "Puteri Irene Alia binti Abdul Hadi, DRB-HICOM"
  - time: "12:30 PM – 1:30 PM"
    title: "Lunch break"
  - time: "1:30 PM – 2:15 PM"
    title: "Your Model Worked Yesterday: Detecting ML Drift with Amazon SageMaker AI"
    speaker: "Mirza Rayana Sanzana, Monash University"
  - time: "2:15 PM – 3:00 PM"
    title: "Jev is all you need*"
    speaker: "Fahim Surani, Arize AI"
  - time: "3:00 PM – 3:15 PM"
    title: "Afternoon break"
  - time: "3:15 PM – 4:00 PM"
    title: "AI-Powered API Discovery, the Road to AGI, and Quantum Computing on AWS"
    speaker: "Mohanahari Mohan, Maybank"
  - time: "4:00 PM – 4:15 PM"
    title: "Closing remarks and group photo"
  - time: "4:15 PM – 5:00 PM"
    title: "Community networking"

# Sponsors and partners. Entries with the same tier are grouped under one heading.
# logo is a file name in src/assets/sponsors without the extension; leave it out to show the name.
# Example:
#   - name: "Company name"
#     tier: "Gold sponsor"
#     url: "https://..."
#     logo: "company-name"
sponsors:
  - name: "Konfx"
    tier: "Official sponsor"
    url: "https://www.konfx.io/"
    logo: "konfx"

# Volunteer team, the last section on the page. volunteerSlots is how many tiles it shows.
# Tiles without a volunteer yet read "Volunteer to be announced". Set it to 0 to show only
# named volunteers; with 0 and no volunteers the section is left out.
volunteerSlots: 0

# One entry per volunteer, shown in this order. linkedin is optional.
# photo is a file name in src/assets/volunteers without the extension: a finished tile
# made with tools/volunteer-tiles (the person as a comic-book superhero on the skyline).
# Without a photo, the tile shows the skyline silhouette above the name.
# Example:
#   - name: "Full name"
#     photo: "full-name"
#     linkedin: "https://www.linkedin.com/in/..."
volunteers:
  - name: "Tuan Nur Sumayyah Binti Roseli"
    photo: "tuan-nur-sumayyah"
  - name: "Fatin Najdah"
    photo: "fatin-najdah"
  - name: "Ruben Chong"
    photo: "ruben-chong"
  - name: "Yap Hock Seng"
    photo: "yap-hock-seng"
  - name: "Chan Kar Fong"
    photo: "chan-kar-fong"
  - name: "Chong Hun Yee"
    photo: "chong-hun-yee"
  - name: "Jerry Chong"
    photo: "jerry-chong"
  - name: "Lavanesswary"
    photo: "lavanesswary"
  - name: "Edelyn Seah"
    photo: "edelyn-seah"
  - name: "Muhammad Fikhri"
    photo: "muhammad-fikhri"

venueNote: "The building and room will be confirmed closer to the event."
gettingThere:
  - how: "By BRT and LRT"
    text: "The closest station is SunU-Monash on the BRT Sunway Line. The BRT connects to the LRT Kelana Jaya Line at USJ 7."
  - how: "By car"
    text: "Parking is available in the university basement and at the BRT Park and Ride at SunU-Monash station."
  - how: "On foot from Sunway City"
    text: "A covered, elevated walkway links the campus to the rest of Bandar Sunway."
---

AWS Community Day AI/ML Edition 2026 brings together the local artificial intelligence, machine learning and cloud community for a full day of technical talks, practical demonstrations, community sharing and networking.

This is the first Community Day organized by AWS User Group AI/ML Kuala Lumpur. AWS Community Days are planned and delivered by user groups, and the talks come from people who use AWS in their daily work.
