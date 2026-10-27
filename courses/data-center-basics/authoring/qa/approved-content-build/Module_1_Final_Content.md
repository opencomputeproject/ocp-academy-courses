# Module 1 · The Digital World

## M1S1 · The Digital World

{
  "id": 1,
  "type": "title",
  "slug": "the_digital_world",
  "title": "The Digital World",
  "subtitle": "From a familiar service to its physical foundations.",
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 1
    }
  ]
}

Narration:
Module one: The Digital World. Every digital service depends on physical infrastructure. You'll follow that connection from a familiar application to the facility, equipment, electricity and networks behind it. You'll also distinguish facility types, resilience capabilities and cloud services, so the terms describe something concrete.


## M1S2 · Follow the Service, Facility, Rack and Operations

{
  "id": 2,
  "type": "course_overview",
  "slug": "course_overview",
  "title": "Follow the Service, Facility, Rack and Operations",
  "subtitle": "Four connected questions about the systems behind digital services.",
  "modules_listed": [
    "The Digital World",
    "Data Center Physical Infrastructure",
    "Inside the Rack",
    "Management and Trends"
  ],
  "chips": [
    {
      "text": "About 90–95 minutes"
    },
    {
      "text": "Introductory"
    },
    {
      "text": "Narration, videos and knowledge checks"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 1
    },
    {
      "source": "rise_m1",
      "lesson": 2
    }
  ]
}

Narration:
This course follows four connected questions. What does a data center do? What keeps its equipment running? How does that equipment fit into a rack? And how do people operate and improve the whole system?

You'll work through those questions in four modules. Short narrated explanations connect the concepts, while the videos provide longer examples. Knowledge checks give you feedback and a chance to retry. Together, the modules prepare you to explore how the Open Compute Project develops shared approaches to infrastructure.


## M1S3 · A First Look at Physical Infrastructure

{
  "id": 3,
  "type": "content_diagram",
  "slug": "course_introduction_video",
  "section_label": "Introduction",
  "title": "A First Look at Physical Infrastructure",
  "media_focus": true,
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 2,
      "block": 3
    }
  ],
  "glossary_usage_review": "Reviewed against slide text, current narration, transcribed video speech and hash-bound media text inventory.",
  "glossary_exclude_reason": "course orientation",
  "narration_enabled": false
}

Imported recording transcript:
Welcome to the data center infrastructure that keeps the digital world running. In this lesson, we'll explore the key physical components at a high level that make a data center function: power, cooling, and layout. Let's imagine a data center building and dissect the key components from the outside in. The first layers include power and cooling facilities. We'll start with power. Data centers have powerful energy systems designed to keep operations running 24/7, 365 days a year. From generators and UPSes, batteries, to distribution switchgear, the power infrastructure is a critical system that supplies energy to all the equipment in the data center. Now on to the cooling infrastructure. Chillers, condensers, and air handling units that help manage temperature and humidity on the data center floor so that the systems don't overheat or shut down. These systems don't work in isolation. Every part of the data center is connected through cables, power rails, busways, and energy management systems. They ensure that power is delivered efficiently to the rack. Then comes rack level distribution. This is where the actual compute happens, and a lot of the energy is consumed and heat is generated. Servers are arranged in enclosures where hot and cold air is separated. Cooling via localized air or liquid is constantly monitored with smart sensors and software. All of this is maintained and monitored by systems that control real-time adjustments, alarm, and automation. Think of it as the nervous center of the data center. In the next lesson, we'll go deeper into specific subsystems like power and cooling, but now you should have a bird's-eye view of how all the parts come together to create an always-on environment.

Media:
{
  "path": "resources/videos/module1/1-1-welcome-course-overview-1080p.mp4",
  "poster": "resources/images/module1/video-slide-3-poster.jpg",
  "media_type": "video",
  "role": "original_video",
  "source": "reuse",
  "autoplay": false,
  "loop": false,
  "muted": false,
  "controls": true,
  "alt": "A First Look at Physical Infrastructure video.",
  "caption": "Power, cooling, layout and monitoring work together to support the equipment.",
  "source_sha256": "5b801d149090e45cdc130376f9ef4dbc2ef3fe3f3c45129f6a4a49d173784393",
  "captions": [
    {
      "path": "resources/captions/module1/1-1-welcome-course-overview-1080p.vtt",
      "language": "en",
      "label": "English (transcribed)"
    }
  ],
  "caption_cues": [
    {
      "start": 3.14,
      "end": 6.22,
      "text": "Welcome to the data center infrastructure\nthat keeps the digital world"
    },
    {
      "start": 6.34,
      "end": 9.78,
      "text": "running. In this lesson, we'll explore the\nkey physical"
    },
    {
      "start": 9.86,
      "end": 13.74,
      "text": "components at a high level that make a\ndata center function: power,"
    },
    {
      "start": 13.88,
      "end": 17.74,
      "text": "cooling, and layout. Let's imagine a data\ncenter building"
    },
    {
      "start": 17.92,
      "end": 21.84,
      "text": "and dissect the key components from the\noutside in. The first"
    },
    {
      "start": 21.9,
      "end": 25.64,
      "text": "layers include power and cooling\nfacilities. We'll start with power."
    },
    {
      "start": 27.12,
      "end": 31.12,
      "text": "Data centers have powerful energy systems\ndesigned to keep operations running"
    },
    {
      "start": 31.34,
      "end": 35.3,
      "text": "24/7, 365 days a year. From"
    },
    {
      "start": 35.42,
      "end": 39.22,
      "text": "generators and UPSes, batteries, to\ndistribution switchgear,"
    },
    {
      "start": 40.32,
      "end": 44.32,
      "text": "the power infrastructure is a critical\nsystem that supplies energy to all the"
    },
    {
      "start": 44.36,
      "end": 48.06,
      "text": "equipment in the data center. Now on to\nthe cooling infrastructure."
    },
    {
      "start": 49.9,
      "end": 53.56,
      "text": "Chillers, condensers, and air handling\nunits that help manage temperature"
    },
    {
      "start": 53.84,
      "end": 57.3,
      "text": "and humidity on the data center floor so\nthat the systems don't"
    },
    {
      "start": 57.4,
      "end": 61.24,
      "text": "overheat or shut down. These systems don't\nwork in"
    },
    {
      "start": 61.3,
      "end": 65.16,
      "text": "isolation. Every part of the data center\nis connected through cables,"
    },
    {
      "start": 65.36,
      "end": 69.24,
      "text": "power rails, busways, and energy\nmanagement systems. They"
    },
    {
      "start": 69.28,
      "end": 73.26,
      "text": "ensure that power is delivered efficiently\nto the rack. Then"
    },
    {
      "start": 73.32,
      "end": 77.1,
      "text": "comes rack level distribution. This is\nwhere the"
    },
    {
      "start": 77.2,
      "end": 80.54,
      "text": "actual compute happens, and a lot of the\nenergy is consumed and heat is"
    },
    {
      "start": 80.6,
      "end": 84.6,
      "text": "generated. Servers are arranged in\nenclosures where hot and cold"
    },
    {
      "start": 84.68,
      "end": 88.68,
      "text": "air is separated. Cooling via localized\nair or liquid"
    },
    {
      "start": 88.9,
      "end": 92.88,
      "text": "is constantly monitored with smart sensors\nand software. All"
    },
    {
      "start": 92.92,
      "end": 96.58,
      "text": "of this is maintained and monitored by\nsystems that"
    },
    {
      "start": 96.62,
      "end": 99.5,
      "text": "control real-time adjustments, alarm, and\nautomation."
    },
    {
      "start": 100.82,
      "end": 104.74,
      "text": "Think of it as the nervous center of the\ndata center. In the"
    },
    {
      "start": 104.78,
      "end": 108.62,
      "text": "next lesson, we'll go deeper into specific\nsubsystems like power and"
    },
    {
      "start": 108.7,
      "end": 112.68,
      "text": "cooling, but now you should have a\nbird's-eye view of how all"
    },
    {
      "start": 112.72,
      "end": 116.04,
      "text": "the parts come together to create an\nalways-on environment."
    }
  ],
  "assets": [
    "resources/captions/module1/1-1-welcome-course-overview-1080p.vtt"
  ],
  "text_inventory": {
    "sha256": "5b801d149090e45cdc130376f9ef4dbc2ef3fe3f3c45129f6a4a49d173784393",
    "entries": [
      {
        "text": "OPEN",
        "at_seconds": 2.5
      },
      {
        "text": "Compute Project ®",
        "at_seconds": 2.5
      },
      {
        "text": "POWE",
        "at_seconds": 22.5
      },
      {
        "text": "FACIL",
        "at_seconds": 22.5
      },
      {
        "text": "DATA CENTERS HAVE",
        "at_seconds": 27.5
      },
      {
        "text": "DATA CENTERS HAVE POWERFUL",
        "at_seconds": 32.5
      },
      {
        "text": "ENERGY SYSTEMS DESIGNED TO KEEP",
        "at_seconds": 32.5
      },
      {
        "text": "OPERATIONS RUNNING 24/7",
        "at_seconds": 32.5
      },
      {
        "text": "POWER GRID TRANSFORMER",
        "at_seconds": 37.5
      },
      {
        "text": "SWITCHGEAR",
        "at_seconds": 37.5
      },
      {
        "text": "UPS's",
        "at_seconds": 37.5
      },
      {
        "text": "GENERATORS",
        "at_seconds": 37.5
      },
      {
        "text": "UPS BAT",
        "at_seconds": 37.5
      },
      {
        "text": "PDU's",
        "at_seconds": 37.5
      },
      {
        "text": "COOLING",
        "at_seconds": 47.5
      },
      {
        "text": "INFRASTRUCTURE",
        "at_seconds": 47.5
      },
      {
        "text": "CHILLERS",
        "at_seconds": 52.5
      },
      {
        "text": "CONDENSERS",
        "at_seconds": 52.5
      },
      {
        "text": "AIR HANDLING",
        "at_seconds": 52.5
      },
      {
        "text": "UNITS",
        "at_seconds": 52.5
      },
      {
        "text": "110h1.",
        "at_seconds": 77.5
      },
      {
        "text": "Hiahh",
        "at_seconds": 77.5
      },
      {
        "text": "HHinH",
        "at_seconds": 77.5
      },
      {
        "text": "NERVOUS",
        "at_seconds": 102.5
      },
      {
        "text": "SYSTEM",
        "at_seconds": 102.5
      },
      {
        "text": "WE'LL GO DEEPER INTO",
        "at_seconds": 107.5
      },
      {
        "text": "SPECIFIC SUBSYSTEMS LIKE",
        "at_seconds": 107.5
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  },
  "source_poster": "resources/images/module1/1-1-welcome-course-overview-1080p.jpg"
}

## M1S4 · One Request Depends on Many Systems

{
  "id": 4,
  "type": "content_diagram",
  "slug": "service_journey",
  "section_label": "Service Dependencies",
  "title": "One Request Depends on Many Systems",
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 3
    }
  ]
}

Narration:
Think about opening a shared document. Your device sends a request through networks to the systems providing that service. Computing equipment handles the request, storage holds the information, and a response travels back.

The animation follows that sequence. The physical systems underneath stay necessary throughout: electricity powers the equipment, and cooling removes the heat it produces. A simple action on your device can depend on many connected systems, even though the service hides most of that complexity.


Media:
{
  "path": "figures/module1/service-journey.mp4",
  "poster": "figures/module1/service-journey-poster.png",
  "media_type": "video",
  "source": "custom",
  "autoplay": false,
  "loop": false,
  "muted": true,
  "alt": "A request travels from a user through networks to compute and storage, and a response returns. Power and cooling support the equipment throughout.",
  "caption": "A simple service action depends on connected physical systems.",
  "text_inventory": {
    "sha256": "6175621c1b841a4213bc618eec8fb1890f5742db89b7e470f3a44db50feb4baa",
    "entries": [
      {
        "text": "Your device",
        "at_seconds": 0
      },
      {
        "text": "Network",
        "at_seconds": 0
      },
      {
        "text": "Service systems",
        "at_seconds": 0
      },
      {
        "text": "Compute",
        "at_seconds": 0
      },
      {
        "text": "Storage",
        "at_seconds": 0
      },
      {
        "text": "Request",
        "at_seconds": 0
      },
      {
        "text": "Response",
        "at_seconds": 0
      },
      {
        "text": "Electricity powers equipment",
        "at_seconds": 0
      },
      {
        "text": "Heat must be removed",
        "at_seconds": 0
      },
      {
        "text": "A simple service action keeps its physical dependencies",
        "at_seconds": 0
      }
    ],
    "reviewed_on": "2026-10-26",
    "review_method": "Connector simplification: native source and decoded-frame visual review, arrow geometry and narration-synchronized playback checks. Figure wording and final narration timing are unchanged."
  },
  "sync_to_narration": true,
  "animation_source": "animations/module1/service-journey.html"
}

## M1S5 · What Is a Data Center?

{
  "id": 5,
  "type": "content_diagram",
  "slug": "what_is_a_data_center_video",
  "section_label": "Facility Purpose",
  "title": "What Is a Data Center?",
  "media_focus": true,
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 3,
      "block": 3
    }
  ],
  "glossary_usage_review": "Reviewed against slide text, current narration, transcribed video speech and hash-bound media text inventory.",
  "term_refs": [
    "power",
    "redundancy",
    "hyperscale",
    "edge_data_center",
    "cloud_computing",
    "ups"
  ],
  "narration_enabled": false,
  "technical_note": {
    "title": "Technical context for this recording",
    "paragraphs": [
      "The facility examples are illustrative. Edge describes proximity to the workload; it does not require a small or modular building. Carrier neutrality means customer choice among network providers. Connectivity and redundancy depend on the site and service design."
    ]
  }
}

Imported recording transcript:
So, now that you understand how data drives the digital world, let's answer the big question. What exactly is a data center? In simple terms, a data center is a specialized facility that houses computing systems, servers, storage, and networking hardware. These systems support everything from websites and cloud services to enterprise apps, financial transactions, and even the AI models we work with. You can think of it like this. When you stream a movie, check your bank account, join a video call, you're reaching out to computers located somewhere in the world inside a data center. But a data center is much more than just a room full of computers. It's a tightly controlled environment designed to maximize uptime, performance, security, all the time being as efficient as possible. First, there's power. Servers don't just plug into the wall. Data centers use redundant power systems. They use backup generators and battery arrays to keep everything running even during outages. Then there's cooling. Servers compute a lot of information, and that generates heat, a lot of it. So data centers use air and even liquid cooling systems to cool server components and maintain ideal operating temperatures for these servers to run reliably and at full speed. Connectivity is another key layer. Data centers act as digital hubs connected to the Internet via high-speed fiber optic cables. Many of these are also carrier neutral, meaning they connect to multiple providers offering maximum connectivity options. Security is baked into every level, physical and digital. Think of biometric access, surveillance, and fire suppression physically. Firewall segmentation and threat detection are done digitally and physically. All together, these systems create an environment where critical data and applications can live safely, operate continuously, and scale as needed. But not all data centers are the same. They vary in size, purpose, and location. In fact, you can think of data centers as existing on a spectrum. Smaller ones typically serve individual businesses and enterprises, while larger ones, hyperscale facilities, support vast global cloud platforms. Some serve small regional businesses. Others, and they are called hyperscale data centers, are run by tech giants like Amazon, Google, or Microsoft, and they support global cloud services. Then there are also edge data centers. They're smaller, modular units placed closer to where the data is generated. These are vital for real-time services like IoT, 5G, and AI. Regardless of size, all data centers share the same goal, to efficiently process, store, and move massive volumes of data reliably, fast, and securely. So why does this matter? Well, while we may not see them, data centers are essential to the smooth operation of our daily digital world. Data centers are the invisible backbone of everything we do online. They allow companies to scale, innovate, and operate globally. Without data centers, the digital world simply wouldn't function. In the next chapter, we'll take a closer look inside a data center to explore the key elements in the physical infrastructure that powers it all.

Media:
{
  "path": "resources/videos/module1/1-2-what-is-a-data-center-1080p.mp4",
  "poster": "resources/images/module1/video-slide-5-poster.jpg",
  "media_type": "video",
  "role": "original_video",
  "source": "reuse",
  "autoplay": false,
  "loop": false,
  "muted": false,
  "controls": true,
  "alt": "What Is a Data Center? video.",
  "caption": "Computing equipment depends on the facility and systems that support it.",
  "source_sha256": "bca8e8d5f4efab69a90902eedea5484dc0e48a97a81fbd634b755764a2c45882",
  "captions": [
    {
      "path": "resources/captions/module1/1-2-what-is-a-data-center-1080p.vtt",
      "language": "en",
      "label": "English (transcribed)"
    }
  ],
  "caption_cues": [
    {
      "start": 3.42,
      "end": 7.28,
      "text": "So, now that you understand how data\ndrives the digital world,"
    },
    {
      "start": 7.6,
      "end": 11.54,
      "text": "let's answer the big question. What\nexactly is a data"
    },
    {
      "start": 11.6,
      "end": 15.1,
      "text": "center? In simple terms, a data center is\na specialized"
    },
    {
      "start": 15.14,
      "end": 19.12,
      "text": "facility that houses computing systems,\nservers, storage,"
    },
    {
      "start": 19.4,
      "end": 23.22,
      "text": "and networking hardware. These systems\nsupport everything"
    },
    {
      "start": 23.28,
      "end": 27.04,
      "text": "from websites and cloud services to\nenterprise apps, financial"
    },
    {
      "start": 27.14,
      "end": 30.3,
      "text": "transactions, and even the AI models we\nwork with."
    },
    {
      "start": 31.74,
      "end": 35.3,
      "text": "You can think of it like this. When you\nstream a movie, check your bank"
    },
    {
      "start": 35.36,
      "end": 38.94,
      "text": "account, join a video call, you're\nreaching out to computers"
    },
    {
      "start": 39.52,
      "end": 42.94,
      "text": "located somewhere in the world inside a\ndata center."
    },
    {
      "start": 43.78,
      "end": 47.2,
      "text": "But a data center is much more than just a\nroom full of computers."
    },
    {
      "start": 48.18,
      "end": 52.12,
      "text": "It's a tightly controlled environment\ndesigned to maximize uptime,"
    },
    {
      "start": 52.28,
      "end": 55.66,
      "text": "performance, security, all the time being\nas"
    },
    {
      "start": 55.72,
      "end": 59.72,
      "text": "efficient as possible. First, there's\npower."
    },
    {
      "start": 60.44,
      "end": 64.12,
      "text": "Servers don't just plug into the wall.\nData centers use"
    },
    {
      "start": 64.18,
      "end": 67.98,
      "text": "redundant power systems. They use backup\ngenerators and"
    },
    {
      "start": 68.16,
      "end": 71.98,
      "text": "battery arrays to keep everything running\neven during outages."
    },
    {
      "start": 73.3,
      "end": 77.06,
      "text": "Then there's cooling. Servers compute a\nlot of information,"
    },
    {
      "start": 77.42,
      "end": 80.1,
      "text": "and that generates heat, a lot of it."
    },
    {
      "start": 81.32,
      "end": 85.3,
      "text": "So data centers use air and even liquid\ncooling systems"
    },
    {
      "start": 85.36,
      "end": 89.22,
      "text": "to cool server components and maintain\nideal operating"
    },
    {
      "start": 89.3,
      "end": 93.18,
      "text": "temperatures for these servers to run\nreliably and at full speed."
    },
    {
      "start": 94.36,
      "end": 98.04,
      "text": "Connectivity is another key layer. Data\ncenters act as digital"
    },
    {
      "start": 98.08,
      "end": 101.92,
      "text": "hubs connected to the Internet via high-\nspeed fiber optic cables."
    },
    {
      "start": 103.46,
      "end": 107.24,
      "text": "Many of these are also carrier neutral,\nmeaning they connect to multiple"
    },
    {
      "start": 107.28,
      "end": 110.18,
      "text": "providers offering maximum connectivity\noptions."
    },
    {
      "start": 111.42,
      "end": 115.36,
      "text": "Security is baked into every level,\nphysical and digital. Think of"
    },
    {
      "start": 115.42,
      "end": 119.18,
      "text": "biometric access, surveillance, and fire\nsuppression physically."
    },
    {
      "start": 120.38,
      "end": 123.86,
      "text": "Firewall segmentation and threat detection\nare done digitally"
    },
    {
      "start": 124.3,
      "end": 128.24,
      "text": "and physically. All together, these\nsystems"
    },
    {
      "start": 128.3,
      "end": 132.28,
      "text": "create an environment where critical data\nand applications can live safely,"
    },
    {
      "start": 132.64,
      "end": 135.3,
      "text": "operate continuously, and scale as needed."
    },
    {
      "start": 136.7,
      "end": 140.1,
      "text": "But not all data centers are the same.\nThey vary in size,"
    },
    {
      "start": 140.4,
      "end": 144.06,
      "text": "purpose, and location. In fact, you can\nthink of data"
    },
    {
      "start": 144.14,
      "end": 147.88,
      "text": "centers as existing on a spectrum. Smaller"
    },
    {
      "start": 147.98,
      "end": 151.48,
      "text": "ones typically serve individual businesses\nand enterprises,"
    },
    {
      "start": 152.04,
      "end": 155.68,
      "text": "while larger ones, hyperscale facilities,\nsupport"
    },
    {
      "start": 155.76,
      "end": 159.58,
      "text": "vast global cloud platforms. Some"
    },
    {
      "start": 160.2,
      "end": 163.74,
      "text": "serve small regional businesses. Others,"
    },
    {
      "start": 164.34,
      "end": 168.16,
      "text": "and they are called hyperscale data\ncenters, are run by tech giants like"
    },
    {
      "start": 168.26,
      "end": 172.0,
      "text": "Amazon, Google, or Microsoft, and they\nsupport global"
    },
    {
      "start": 172.06,
      "end": 175.76,
      "text": "cloud services. Then there are also"
    },
    {
      "start": 175.84,
      "end": 179.32,
      "text": "edge data centers. They're smaller,\nmodular units"
    },
    {
      "start": 179.96,
      "end": 183.96,
      "text": "placed closer to where the data is\ngenerated. These are vital for real-time"
    },
    {
      "start": 184.04,
      "end": 187.44,
      "text": "services like IoT, 5G, and AI."
    },
    {
      "start": 187.98,
      "end": 191.64,
      "text": "Regardless of size, all data centers share\nthe same goal,"
    },
    {
      "start": 192.52,
      "end": 196.42,
      "text": "to efficiently process, store, and move\nmassive"
    },
    {
      "start": 196.52,
      "end": 200.34,
      "text": "volumes of data reliably, fast, and"
    },
    {
      "start": 200.4,
      "end": 204.2,
      "text": "securely. So why does this matter? Well,"
    },
    {
      "start": 205.16,
      "end": 209.14,
      "text": "while we may not see them, data centers\nare essential to the"
    },
    {
      "start": 209.26,
      "end": 212.0,
      "text": "smooth operation of our daily digital\nworld."
    },
    {
      "start": 213.32,
      "end": 216.94,
      "text": "Data centers are the invisible backbone of\neverything we do online."
    },
    {
      "start": 217.58,
      "end": 221.2,
      "text": "They allow companies to scale, innovate,\nand operate globally."
    },
    {
      "start": 222.4,
      "end": 225.92,
      "text": "Without data centers, the digital world\nsimply wouldn't"
    },
    {
      "start": 225.98,
      "end": 229.58,
      "text": "function. In the next chapter, we'll take\na closer look"
    },
    {
      "start": 229.66,
      "end": 232.78,
      "text": "inside a data center to explore the key\nelements in the physical"
    },
    {
      "start": 232.84,
      "end": 234.54,
      "text": "infrastructure that powers it all."
    }
  ],
  "assets": [
    "resources/captions/module1/1-2-what-is-a-data-center-1080p.vtt"
  ],
  "text_inventory": {
    "sha256": "bca8e8d5f4efab69a90902eedea5484dc0e48a97a81fbd634b755764a2c45882",
    "entries": [
      {
        "text": "OPEN",
        "at_seconds": 2.5
      },
      {
        "text": "Compute Project ®",
        "at_seconds": 2.5
      },
      {
        "text": "WHAT IS ADATA",
        "at_seconds": 7.5
      },
      {
        "text": "CENTER?",
        "at_seconds": 7.5
      },
      {
        "text": "COMPUTING",
        "at_seconds": 17.5
      },
      {
        "text": "SYSTEM",
        "at_seconds": 17.5
      },
      {
        "text": "SE",
        "at_seconds": 17.5
      },
      {
        "text": "DATA CENTER",
        "at_seconds": 17.5
      },
      {
        "text": "WEBSITES AND",
        "at_seconds": 27.5
      },
      {
        "text": "CLOUD SERVICES",
        "at_seconds": 27.5
      },
      {
        "text": "FINANCIAL TRANSACTIONS",
        "at_seconds": 27.5
      },
      {
        "text": "A DATA CENTER IS MUCH MORE",
        "at_seconds": 47.5
      },
      {
        "text": "THAN JUST A ROOM FULL OF COMPUTERS",
        "at_seconds": 47.5
      },
      {
        "text": "CONNECTIVITY AREA",
        "at_seconds": 52.5
      },
      {
        "text": "SECURITY",
        "at_seconds": 52.5
      },
      {
        "text": "POWER AREA",
        "at_seconds": 52.5
      },
      {
        "text": "COOLING AREA",
        "at_seconds": 52.5
      },
      {
        "text": "SECURITY AREA",
        "at_seconds": 57.5
      },
      {
        "text": "POWER SYSTEM",
        "at_seconds": 62.5
      },
      {
        "text": "4",
        "at_seconds": 67.5
      },
      {
        "text": "POWER GRID",
        "at_seconds": 67.5
      },
      {
        "text": "DUAL FEED",
        "at_seconds": 67.5
      },
      {
        "text": "UNINTERRUPTED",
        "at_seconds": 67.5
      },
      {
        "text": "POWER SUPPLY (UPS)",
        "at_seconds": 67.5
      },
      {
        "text": "BACKUP",
        "at_seconds": 67.5
      },
      {
        "text": "GENERATOR",
        "at_seconds": 67.5
      },
      {
        "text": "SERVERS COMPUTE A LOT OF INFORMATION,",
        "at_seconds": 77.5
      },
      {
        "text": "AND THAT GE",
        "at_seconds": 77.5
      },
      {
        "text": "• COOLING SYSTEM",
        "at_seconds": 77.5
      },
      {
        "text": "AIR COOLING",
        "at_seconds": 87.5
      },
      {
        "text": "LIQUID COOLING",
        "at_seconds": 87.5
      },
      {
        "text": "DATA CENTERS ACT",
        "at_seconds": 97.5
      },
      {
        "text": "AS DIG",
        "at_seconds": 97.5
      },
      {
        "text": "IEUIA",
        "at_seconds": 97.5
      },
      {
        "text": "TERS ACT",
        "at_seconds": 102.5
      },
      {
        "text": "IL HUBS",
        "at_seconds": 102.5
      },
      {
        "text": "MANY ARE ALSO CARRIER-NEUTRAL,",
        "at_seconds": 107.5
      },
      {
        "text": "MEANING THEY CONNECT TO",
        "at_seconds": 107.5
      },
      {
        "text": "MULTIPLE PROVIDERS OFFERING",
        "at_seconds": 107.5
      },
      {
        "text": "PHYSICAL SECURITY",
        "at_seconds": 112.5
      },
      {
        "text": "DIGITAL SECURITY",
        "at_seconds": 122.5
      },
      {
        "text": "THESE ELEMENTS",
        "at_seconds": 127.5
      },
      {
        "text": "POWER",
        "at_seconds": 127.5
      },
      {
        "text": "COOLING",
        "at_seconds": 132.5
      },
      {
        "text": "CONNECTIVITY",
        "at_seconds": 132.5
      },
      {
        "text": "NOT ALL DATA CENTERS ARE THE SAME",
        "at_seconds": 137.5
      },
      {
        "text": "THEY VARY IN:",
        "at_seconds": 142.5
      },
      {
        "text": "• SIZE",
        "at_seconds": 142.5
      },
      {
        "text": "• PURPOSE",
        "at_seconds": 142.5
      },
      {
        "text": "• LOCATION",
        "at_seconds": 142.5
      },
      {
        "text": "SMALLER ONES",
        "at_seconds": 152.5
      },
      {
        "text": "TYPICALLY SERVE",
        "at_seconds": 152.5
      },
      {
        "text": "INDIVIDUAL BUSINESSES",
        "at_seconds": 152.5
      },
      {
        "text": "OR ENTERPRISE NEEDS",
        "at_seconds": 152.5
      },
      {
        "text": "LARGER HYPERSCALE",
        "at_seconds": 152.5
      },
      {
        "text": "FACILITIES SUPPORT",
        "at_seconds": 152.5
      },
      {
        "text": "VAST GLOBAL CLOUD",
        "at_seconds": 152.5
      },
      {
        "text": "PLATFORMS",
        "at_seconds": 152.5
      },
      {
        "text": "SOME SERVE SMALL REGIONAL BUSINESSES",
        "at_seconds": 162.5
      },
      {
        "text": "OTHERS CALLED HYPERSCALE DATA CENTERS ARE RUN BY TECH GIANTS",
        "at_seconds": 167.5
      },
      {
        "text": "amazon",
        "at_seconds": 172.5
      },
      {
        "text": "Google",
        "at_seconds": 172.5
      },
      {
        "text": "H Microsoft",
        "at_seconds": 172.5
      },
      {
        "text": "EDGE DATA CENTER",
        "at_seconds": 177.5
      },
      {
        "text": "TO EFFIC",
        "at_seconds": 192.5
      },
      {
        "text": "TO EFFICIENTLY PROCESS, STORE, AND MOVE MASSIVE",
        "at_seconds": 197.5
      },
      {
        "text": "VOLUMES OF DATA RELIABLY, FAST AND SECURELY",
        "at_seconds": 197.5
      },
      {
        "text": "WHY DOES THIS",
        "at_seconds": 202.5
      },
      {
        "text": "MATTER?",
        "at_seconds": 202.5
      },
      {
        "text": "DATA CENTERS ARE ESSENTIAL",
        "at_seconds": 207.5
      },
      {
        "text": "DATA CENTERS ARE",
        "at_seconds": 212.5
      },
      {
        "text": "TO THE SMOOTH O",
        "at_seconds": 212.5
      },
      {
        "text": "OF OUR DIGITAL",
        "at_seconds": 212.5
      },
      {
        "text": "NO DATA",
        "at_seconds": 222.5
      },
      {
        "text": "Nº",
        "at_seconds": 222.5
      },
      {
        "text": "Compute Project®",
        "at_seconds": 237.5
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  },
  "source_poster": "resources/images/module1/1-2-what-is-a-data-center-1080p.jpg"
}

## M1S6 · Capacity Is More Than Floor Space

{
  "id": 6,
  "type": "content_two_column",
  "slug": "capacity_and_units",
  "section_label": "Physical Capacity",
  "title": "Capacity Is More Than Floor Space",
  "bullets": [
    {
      "bold_lead": "IT capacity",
      "text": "Compute, storage and network capability."
    },
    {
      "bold_lead": "Facility capacity",
      "text": "Power delivery, heat removal and physical space."
    },
    {
      "bold_lead": "Power",
      "text": "kW and MW describe a rate or available electrical capacity."
    },
    {
      "bold_lead": "Energy",
      "text": "kWh measures electrical use over time."
    }
  ],
  "reference_links": [
    {
      "label": "Power and energy units",
      "url": "https://www.eia.gov/energyexplained/electricity/measuring-electricity.php"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 5
    },
    {
      "source": "eia_units"
    }
  ],
  "term_refs": [
    "energy"
  ]
}

Narration:
# pronunciation: kW -> kilowatts; MW -> megawatts; kWh -> kilowatt hours
A data center needs several kinds of capacity. Servers process information, storage retains it, and networks move it. The facility must supply enough electrical power and remove the resulting heat. Available floor space alone doesn't tell you what equipment a site can support.

Keep power and energy separate. Kilowatts and megawatts describe the rate of electrical use or available capacity. Kilowatt hours measure energy used over time. A constant load of one kilowatt running for one hour uses one kilowatt hour. We'll use that distinction again when discussing efficiency.


Media:
{
  "path": "figures/module1/capacity-and-units.svg",
  "source": "custom",
  "alt": "Compute, storage and networking are supported by electrical and cooling capacity. One kilowatt for one hour equals one kilowatt hour.",
  "caption": "Physical capacity and energy use answer different planning questions.",
  "text_inventory": {
    "sha256": "8a421a3f1518e4ea5b02e0818be02637ebbd5bd78b196ec02394750b4e7fa9dc",
    "entries": [
      {
        "text": "Compute"
      },
      {
        "text": "Storage"
      },
      {
        "text": "Networking"
      },
      {
        "text": "Electrical capacity"
      },
      {
        "text": "Heat removal"
      },
      {
        "text": "1 kW × 1 h = 1 kWh"
      },
      {
        "text": "Power × time = energy"
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  }
}

## M1S7 · Tiers Describe Infrastructure Capabilities

{
  "id": 7,
  "type": "content_table",
  "slug": "tier_capabilities",
  "section_label": "Infrastructure Resilience",
  "title": "Tiers Describe Infrastructure Capabilities",
  "subtitle": "A capability classification does not guarantee an annual uptime percentage.",
  "columns": [
    "Tier",
    "Distinguishing capability"
  ],
  "rows": [
    [
      "I — Basic capacity",
      "Capacity to support the critical environment."
    ],
    [
      "II — Redundant capacity",
      "Additional capacity components; distribution remains a limitation."
    ],
    [
      "III — Concurrently maintainable",
      "Planned component or distribution-path maintenance without interrupting operations."
    ],
    [
      "IV — Fault tolerant",
      "An individual equipment failure or distribution interruption does not interrupt operations."
    ]
  ],
  "reference_links": [
    {
      "label": "Uptime Tier capabilities",
      "url": "https://uptimeinstitute.com/tiers"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 4
    },
    {
      "source": "uptime_tiers"
    }
  ],
  "source_correction": "Replace embedded uptime percentages and annual downtime predictions with current capability definitions.",
  "term_refs": [
    "concurrent_maintainability",
    "fault_tolerance"
  ]
}

Narration:
# pronunciation: Tier I -> tier one; Tier II -> tier two; Tier III -> tier three; Tier IV -> tier four
Uptime Institute's four Tiers describe site infrastructure capabilities. Tier one provides basic capacity. Tier two adds redundant capacity components. Tier three adds concurrent maintainability: planned work can remove a component or distribution path without interrupting operations. Tier four adds fault tolerance for an individual equipment failure or distribution interruption.

These categories don't promise a particular annual uptime percentage. They also don't replace resilient applications, network design or disciplined operations. Use the Tier description to ask what maintenance and failure the infrastructure can accommodate, then consider the service's wider requirements.


## M1S8 · Enterprise, Colocation, Hyperscale and Edge

{
  "id": 8,
  "type": "content_grid",
  "slug": "facility_types",
  "section_label": "Facility Characteristics",
  "title": "Enterprise, Colocation, Hyperscale and Edge",
  "subtitle": "The labels describe different dimensions and can overlap.",
  "grid_cols": 2,
  "cards": [
    {
      "title": "Enterprise",
      "body": "A facility serving an organization's own computing needs."
    },
    {
      "title": "Colocation",
      "body": "Space, power and supporting infrastructure for customers' equipment."
    },
    {
      "title": "Hyperscale",
      "body": "Infrastructure designed for very large, repeatable operations and growth."
    },
    {
      "title": "Edge",
      "body": "Computing placed close to the users, devices or activity it serves."
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 5
    }
  ],
  "term_refs": [
    "colocation"
  ]
}

Narration:
Enterprise, colocation, hyperscale and edge describe different aspects of a data center. An enterprise facility supports an organization's needs. Colocation provides space and supporting infrastructure for customers' equipment. Hyperscale describes an approach built to operate and expand at very large scale. Edge places computing closer to the users, devices or activity it serves.

The labels can overlap. An organization might place an edge deployment in a colocation facility. Ask which characteristic a label describes: the operating arrangement, the scale, or the relationship to the workload.


## M1S9 · AI Factories Align the Whole System

{
  "id": 9,
  "type": "content_diagram",
  "slug": "ai_workloads",
  "section_label": "A Workload and Design Lens",
  "title": "AI Factories Align the Whole System",
  "reference_links": [
    {
      "label": "IEA · Energy and AI",
      "url": "https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary"
    },
    {
      "label": "OCP ecosystem vision",
      "url": "https://www.opencompute.org/news/realizing-the-ocp-open-data-center-ecosystem-vision/"
    }
  ],
  "term_refs": [
    "training",
    "inference",
    "ai_factory"
  ]
}

Narration:
# Approved Astra content update · Leo / Eleven v4
Training adjusts an artificial intelligence model using data. Inference uses a trained model to produce an output, such as identifying a defect in an image. These activities can place different demands on the infrastructure. An AI factory organizes computing and data movement around developing and running AI at scale. Accelerators work with memory, storage, networks and software. Electrical power and heat removal support the complete system. Useful output depends on those parts working together. AI factory describes a purpose and design approach. It can overlap enterprise, colocation or hyperscale arrangements. It does not prescribe one rack density, one cooling technology or one ownership model. Ask what the workload needs before choosing the infrastructure.


Media:
{
  "path": "figures/module1/ai-factory-system.svg",
  "source": "custom",
  "alt": "Training adjusts a model; inference uses it. Computing, data movement, software, power and cooling form one coordinated system.",
  "caption": "AI factory describes a purpose and design approach that can overlap familiar facility types.",
  "text_inventory": {
    "sha256": "df8c085d978042885d57a7aa6e2f11fd83209cdb25e9589d750fb58d219c98fb",
    "entries": [
      {
        "text": "Training: adjust a model using data"
      },
      {
        "text": "Inference: use a trained model"
      },
      {
        "text": "Coordinate the complete system around AI workloads"
      },
      {
        "text": "Accelerators & memory"
      },
      {
        "text": "Storage & data movement"
      },
      {
        "text": "Networks & software"
      },
      {
        "text": "Electrical power · heat removal · operating capacity"
      },
      {
        "text": "Purpose and design can overlap enterprise, colocation and hyperscale"
      }
    ],
    "reviewed_on": "2026-10-26",
    "review_method": "Native rendered SVG visual review and text geometry inspection."
  }
}

## M1S10 · Place AI Where the Service Can Work

{
  "id": 10,
  "type": "content_diagram",
  "slug": "ai_placement",
  "section_label": "AI Computing Continuum",
  "title": "Place AI Where the Service Can Work",
  "reference_links": [
    {
      "label": "OCP AICC project",
      "url": "https://www.opencompute.org/projects/aicc/"
    },
    {
      "label": "Explore the AICC course",
      "url": "https://academy.opencompute.org/learn/courses/58/ai-computing-continuum-aicc-extending-ai-beyond-the-hyperscale-data-center"
    }
  ],
  "term_refs": [
    "aicc"
  ]
}

Narration:
# Approved Astra content update · Leo / Eleven v4
Consider an industrial inspection service. A camera sends an image to a trained model at the local site. The response must arrive before the item passes the inspection point. A remote connection cannot be assumed to meet that deadline. Now the wide-area connection becomes unavailable. Local inference can continue if its model, data, power and computing resources remain available. Separate, nonurgent analysis can wait. When connectivity returns, that work can use regional capacity if data rules and available resources permit. This is a placement decision, not an instant move of a running task. Edge describes proximity to the activity being served. OCP's AI Computing Continuum project develops open, modular infrastructure approaches for regional, enterprise, telecommunications and industrial environments beyond hyperscale facilities. Its dedicated Academy course explores the architecture. Choose placement through response needs, connectivity, data constraints and site capacity.


Media:
{
  "path": "figures/module1/ai-placement.mp4",
  "poster": "figures/module1/ai-placement-poster.png",
  "media_type": "video",
  "source": "custom",
  "autoplay": false,
  "loop": false,
  "muted": true,
  "sync_to_narration": true,
  "animation_source": "animations/module1/ai-placement.html",
  "alt": "Local industrial inspection continues during a wide-area connection outage; nonurgent analysis waits for regional capacity and a restored connection.",
  "caption": "An illustrative placement decision: protect local response, then schedule work that can wait.",
  "text_inventory": {
    "sha256": "44ee5ddd5c9461348ccfb8b4b3fef8fcc57abead30f3436f29a6c3fa6a440b54",
    "entries": [
      {
        "text": "Industrial inspection · illustrative service constraints",
        "at_seconds": 0
      },
      {
        "text": "Inspection camera",
        "at_seconds": 0
      },
      {
        "text": "Local model inference",
        "at_seconds": 0
      },
      {
        "text": "Respond before inspection point",
        "at_seconds": 0
      },
      {
        "text": "Production line keeps its response",
        "at_seconds": 0
      },
      {
        "text": "Separate nonurgent analysis queue",
        "at_seconds": 0
      },
      {
        "text": "Regional analysis capacity",
        "at_seconds": 0
      },
      {
        "text": "Wide-area connection",
        "at_seconds": 0
      },
      {
        "text": "Connection unavailable · local inference remains feasible",
        "at_seconds": 0
      },
      {
        "text": "Connection restored · schedule eligible nonurgent work",
        "at_seconds": 0
      },
      {
        "text": "Short response deadline · local model and resources available",
        "at_seconds": 0
      },
      {
        "text": "Nonurgent work waits; the running local task does not migrate",
        "at_seconds": 0
      },
      {
        "text": "Regional work requires connectivity, suitable data rules and available capacity",
        "at_seconds": 0
      },
      {
        "text": "OCP AICC · regional, enterprise, telco and industrial",
        "at_seconds": 0
      },
      {
        "text": "Response needs · connectivity · data constraints · site capacity",
        "at_seconds": 0
      }
    ],
    "reviewed_on": "2026-10-26",
    "review_method": "Native deterministic source states and exact decoded-frame review; dynamic labels and final-WAV phrase map inspected."
  }
}

## M1S11 · Match the Facility to Its Role

{
  "id": 11,
  "type": "knowledge_check",
  "slug": "facility_matching",
  "title": "Match the Facility to Its Role",
  "subtitle": "Match all four definitions, then submit. An attempt is required; correctness is not.",
  "questions": [
    {
      "id": "m1_kc1",
      "type": "matching",
      "source_check_id": "M1-KC1",
      "prompt": "Match each data center type to the characteristic emphasized in its definition.",
      "pairs": [
        {
          "id": "edge",
          "prompt": "Edge Data Centers",
          "match": "Located near end-users to reduce latency",
          "feedback": "Edge emphasizes proximity to a workload or its users. It can be deployed within several ownership or operating models."
        },
        {
          "id": "hyperscale",
          "prompt": "Hyperscale Data Center",
          "match": "Support global-scale cloud infrastructure",
          "feedback": "Hyperscale emphasizes scale and repeatable operations. Large cloud infrastructure is the example tested here."
        },
        {
          "id": "enterprise",
          "prompt": "Enterprise Data Center",
          "match": "Built and used by a single organization",
          "feedback": "Enterprise emphasizes serving an organization's own needs; it does not specify one fixed facility size."
        },
        {
          "id": "colocation",
          "prompt": "Colocation Data Center",
          "match": "Shared facility where tenants bring their own equipment",
          "feedback": "Colocation separates the facility service from the customer's equipment. The provider supplies contracted space and supporting infrastructure."
        }
      ],
      "feedback_correct": "Each association identifies the characteristic emphasized by that label. The labels can overlap in real deployments.",
      "feedback_incorrect": "Compare the definition with the label's purpose: edge is proximity, hyperscale is scale, enterprise is organizational use, and colocation is a facility service."
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 5,
      "block": 8
    }
  ]
}

Narration:
Match each facility type to the characteristic emphasized in its definition. Treat these as useful associations, rather than categories that can never overlap. Submit a complete set of matches to continue. Correct answers aren't required, and you can use the explanations to review the relationships and try again.


## M1S12 · Location Balances Access, Energy and Risk

{
  "id": 12,
  "type": "content_diagram",
  "slug": "location_tradeoffs",
  "section_label": "Site Selection",
  "title": "Location Balances Access, Energy and Risk",
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 6
    }
  ],
  "term_refs": [
    "latency"
  ]
}

Narration:
Location balances several needs. Being closer to users can reduce network delay, or latency. Strong connectivity gives services access to users and other facilities. Power availability, cooling conditions, water requirements and local hazards affect what a site can support.

Organizations also consider costs and requirements for where information is stored or processed. A city name alone doesn't establish compliance or resilience. The useful question is whether a location fits the workload and its constraints. The lowest-cost site can be a poor choice if it cannot meet those needs.


Media:
{
  "path": "figures/module1/location-tradeoffs.svg",
  "source": "custom",
  "alt": "Workload needs are considered alongside connectivity and latency, power and cooling resources, hazards and recovery, costs and data-location requirements.",
  "caption": "Choose a location by the workload's requirements and the site's constraints.",
  "text_inventory": {
    "sha256": "3f5203ae0019a9af11265cc047c12b42b5cb33fa46944ed13632e738be3f0d45",
    "entries": [
      {
        "text": "Connectivity and proximity"
      },
      {
        "text": "Routes, users and network delay"
      },
      {
        "text": "Power and cooling resources"
      },
      {
        "text": "Available electrical and thermal capacity"
      },
      {
        "text": "Risk and recovery"
      },
      {
        "text": "Hazards and shared dependencies"
      },
      {
        "text": "Cost and data requirements"
      },
      {
        "text": "Operating needs and location constraints"
      },
      {
        "text": "Match site constraints to workload requirements"
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  }
}

## M1S13 · Regional Hubs Serve Different Needs

{
  "id": 13,
  "type": "content_grid",
  "slug": "regional_examples",
  "section_label": "Regional Examples",
  "title": "Regional Hubs Serve Different Needs",
  "subtitle": "Illustrative roles, not a city ranking or a site guarantee.",
  "grid_cols": 3,
  "cards": [
    {
      "title": "Ashburn",
      "body": "North American network connectivity."
    },
    {
      "title": "São Paulo",
      "body": "Access to a large South American market."
    },
    {
      "title": "Frankfurt",
      "body": "European users and interconnected networks."
    },
    {
      "title": "Johannesburg",
      "body": "A regional example in southern Africa."
    },
    {
      "title": "Singapore",
      "body": "A regional example in Southeast Asia."
    },
    {
      "title": "Sydney",
      "body": "A regional example in Australia."
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 6
    }
  ],
  "editorial_note": "Use compact cards to preserve all six named source examples; source claims of rankings, legal compliance and guaranteed suitability are not repeated."
}

Narration:
The regional examples illustrate the same location questions in different settings. Ashburn connects services to a major North American network market. São Paulo serves a large South American market, while Frankfurt connects European users and networks.

Johannesburg, Singapore and Sydney illustrate regional connectivity in southern Africa, Southeast Asia and Australia. Their usefulness depends on the customers, networks and facility options a particular deployment needs. These are examples of regional roles, rather than a ranking of cities or a guarantee that any site in one city will meet a project's requirements.


## M1S14 · Remote Sites Have a Different Tradeoff

{
  "id": 14,
  "type": "content_diagram",
  "slug": "remote_research",
  "section_label": "Remote Computing",
  "title": "Remote Sites Have a Different Tradeoff",
  "reference_links": [
    {
      "label": "McMurdo research computing example",
      "url": "https://www.unavco.org/polar-services/forward-fielded-instruments/mcmurdo-station/"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 6
    },
    {
      "source": "mcmurdo_research"
    }
  ]
}

Narration:
# pronunciation: McMurdo -> Mack Murdo
Remote research creates a different location problem. At a station such as Mack Murdo in Antarctica, instruments and researchers need local computing and data handling far from the usual network hubs.

Processing some information locally can reduce dependence on a distant connection. Information may still need to be stored, transferred or backed up elsewhere. The lesson is to place the needed capability where the activity occurs, while planning for limited connectivity, maintenance access and logistics. A remote installation doesn't need to resemble a large commercial campus to perform an important role.


Media:
{
  "path": "figures/module1/remote-research.svg",
  "source": "custom",
  "alt": "Local instruments connect to local processing and storage, with a separate link to distant facilities.",
  "caption": "Local capability supports the research activity while remote links and logistics impose constraints.",
  "text_inventory": {
    "sha256": "da4cd109af85e851ddec95f4791eab69e98bba6e3b24edcc1c1ee9975ccfde33",
    "entries": [
      {
        "text": "Instruments"
      },
      {
        "text": "Local processing and storage"
      },
      {
        "text": "Remote systems"
      },
      {
        "text": "Local capability and remote connectivity serve different needs"
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  }
}

## M1S15 · Fiber Connects Facilities and Users

{
  "id": 15,
  "type": "content_diagram",
  "slug": "network_connections",
  "section_label": "Physical Connectivity",
  "title": "Fiber Connects Facilities and Users",
  "reference_links": [
    {
      "label": "Submarine cable resilience",
      "url": "https://www.itu.int/digital-resilience/submarine-cables/"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 8
    },
    {
      "source": "itu_connectivity"
    }
  ]
}

Narration:
Data centers connect through physical networks. Terrestrial fiber links buildings and regions; submarine fiber links land networks across oceans. Local access networks complete the connection to businesses, devices and users.

Satellite systems can provide connectivity or an alternate path where geography and infrastructure make other options difficult. Their performance depends on the system and location, so avoid assuming one fixed delay or bandwidth for every satellite connection. The map illustrates how many networks depend on shared physical routes. It isn't a current inventory of every cable or connection.


Media:
{
  "path": "resources/images/module1/world-cable-map.jpg",
  "source": "reuse",
  "alt": "A historical world cable map illustrates the physical routes and landing points of international connections.",
  "caption": "Illustrative cable map; not a current cable inventory. Map data: OpenStreetMap contributors. Cable data: Greg’s Cable Map.",
  "source_sha256": "87c37019582253115fca3b991c3a2fc5332d470c04c2d73e0db7336c6af9cb20",
  "text_inventory": {
    "sha256": "87c37019582253115fca3b991c3a2fc5332d470c04c2d73e0db7336c6af9cb20",
    "entries": [
      {
        "text": "Canada; United States of America; Russia; Kazakhstan; Pakistan; Brazil; Paraguay; Australia; New Zealand; map data © OpenStreetMap contributors; Cable data from cablemap.info / Greg’s Cable Map."
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  }
}

## M1S16 · Redundancy Must Survive the Same Failure

{
  "id": 16,
  "type": "content_diagram",
  "slug": "failure_domains",
  "section_label": "Shared Failures",
  "title": "Redundancy Must Survive the Same Failure",
  "reference_links": [
    {
      "label": "Physical network resilience",
      "url": "https://www.itu.int/digital-resilience/submarine-cables/"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 8
    },
    {
      "source": "itu_connectivity"
    }
  ]
}

Narration:
Two connections can still share one point of failure. Imagine separate network services that pass through the same trench. A single excavation could damage both. Extra equipment is useful only when it addresses the failure you're trying to withstand.

Resilience combines appropriate separation with ways to continue or recover service. That may include alternate routes, replicated systems and tested recovery procedures. Backups support recovery, but they don't automatically provide uninterrupted service. Ask what event could affect the paths or systems together, and what the service would do next.


Media:
{
  "path": "figures/module1/shared-failure-routes.svg",
  "source": "custom",
  "alt": "Two connections share a trench in one example; an alternate example uses physically separated routes.",
  "caption": "Separate services may still share a physical risk. Route diversity must address the event being considered.",
  "text_inventory": {
    "sha256": "f8537684fb288fd0c6eab6eebdf6de02b9709c19885ee7ca2ce93ed7bb0a8b9a",
    "entries": [
      {
        "text": "Shared physical risk"
      },
      {
        "text": "Site A"
      },
      {
        "text": "Site B"
      },
      {
        "text": "One trench can affect both links"
      },
      {
        "text": "Separated physical routes"
      },
      {
        "text": "Site A"
      },
      {
        "text": "Site B"
      },
      {
        "text": "Review other shared dependencies too"
      }
    ],
    "reviewed_on": "2026-10-26",
    "review_method": "Connector audit: simplified separated physical routes from four bends to two each, preserving route separation and all text; native SVG and desktop/phone course-page visual review."
  }
}

## M1S17 · Cloud Is a Service Model Built on Facilities

{
  "id": 17,
  "type": "content_two_column",
  "slug": "cloud_service_model",
  "section_label": "Facility and Service",
  "title": "Cloud Is a Service Model Built on Facilities",
  "bullets": [
    {
      "bold_lead": "Facility",
      "text": "Houses and supports physical equipment."
    },
    {
      "bold_lead": "Cloud",
      "text": "Provides on-demand access to pooled configurable resources."
    },
    {
      "bold_lead": "Deployment",
      "text": "Can be private, public or connected with other cloud environments."
    },
    {
      "bold_lead": "Availability",
      "text": "Depends on the selected service and its architecture."
    }
  ],
  "reference_links": [
    {
      "label": "NIST cloud definition",
      "url": "https://www.nist.gov/publications/nist-definition-cloud-computing?pub_id=909616"
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 9
    },
    {
      "source": "nist_cloud"
    }
  ]
}

Narration:
Cloud computing is a way to provide resources as an on-demand service. Users can obtain shared computing capabilities that can be provisioned and released with little manual intervention. The service still relies on physical equipment and facilities.

A cloud can be private to one organization, public, or connected with other cloud environments. It doesn't have to span many data centers, and a private cloud doesn't have to be reached through the public internet. When comparing options, separate the service model from the facility and check which availability features the particular service provides.


Media:
{
  "path": "figures/module1/cloud-service-layers.svg",
  "source": "custom",
  "alt": "An on-demand service layer is supported by physical compute, storage and networking within facilities.",
  "caption": "The service model changes how resources are provided; the physical dependencies remain.",
  "text_inventory": {
    "sha256": "446eb7b646a980855c9a2c7cf9c4198f31df0b604faab17e9c0d367316237285",
    "entries": [
      {
        "text": "On-demand resource delivery"
      },
      {
        "text": "Physical compute, storage and networking"
      },
      {
        "text": "Facility power, cooling and space"
      },
      {
        "text": "The service model retains physical dependencies"
      }
    ],
    "reviewed_on": "2026-10-23",
    "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
  }
}

## M1S18 · What Connects the Digital World

{
  "id": 18,
  "type": "takeaways",
  "slug": "digital_world_takeaways",
  "title": "What Connects the Digital World",
  "items": [
    "Digital services depend on connected physical systems.",
    "Facility labels describe ownership, scale or proximity; AI factory adds a workload and design lens.",
    "Resilience depends on maintenance, failure and recovery behavior.",
    "Cloud describes a service model that still depends on facilities."
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 10
    }
  ]
}

Narration:
# Approved Astra content update · Leo / Eleven v4
Digital services depend on connected physical systems. Facility labels describe different dimensions, including ownership, scale and proximity. An AI factory adds a workload and design lens. Training and inference have requirements that must be matched to the whole system. Placement across the computing continuum depends on response needs, connectivity, data and site capacity. Resilience depends on how systems behave during maintenance, failure and recovery. Cloud services still depend on real facilities. Keep these relationships in mind as we follow power and heat through the next module.


## M1S19 · Apply the Digital World Model

{
  "id": 19,
  "type": "knowledge_check",
  "slug": "digital_world_check",
  "title": "Apply the Digital World Model",
  "subtitle": "Submit all three questions to continue. Use the feedback to review and retry.",
  "questions": [
    {
      "id": "m1_kc2",
      "source_check_id": "M1-KC2",
      "prompt": "What is the primary role of a data center in digital infrastructure?",
      "choices": [
        {
          "id": "a",
          "text": "To replace the cloud",
          "correct": false,
          "feedback_incorrect": "Cloud services rely on data-center equipment. A facility supports those services rather than replacing the service model."
        },
        {
          "id": "b",
          "text": "To create mobile apps",
          "correct": false,
          "feedback_incorrect": "Developers create apps. The physical facility provides the equipment and supporting systems on which applications and their services can run."
        },
        {
          "id": "c",
          "text": "To store and process data through physical hardware",
          "correct": true
        },
        {
          "id": "d",
          "text": "To provide customer support services",
          "correct": false,
          "feedback_incorrect": "Customer support is an organizational function that may use digital services. The data center's underlying role is to house and support the hardware that stores, processes and moves information."
        }
      ],
      "feedback_correct": "The data center brings physical computing, storage and networking equipment together with the systems that support its operation.",
      "feedback_incorrect": "Separate the facility's physical role from the applications or organizational activities it supports."
    },
    {
      "id": "m1_kc3",
      "source_check_id": "M1-KC3",
      "prompt": "Which statement best describes cloud computing?",
      "choices": [
        {
          "id": "a",
          "text": "A single company-owned data center, regardless of how resources are provided",
          "correct": false,
          "feedback_incorrect": "A single facility can host a private cloud, but ownership and location don't establish the service model. Look for on-demand access to pooled resources."
        },
        {
          "id": "b",
          "text": "On-demand network access to pooled, configurable computing resources",
          "correct": true
        },
        {
          "id": "c",
          "text": "Any off-site equipment, even when each change requires manual provisioning",
          "correct": false,
          "feedback_incorrect": "Off-site hosting describes location. Cloud also concerns how resources are provisioned, shared and made available on demand."
        },
        {
          "id": "d",
          "text": "A service that can exist only on the public internet",
          "correct": false,
          "feedback_incorrect": "Private cloud resources can be accessed through private networks. Public internet access is not a requirement for every cloud deployment."
        }
      ],
      "feedback_correct": "Cloud describes how computing resources are provided. The physical deployment may vary, and a private cloud need not span many data centers.",
      "feedback_incorrect": "Look for the resource-delivery characteristics rather than ownership, off-site location or public internet access alone."
    },
    {
      "id": "m1_kc4",
      "source_check_id": "M1-KC4",
      "prompt": "Which data center type is specifically placed near its users or activity to reduce latency?",
      "choices": [
        {
          "id": "a",
          "text": "Public Library",
          "correct": false,
          "feedback_incorrect": "A library may use local computing, but this label describes an institution. Edge is the infrastructure label that emphasizes proximity to the activity or users."
        },
        {
          "id": "b",
          "text": "Underground Bunker Facility",
          "correct": false,
          "feedback_incorrect": "A bunker can house a data center, but the building form does not tell you how close the computing is to its users. Edge specifically describes that placement goal."
        },
        {
          "id": "c",
          "text": "Tier 1 Cloud Hub",
          "correct": false,
          "feedback_incorrect": "A Tier label concerns site infrastructure capability. It does not specify proximity to users, and 'Tier 1 Cloud Hub' is not the facility type being tested."
        },
        {
          "id": "d",
          "text": "Edge Data Center",
          "correct": true
        }
      ],
      "feedback_correct": "Edge placement brings computing closer to the users, devices or activity it serves, which can reduce network delay.",
      "feedback_incorrect": "Choose the label that describes computing placement relative to a workload or its users."
    }
  ],
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 7
    },
    {
      "source": "nist_cloud"
    }
  ]
}

Narration:
Use these three questions to connect the terms to their purpose. Consider what a data center physically does, what makes cloud a service model, and why computing might be placed near its users.

Submit an answer to each question before continuing. You don't need every answer correct to advance. Read the explanation for your selected choice, and retry if you want to check your reasoning again.


## M1S20 · up_next

{
  "id": 20,
  "type": "up_next",
  "slug": "physical_infrastructure_next",
  "next_module_number": 2,
  "next_module_title": "Data Center Physical Infrastructure",
  "thank_you_message": "Thank you for completing Module 1: The Digital World.",
  "source_refs": [
    {
      "source": "rise_m1",
      "lesson": 10
    }
  ]
}

Narration:
Thank you for completing The Digital World. You can now connect digital services to their physical foundations and distinguish facility characteristics from cloud services.

Module two examines how power delivery, cooling and physical layout support the equipment. You'll follow those systems together, because a working service depends on the whole chain.
