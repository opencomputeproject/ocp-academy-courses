# Module 2: Data Center Physical Infrastructure
Course: Data Centers: From Digital Services to Physical Infrastructure
Review packet generated from the current editable course. Narration marked inactive is absent from the runtime.

## M2S1: Data Center Physical Infrastructure
Type: title

### Authored slide fields
```json
{
  "id": 1,
  "type": "title",
  "slug": "physical_infrastructure",
  "title": "Data Center Physical Infrastructure",
  "subtitle": "Follow power, heat and the systems that support IT.",
  "audio": {
    "script_file": "audio/module2/slide_01_physical_infrastructure.txt",
    "wav_file": "audio/module2/slide_01_physical_infrastructure.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 1
    }
  ]
}
```

### Active spoken narration
Module two: Data Center Physical Infrastructure. Computing equipment needs a continuous supply of power and a way to release heat. You'll follow those supporting systems through the facility and see why electrical, thermal and physical constraints have to be considered together.


## M2S2: Trace Power, Heat and Physical Constraints
Type: objectives

### Authored slide fields
```json
{
  "id": 2,
  "type": "objectives",
  "slug": "trace_supporting_systems",
  "title": "Trace Power, Heat and Physical Constraints",
  "objectives": [
    "Identify facility, electrical, cooling and IT systems.",
    "Trace power delivery and explain backup roles.",
    "Explain heat removal and airflow containment.",
    "Recognize the constraints that jointly limit a deployment."
  ],
  "audio": {
    "script_file": "audio/module2/slide_02_trace_supporting_systems.txt",
    "wav_file": "audio/module2/slide_02_trace_supporting_systems.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 1
    }
  ]
}
```

### Active spoken narration
By the end of this module, you'll be able to trace a conventional power path, explain the purpose of backup systems, and describe how cooling moves heat out of the equipment. You'll also compare hot and cold aisle containment and recognize why free floor space doesn't guarantee room for another workload.

The goal is a system view: a deployment works only when the supporting systems can accommodate it together.


## M2S3: A Tour of the Physical Systems
Type: content_diagram

### Authored slide fields
```json
{
  "id": 3,
  "type": "content_diagram",
  "slug": "2_1_data_center_overview_1080p",
  "title": "A Tour of the Physical Systems",
  "section_label": "Explanatory Video",
  "media_focus": true,
  "figure": {
    "path": "resources/videos/module2/2-1-data-center-overview-1080p.mp4",
    "poster": "resources/images/module2/video-slide-3-poster.jpg",
    "media_type": "video",
    "role": "original_video",
    "source": "reuse",
    "autoplay": false,
    "loop": false,
    "muted": false,
    "controls": true,
    "alt": "A Tour of the Physical Systems video.",
    "caption": "CRAC and CRAH describe distinct room-cooling technologies. A UPS is a complete system, including power electronics, controls and stored energy.",
    "source_sha256": "6b694529e9d196954c3bade8a1d92a789b9b0903fe3ea0e59ca75de8cb564da8",
    "captions": [
      {
        "path": "resources/captions/module2/2-1-data-center-overview-1080p.vtt",
        "language": "en",
        "label": "English (transcribed)"
      }
    ],
    "caption_cues": [
      {
        "start": 3.44,
        "end": 7.34,
        "text": "When you picture a data center, what comes\nto mind? Maybe a secure"
      },
      {
        "start": 7.42,
        "end": 11.38,
        "text": "building with rows of servers glowing in\ngreen light. That's not wrong,"
      },
      {
        "start": 11.6,
        "end": 15.3,
        "text": "but it's only the surface. Data centers\nare engineered"
      },
      {
        "start": 15.4,
        "end": 19.36,
        "text": "ecosystems optimized for nonstop digital\noperations."
      },
      {
        "start": 20.62,
        "end": 24.2,
        "text": "In this video, we'll take a look at how\nthey're physically structured from"
      },
      {
        "start": 24.24,
        "end": 27.98,
        "text": "the ground up. The first thing to\nunderstand is that"
      },
      {
        "start": 28.08,
        "end": 31.98,
        "text": "everything in a data center is built for\nmaximum uptime. Whether you're"
      },
      {
        "start": 32.08,
        "end": 35.42,
        "text": "streaming a video, sending an email, or\njust using cloud"
      },
      {
        "start": 35.48,
        "end": 39.02,
        "text": "applications somewhere, a data center is\npowering that"
      },
      {
        "start": 39.06,
        "end": 43.06,
        "text": "experience. To stay online twenty-four\nseven,"
      },
      {
        "start": 43.32,
        "end": 47.06,
        "text": "a data center needs three core systems,\nand they all work together."
      },
      {
        "start": 47.2,
        "end": 49.68,
        "text": "They're power, cooling, and IT equipment."
      },
      {
        "start": 51.24,
        "end": 54.98,
        "text": "Let's start with cooling because heat is\none of the biggest"
      },
      {
        "start": 55.14,
        "end": 59.04,
        "text": "enemies of performance. Data centers\ngenerate a lot"
      },
      {
        "start": 59.08,
        "end": 62.44,
        "text": "of heat. On the outside, you'll see\nindustrial-grade chillers,"
      },
      {
        "start": 62.54,
        "end": 66.42,
        "text": "condensers, and cooling towers. These\nsystems work"
      },
      {
        "start": 66.46,
        "end": 70.02,
        "text": "to remove heat from the building through a\nmix of air and liquid cold"
      },
      {
        "start": 70.06,
        "end": 73.96,
        "text": "methods. Inside, air handling units, also\nknown as CRACs,"
      },
      {
        "start": 74.32,
        "end": 78.12,
        "text": "Computer Room Air Conditioners, keep\ntemperatures in check by distributing"
      },
      {
        "start": 78.38,
        "end": 82.1,
        "text": "cold air across the data hall. For liquid-\ncooled servers,"
      },
      {
        "start": 82.5,
        "end": 86.18,
        "text": "cooling distribution units, or CDUs,\nensure cold"
      },
      {
        "start": 86.24,
        "end": 90.06,
        "text": "liquid keeps the servers cool. These\nsystems"
      },
      {
        "start": 90.28,
        "end": 93.92,
        "text": "often operate in tandem with raised floors\nand cold aisle"
      },
      {
        "start": 93.96,
        "end": 97.82,
        "text": "containments. They also include smart\nsensors. Now let's talk"
      },
      {
        "start": 97.88,
        "end": 101.72,
        "text": "about power. At the heart of any data\ncenter is an incredibly robust"
      },
      {
        "start": 101.78,
        "end": 105.42,
        "text": "energy system. Power typically enters from\nutility"
      },
      {
        "start": 105.5,
        "end": 109.22,
        "text": "lines from the grid or renewable sources\nand runs through medium and low"
      },
      {
        "start": 109.26,
        "end": 113.16,
        "text": "voltage switchgear. From here, it's fed\nvia backup"
      },
      {
        "start": 113.24,
        "end": 116.8,
        "text": "systems, diesel generators, and UPSs, or"
      },
      {
        "start": 116.96,
        "end": 120.54,
        "text": "uninterruptible power supplies for short.\nThese are banks of"
      },
      {
        "start": 120.58,
        "end": 124.04,
        "text": "batteries and help keep the data center\nrunning during"
      },
      {
        "start": 124.12,
        "end": 127.84,
        "text": "outages or grid instability. Once\nstabilized,"
      },
      {
        "start": 128.12,
        "end": 131.82,
        "text": "power is distributed through PDUs, or\npower distribution"
      },
      {
        "start": 131.9,
        "end": 135.42,
        "text": "units, and sometimes even intelligent\nbusbars that reduce"
      },
      {
        "start": 135.46,
        "end": 139.22,
        "text": "complexity in cable routing. All of this"
      },
      {
        "start": 139.28,
        "end": 142.96,
        "text": "ensures that each server receives\nconsistent, safe"
      },
      {
        "start": 143.34,
        "end": 147.24,
        "text": "electricity. The layout of a data center\nalso"
      },
      {
        "start": 147.28,
        "end": 151.22,
        "text": "plays a major role. Most are designed with\nhot and cold aisle containments"
      },
      {
        "start": 151.44,
        "end": 155.28,
        "text": "to keep airflow controlled and cooling\nefficient. Sensors track"
      },
      {
        "start": 155.32,
        "end": 158.36,
        "text": "temperature, humidity, and power usage in\nreal time."
      },
      {
        "start": 160.1,
        "end": 164.0,
        "text": "Centralized control systems allow\ntechnicians to automate responses and"
      },
      {
        "start": 164.18,
        "end": 167.96,
        "text": "optimize system performance remotely.\nIncreasingly, data"
      },
      {
        "start": 167.98,
        "end": 171.74,
        "text": "centers are becoming more sustainable.\nSome include microgrids,"
      },
      {
        "start": 172.16,
        "end": 175.86,
        "text": "solar panels, or fuel cell systems to\nreduce reliance on"
      },
      {
        "start": 175.9,
        "end": 179.8,
        "text": "public utilities and carbon output. Rack-\nlevel equipment"
      },
      {
        "start": 179.82,
        "end": 183.64,
        "text": "has also evolved. Racks are designed not\nonly for high-density"
      },
      {
        "start": 183.72,
        "end": 187.18,
        "text": "performance but also for efficient\nairflow, liquid cooling,"
      },
      {
        "start": 187.5,
        "end": 190.14,
        "text": "cable management, and environmental\nsensing."
      },
      {
        "start": 191.46,
        "end": 195.42,
        "text": "All these systems, cooling, power, and\nmonitoring, are"
      },
      {
        "start": 195.48,
        "end": 198.48,
        "text": "coordinated to keep the data center\nreliable and secure."
      },
      {
        "start": 199.42,
        "end": 203.4,
        "text": "Downtime isn't an option when you're\nsupporting financial markets, hospitals,"
      },
      {
        "start": 203.6,
        "end": 207.14,
        "text": "or global communication platforms. So to\nsummarize,"
      },
      {
        "start": 207.58,
        "end": 210.54,
        "text": "data centers are more than just rows of\nservers."
      },
      {
        "start": 211.92,
        "end": 215.54,
        "text": "They are intricately designed\ninfrastructures combining engineering,"
      },
      {
        "start": 215.94,
        "end": 219.9,
        "text": "IT, and environmental controls. Each"
      },
      {
        "start": 219.96,
        "end": 223.72,
        "text": "component, chillers, batteries, busbars,\nand racks, has a"
      },
      {
        "start": 223.78,
        "end": 227.76,
        "text": "role in keeping your digital world up and\nrunning. In the"
      },
      {
        "start": 227.82,
        "end": 231.1,
        "text": "next lesson, we'll zoom in on how data\ncenters handle power"
      },
      {
        "start": 231.18,
        "end": 235.1,
        "text": "distribution and why energy systems are\none of the most"
      },
      {
        "start": 235.22,
        "end": 237.88,
        "text": "critical components in digital operations."
      }
    ],
    "assets": [
      "resources/captions/module2/2-1-data-center-overview-1080p.vtt"
    ],
    "text_inventory": {
      "sha256": "6b694529e9d196954c3bade8a1d92a789b9b0903fe3ea0e59ca75de8cb564da8",
      "entries": [
        {
          "text": "OPEN",
          "at_seconds": 2.5
        },
        {
          "text": "Compute Project®",
          "at_seconds": 2.5
        },
        {
          "text": "DATA CENTERS",
          "at_seconds": 17.5
        },
        {
          "text": "ARE ENGINEERED ECOSYSTEMS, OPTIMIZED",
          "at_seconds": 17.5
        },
        {
          "text": "FOR NONSTOP DIGITAL OPER",
          "at_seconds": 17.5
        },
        {
          "text": "THE FIRST THING TO UNDERSTAND IS",
          "at_seconds": 27.5
        },
        {
          "text": "STREAMING A",
          "at_seconds": 32.5
        },
        {
          "text": "VIDEO",
          "at_seconds": 32.5
        },
        {
          "text": "USING CLOUD",
          "at_seconds": 37.5
        },
        {
          "text": "APPLICATIONS",
          "at_seconds": 37.5
        },
        {
          "text": "CORE SYSTEMS:",
          "at_seconds": 42.5
        },
        {
          "text": "POWER - COOLING - IT EQUIPMENT",
          "at_seconds": 47.5
        },
        {
          "text": "LET'S START WITH COOLING BECAUSE",
          "at_seconds": 52.5
        },
        {
          "text": "DATA CE",
          "at_seconds": 57.5
        },
        {
          "text": "DATA CENTERS GENERATE A LOT OF HEAT",
          "at_seconds": 62.5
        },
        {
          "text": "INDUSTRIAL-GRADE CHILLERS",
          "at_seconds": 62.5
        },
        {
          "text": "CONDENSERS",
          "at_seconds": 62.5
        },
        {
          "text": "CRACS",
          "at_seconds": 77.5
        },
        {
          "text": "THESE SYSTEMS OFTEN OPERATE IN TANDEM WITH",
          "at_seconds": 92.5
        },
        {
          "text": "RAISED FLOORS",
          "at_seconds": 92.5
        },
        {
          "text": "POWER",
          "at_seconds": 102.5
        },
        {
          "text": "AT THE HEART OF ANY DATA CENTER IS",
          "at_seconds": 102.5
        },
        {
          "text": "AN INCREDIBLY ROBUST ENERGY SYSTEM",
          "at_seconds": 102.5
        },
        {
          "text": "POWER GRID TRANSFORMER",
          "at_seconds": 107.5
        },
        {
          "text": "SWITCHGEAR",
          "at_seconds": 107.5
        },
        {
          "text": "POWER GRID",
          "at_seconds": 112.5
        },
        {
          "text": "TRANSFORMER",
          "at_seconds": 112.5
        },
        {
          "text": "UPS's",
          "at_seconds": 117.5
        },
        {
          "text": "GENERATORS",
          "at_seconds": 117.5
        },
        {
          "text": "POWER DISTRIBUTION UNITS",
          "at_seconds": 127.5
        },
        {
          "text": "POWER DISTRIBUTION",
          "at_seconds": 132.5
        },
        {
          "text": "UNITS (PDUs)",
          "at_seconds": 132.5
        },
        {
          "text": "Di",
          "at_seconds": 132.5
        },
        {
          "text": "ПШ",
          "at_seconds": 132.5
        },
        {
          "text": "1atth",
          "at_seconds": 152.5
        },
        {
          "text": "CENTRALIZED CONTROL SYSTEMS",
          "at_seconds": 162.5
        },
        {
          "text": "ALLOW TECHNICIANS TO AUTOMATE",
          "at_seconds": 162.5
        },
        {
          "text": "MICROGRIDS",
          "at_seconds": 172.5
        },
        {
          "text": "SOLAR PANELS",
          "at_seconds": 172.5
        },
        {
          "text": "FUEL CELL SYSTEMS",
          "at_seconds": 177.5
        },
        {
          "text": "// |/ |/|//",
          "at_seconds": 182.5
        },
        {
          "text": "• HIGH-DENSITY PERFORMANCE",
          "at_seconds": 187.5
        },
        {
          "text": "• EFFICIENT AIRFLOW",
          "at_seconds": 187.5
        },
        {
          "text": "• CABL",
          "at_seconds": 187.5
        },
        {
          "text": "ALL THESE SYSTEMS, COOLING, POWER,",
          "at_seconds": 192.5
        },
        {
          "text": "AND MONITORING, ARE COORDINATED",
          "at_seconds": 197.5
        },
        {
          "text": "TO KEEP THE DATA CENTER",
          "at_seconds": 197.5
        },
        {
          "text": "RELIABLE AND SECU",
          "at_seconds": 197.5
        },
        {
          "text": "DOWNTIME = RISK",
          "at_seconds": 202.5
        },
        {
          "text": "DATACENTERS",
          "at_seconds": 207.5
        },
        {
          "text": "ARE MORE THAN JUST ROWS OF SERVERS",
          "at_seconds": 207.5
        },
        {
          "text": "• ENGINEERING",
          "at_seconds": 217.5
        },
        {
          "text": "• IT",
          "at_seconds": 217.5
        },
        {
          "text": "• ENVIRONMENTAL CONTROL",
          "at_seconds": 217.5
        },
        {
          "text": "EACH COMPONENT, CHILLERS,",
          "at_seconds": 222.5
        },
        {
          "text": "BATTERIES, BUSBARS, AND RACKS,",
          "at_seconds": 222.5
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    },
    "source_poster": "resources/images/module2/2-1-data-center-overview-1080p.jpg"
  },
  "audio": null,
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 2
    }
  ],
  "video_transcript": "When you picture a data center, what comes to mind? Maybe a secure building with rows of servers glowing in green light. That's not wrong, but it's only the surface. Data centers are engineered ecosystems optimized for nonstop digital operations. In this video, we'll take a look at how they're physically structured from the ground up. The first thing to understand is that everything in a data center is built for maximum uptime. Whether you're streaming a video, sending an email, or just using cloud applications somewhere, a data center is powering that experience. To stay online twenty-four seven, a data center needs three core systems, and they all work together. They're power, cooling, and IT equipment. Let's start with cooling because heat is one of the biggest enemies of performance. Data centers generate a lot of heat. On the outside, you'll see industrial-grade chillers, condensers, and cooling towers. These systems work to remove heat from the building through a mix of air and liquid cold methods. Inside, air handling units, also known as CRACs, Computer Room Air Conditioners, keep temperatures in check by distributing cold air across the data hall. For liquid-cooled servers, cooling distribution units, or CDUs, ensure cold liquid keeps the servers cool. These systems often operate in tandem with raised floors and cold aisle containments. They also include smart sensors. Now let's talk about power. At the heart of any data center is an incredibly robust energy system. Power typically enters from utility lines from the grid or renewable sources and runs through medium and low voltage switchgear. From here, it's fed via backup systems, diesel generators, and UPSs, or uninterruptible power supplies for short. These are banks of batteries and help keep the data center running during outages or grid instability. Once stabilized, power is distributed through PDUs, or power distribution units, and sometimes even intelligent busbars that reduce complexity in cable routing. All of this ensures that each server receives consistent, safe electricity. The layout of a data center also plays a major role. Most are designed with hot and cold aisle containments to keep airflow controlled and cooling efficient. Sensors track temperature, humidity, and power usage in real time. Centralized control systems allow technicians to automate responses and optimize system performance remotely. Increasingly, data centers are becoming more sustainable. Some include microgrids, solar panels, or fuel cell systems to reduce reliance on public utilities and carbon output. Rack-level equipment has also evolved. Racks are designed not only for high-density performance but also for efficient airflow, liquid cooling, cable management, and environmental sensing. All these systems, cooling, power, and monitoring, are coordinated to keep the data center reliable and secure. Downtime isn't an option when you're supporting financial markets, hospitals, or global communication platforms. So to summarize, data centers are more than just rows of servers. They are intricately designed infrastructures combining engineering, IT, and environmental controls. Each component, chillers, batteries, busbars, and racks, has a role in keeping your digital world up and running. In the next lesson, we'll zoom in on how data centers handle power distribution and why energy systems are one of the most critical components in digital operations. ",
  "term_refs": [
    "power",
    "energy",
    "cloud_computing",
    "ups",
    "pdu",
    "crac",
    "crah",
    "cdu"
  ],
  "narration_enabled": false,
  "transcript": "When you picture a data center, what comes to mind? Maybe a secure building with rows of servers glowing in green light. That's not wrong, but it's only the surface. Data centers are engineered ecosystems optimized for nonstop digital operations. In this video, we'll take a look at how they're physically structured from the ground up. The first thing to understand is that everything in a data center is built for maximum uptime. Whether you're streaming a video, sending an email, or just using cloud applications somewhere, a data center is powering that experience. To stay online twenty-four seven, a data center needs three core systems, and they all work together. They're power, cooling, and IT equipment. Let's start with cooling because heat is one of the biggest enemies of performance. Data centers generate a lot of heat. On the outside, you'll see industrial-grade chillers, condensers, and cooling towers. These systems work to remove heat from the building through a mix of air and liquid cold methods. Inside, air handling units, also known as CRACs, Computer Room Air Conditioners, keep temperatures in check by distributing cold air across the data hall. For liquid-cooled servers, cooling distribution units, or CDUs, ensure cold liquid keeps the servers cool. These systems often operate in tandem with raised floors and cold aisle containments. They also include smart sensors. Now let's talk about power. At the heart of any data center is an incredibly robust energy system. Power typically enters from utility lines from the grid or renewable sources and runs through medium and low voltage switchgear. From here, it's fed via backup systems, diesel generators, and UPSs, or uninterruptible power supplies for short. These are banks of batteries and help keep the data center running during outages or grid instability. Once stabilized, power is distributed through PDUs, or power distribution units, and sometimes even intelligent busbars that reduce complexity in cable routing. All of this ensures that each server receives consistent, safe electricity. The layout of a data center also plays a major role. Most are designed with hot and cold aisle containments to keep airflow controlled and cooling efficient. Sensors track temperature, humidity, and power usage in real time. Centralized control systems allow technicians to automate responses and optimize system performance remotely. Increasingly, data centers are becoming more sustainable. Some include microgrids, solar panels, or fuel cell systems to reduce reliance on public utilities and carbon output. Rack-level equipment has also evolved. Racks are designed not only for high-density performance but also for efficient airflow, liquid cooling, cable management, and environmental sensing. All these systems, cooling, power, and monitoring, are coordinated to keep the data center reliable and secure. Downtime isn't an option when you're supporting financial markets, hospitals, or global communication platforms. So to summarize, data centers are more than just rows of servers. They are intricately designed infrastructures combining engineering, IT, and environmental controls. Each component, chillers, batteries, busbars, and racks, has a role in keeping your digital world up and running. In the next lesson, we'll zoom in on how data centers handle power distribution and why energy systems are one of the most critical components in digital operations. "
}
```

### Active spoken narration
None; imported recording owns the audio. Its transcript and caption cues are in the slide fields.

## M2S4: The Data Hall Depends on Support Systems
Type: content_diagram

### Authored slide fields
```json
{
  "id": 4,
  "type": "content_diagram",
  "slug": "facility_dependencies",
  "title": "The Data Hall Depends on Support Systems",
  "section_label": "Facility Context",
  "figure": {
    "path": "figures/module2/facility-dependencies.svg",
    "source": "custom",
    "alt": "IT equipment and facility support systems form one operating system.",
    "caption": "IT equipment and facility support systems form one operating system.",
    "design": {
      "layout": "layers",
      "nodes": [
        "IT equipment in the data hall",
        "Power delivery and heat removal",
        "Building, access and supporting infrastructure"
      ]
    },
    "text_inventory": {
      "sha256": "aebc985c054a9f7fc514f5df415072dff01a624bb2735d96f0ca7ed5ce9834fb",
      "entries": [
        {
          "text": "IT equipment in the data hall"
        },
        {
          "text": "Power delivery and heat removal"
        },
        {
          "text": "Building, access and supporting infrastructure"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module2/slide_04_facility_dependencies.txt",
    "wav_file": "audio/module2/slide_04_facility_dependencies.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 2
    }
  ]
}
```

### Active spoken narration
The data hall is the part many people picture first, but the equipment depends on systems beyond the racks. Electrical infrastructure brings power to the load. Cooling infrastructure transfers heat away from it. The building provides space, access and protection.

Teams sometimes call the IT area white space and the supporting infrastructure grey space. The boundary is useful for coordination; the service still depends on both.


### Visible static figure text
IT equipment in the data hall
Power delivery and heat removal
Building, access and supporting infrastructure

## M2S5: How Power Reaches the Data Hall
Type: content_diagram

### Authored slide fields
```json
{
  "id": 5,
  "type": "content_diagram",
  "slug": "2_2_power_infrastructure_1080p",
  "title": "How Power Reaches the Data Hall",
  "section_label": "Explanatory Video",
  "media_focus": true,
  "figure": {
    "path": "resources/videos/module2/2-2-power-infrastructure-1080p.mp4",
    "poster": "resources/images/module2/video-slide-5-poster.jpg",
    "media_type": "video",
    "role": "original_video",
    "source": "reuse",
    "autoplay": false,
    "loop": false,
    "muted": false,
    "controls": true,
    "alt": "How Power Reaches the Data Hall video.",
    "caption": "Backup generators are typically on standby. Startup time and supported load depend on the design. Rack-power figures are examples; fuel emissions depend on the supply chain.",
    "source_sha256": "ea9d9b8786789e2a862b642d9a606dd3fa5bce245b19b200996a43e5b4dd093c",
    "captions": [
      {
        "path": "resources/captions/module2/2-2-power-infrastructure-1080p.vtt",
        "language": "en",
        "label": "English (transcribed)"
      }
    ],
    "caption_cues": [
      {
        "start": 3.3,
        "end": 7.16,
        "text": "Imagine a hundred megawatt data center.\nJust to turn on the"
      },
      {
        "start": 7.22,
        "end": 11.16,
        "text": "lights, run servers, and maintain a stable\nenvironment requires"
      },
      {
        "start": 11.22,
        "end": 14.7,
        "text": "a massive and uninterrupted supply of\nelectricity."
      },
      {
        "start": 16.14,
        "end": 20.08,
        "text": "In this video, we'll explore how power\nflows into a data center"
      },
      {
        "start": 20.28,
        "end": 23.54,
        "text": "and what keeps it running even when the\ngrid goes down."
      },
      {
        "start": 24.54,
        "end": 28.52,
        "text": "Power begins at the utility level.\nElectricity is generated,"
      },
      {
        "start": 28.9,
        "end": 32.78,
        "text": "transmitted through the grid, and routed\nto a substation. From"
      },
      {
        "start": 32.84,
        "end": 36.5,
        "text": "there, voltage is stepped down and\ndelivered to the data"
      },
      {
        "start": 36.56,
        "end": 40.5,
        "text": "center through dedicated high-capacity\nlines. Once it"
      },
      {
        "start": 40.54,
        "end": 43.92,
        "text": "reaches the facility, the first stop is\nthe input switchgear."
      },
      {
        "start": 44.78,
        "end": 48.38,
        "text": "This equipment acts as a control hub,\ndistributing power to"
      },
      {
        "start": 48.44,
        "end": 52.22,
        "text": "critical systems and protecting them from\nfaults. Power"
      },
      {
        "start": 52.26,
        "end": 55.94,
        "text": "then flows into uninterruptible power\nsupplies or UPS"
      },
      {
        "start": 56.04,
        "end": 59.88,
        "text": "units. These systems maintain power during"
      },
      {
        "start": 59.92,
        "end": 63.66,
        "text": "brief outages or surges. If the grid cuts"
      },
      {
        "start": 63.78,
        "end": 66.34,
        "text": "out, UPS batteries provide power"
      },
      {
        "start": 66.72,
        "end": 70.42,
        "text": "instantaneously and offer a buffer of\npower to keep systems"
      },
      {
        "start": 70.5,
        "end": 73.84,
        "text": "online just long enough for generators to\nactivate."
      },
      {
        "start": 74.6,
        "end": 78.6,
        "text": "Next are the backup generators. They often\nrun on diesel or HVO."
      },
      {
        "start": 79.26,
        "end": 82.96,
        "text": "HVO is a more sustainable fuel than\ndiesel, and it's short for"
      },
      {
        "start": 83.02,
        "end": 86.96,
        "text": "hydrotreated vegetable oil. Now, these\ngenerators are"
      },
      {
        "start": 87.06,
        "end": 90.48,
        "text": "on continuously. They're always on\nstandby, and they"
      },
      {
        "start": 90.58,
        "end": 94.5,
        "text": "automatically supply full operational\npower within seconds"
      },
      {
        "start": 94.58,
        "end": 98.18,
        "text": "of an outage. Many data centers also use\nredundant"
      },
      {
        "start": 98.26,
        "end": 101.8,
        "text": "generator systems for added resilience.\nOnce"
      },
      {
        "start": 101.82,
        "end": 105.82,
        "text": "stabilized, power moves through redundant\nfeeds across the data centers"
      },
      {
        "start": 105.9,
        "end": 109.9,
        "text": "to the PDUs, the power distribution units.\nThese act like circuit"
      },
      {
        "start": 109.94,
        "end": 113.9,
        "text": "breaker panels for the data center. They\nallocate electricity to the various"
      },
      {
        "start": 113.96,
        "end": 117.92,
        "text": "systems in the IT rack, servers, storage\nunits,"
      },
      {
        "start": 118.18,
        "end": 122.0,
        "text": "or networking switchgear. PDUs ensure that\nevery"
      },
      {
        "start": 122.04,
        "end": 125.96,
        "text": "device down to the server level receives\nconsistent power."
      },
      {
        "start": 126.86,
        "end": 129.52,
        "text": "They also allow for monitoring and real-\ntime adjustments."
      },
      {
        "start": 130.9,
        "end": 134.9,
        "text": "Power density has become a major topic. A\nfew years ago,"
      },
      {
        "start": 135.3,
        "end": 139.22,
        "text": "the average rack might draw four or five\nkilowatts"
      },
      {
        "start": 139.26,
        "end": 143.02,
        "text": "of power. Today, it's common to see\nfifteen, thirty,"
      },
      {
        "start": 143.14,
        "end": 147.12,
        "text": "or even a hundred kilowatts of power usage\nper rack. For the near"
      },
      {
        "start": 147.2,
        "end": 151.1,
        "text": "future, some projections go as far as four\nhundred kilowatts or even"
      },
      {
        "start": 151.2,
        "end": 155.16,
        "text": "one megawatt. Now, these power densities\nare mostly driven by"
      },
      {
        "start": 155.18,
        "end": 158.6,
        "text": "the adoption of high-performance workloads\nsuch as AI."
      },
      {
        "start": 159.88,
        "end": 163.52,
        "text": "In daily operations, this entire\narchitecture runs in"
      },
      {
        "start": 163.56,
        "end": 167.5,
        "text": "harmony, but when something fails, it's\nthe coordination"
      },
      {
        "start": 167.54,
        "end": 171.26,
        "text": "between management tools, UPS systems,\nswitchgear, and"
      },
      {
        "start": 171.3,
        "end": 175.16,
        "text": "backup generators that prevents downtime.\nPower in a"
      },
      {
        "start": 175.2,
        "end": 177.88,
        "text": "data center is not just about electricity."
      },
      {
        "start": 179.16,
        "end": 182.9,
        "text": "It's about providing that power\ncontinuously. It's about"
      },
      {
        "start": 182.94,
        "end": 185.76,
        "text": "providing redundancy and proactive\nmanagement."
      },
      {
        "start": 187.2,
        "end": 191.08,
        "text": "Every second of uptime is critical,\nwhether it's"
      },
      {
        "start": 191.14,
        "end": 195.04,
        "text": "for financial markets, healthcare,\ngovernment, or your"
      },
      {
        "start": 195.1,
        "end": 196.16,
        "text": "cloud applications."
      }
    ],
    "assets": [
      "resources/captions/module2/2-2-power-infrastructure-1080p.vtt"
    ],
    "text_inventory": {
      "sha256": "ea9d9b8786789e2a862b642d9a606dd3fa5bce245b19b200996a43e5b4dd093c",
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
          "text": "HOW DATA CENTERS",
          "at_seconds": 7.5
        },
        {
          "text": "ARE POWERED",
          "at_seconds": 7.5
        },
        {
          "text": "HOW POWER FLOWS INTO",
          "at_seconds": 22.5
        },
        {
          "text": "A DATA CENTER AND WHAT",
          "at_seconds": 22.5
        },
        {
          "text": "KEEPS IT RUNNING",
          "at_seconds": 22.5
        },
        {
          "text": "HIGH-CAP",
          "at_seconds": 37.5
        },
        {
          "text": "INP",
          "at_seconds": 42.5
        },
        {
          "text": "N+1 SETUP",
          "at_seconds": 77.5
        },
        {
          "text": "BACKUP GENERATORS",
          "at_seconds": 77.5
        },
        {
          "text": "• CONTINUOUS STANDBY",
          "at_seconds": 87.5
        },
        {
          "text": "• SUPPLY FULL OPERATIONAL",
          "at_seconds": 92.5
        },
        {
          "text": "REDUNDAN",
          "at_seconds": 97.5
        },
        {
          "text": "GENERATOR",
          "at_seconds": 97.5
        },
        {
          "text": "S",
          "at_seconds": 97.5
        },
        {
          "text": "RPP",
          "at_seconds": 107.5
        },
        {
          "text": "POWER DISTRIBUTION",
          "at_seconds": 107.5
        },
        {
          "text": "UNITS (PDUs)",
          "at_seconds": 107.5
        },
        {
          "text": "IT/SERVER LOAD",
          "at_seconds": 107.5
        },
        {
          "text": "O.ll",
          "at_seconds": 127.5
        },
        {
          "text": "FOR MON",
          "at_seconds": 127.5
        },
        {
          "text": "kW/RACK",
          "at_seconds": 137.5
        },
        {
          "text": "15 kW",
          "at_seconds": 142.5
        },
        {
          "text": "MW",
          "at_seconds": 152.5
        },
        {
          "text": "400 kW",
          "at_seconds": 152.5
        },
        {
          "text": "AI AND HIGH-PERFORMANCE",
          "at_seconds": 157.5
        },
        {
          "text": "COMPUTING",
          "at_seconds": 157.5
        },
        {
          "text": "PREVENTS",
          "at_seconds": 167.5
        },
        {
          "text": "DOWNTIME",
          "at_seconds": 167.5
        },
        {
          "text": "MANAGEMENT",
          "at_seconds": 172.5
        },
        {
          "text": "TOOLS",
          "at_seconds": 172.5
        },
        {
          "text": "BACKUP",
          "at_seconds": 172.5
        },
        {
          "text": "GENERATORS",
          "at_seconds": 172.5
        },
        {
          "text": "UPS SYSTEMS",
          "at_seconds": 172.5
        },
        {
          "text": "SWITCHGEAR",
          "at_seconds": 172.5
        },
        {
          "text": "NOT JUST",
          "at_seconds": 177.5
        },
        {
          "text": "ELECTRICITY",
          "at_seconds": 177.5
        },
        {
          "text": "CONTINUITY",
          "at_seconds": 182.5
        },
        {
          "text": "EVERY SECO",
          "at_seconds": 187.5
        },
        {
          "text": "CRI",
          "at_seconds": 187.5
        },
        {
          "text": "EVERY SECONDIS",
          "at_seconds": 192.5
        },
        {
          "text": "CRITICAL",
          "at_seconds": 192.5
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    },
    "source_poster": "resources/images/module2/2-2-power-infrastructure-1080p.jpg"
  },
  "audio": null,
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 3
    }
  ],
  "video_transcript": "Imagine a hundred megawatt data center. Just to turn on the lights, run servers, and maintain a stable environment requires a massive and uninterrupted supply of electricity. In this video, we'll explore how power flows into a data center and what keeps it running even when the grid goes down. Power begins at the utility level. Electricity is generated, transmitted through the grid, and routed to a substation. From there, voltage is stepped down and delivered to the data center through dedicated high-capacity lines. Once it reaches the facility, the first stop is the input switchgear. This equipment acts as a control hub, distributing power to critical systems and protecting them from faults. Power then flows into uninterruptible power supplies or UPS units. These systems maintain power during brief outages or surges. If the grid cuts out, UPS batteries provide power instantaneously and offer a buffer of power to keep systems online just long enough for generators to activate. Next are the backup generators. They often run on diesel or HVO. HVO is a more sustainable fuel than diesel, and it's short for hydrotreated vegetable oil. Now, these generators are on continuously. They're always on standby, and they automatically supply full operational power within seconds of an outage. Many data centers also use redundant generator systems for added resilience. Once stabilized, power moves through redundant feeds across the data centers to the PDUs, the power distribution units. These act like circuit breaker panels for the data center. They allocate electricity to the various systems in the IT rack, servers, storage units, or networking switchgear. PDUs ensure that every device down to the server level receives consistent power. They also allow for monitoring and real-time adjustments. Power density has become a major topic. A few years ago, the average rack might draw four or five kilowatts of power. Today, it's common to see fifteen, thirty, or even a hundred kilowatts of power usage per rack. For the near future, some projections go as far as four hundred kilowatts or even one megawatt. Now, these power densities are mostly driven by the adoption of high-performance workloads such as AI. In daily operations, this entire architecture runs in harmony, but when something fails, it's the coordination between management tools, UPS systems, switchgear, and backup generators that prevents downtime. Power in a data center is not just about electricity. It's about providing that power continuously. It's about providing redundancy and proactive management. Every second of uptime is critical, whether it's for financial markets, healthcare, government, or your cloud applications. ",
  "term_refs": [
    "redundancy"
  ],
  "narration_enabled": false,
  "transcript": "Imagine a hundred megawatt data center. Just to turn on the lights, run servers, and maintain a stable environment requires a massive and uninterrupted supply of electricity. In this video, we'll explore how power flows into a data center and what keeps it running even when the grid goes down. Power begins at the utility level. Electricity is generated, transmitted through the grid, and routed to a substation. From there, voltage is stepped down and delivered to the data center through dedicated high-capacity lines. Once it reaches the facility, the first stop is the input switchgear. This equipment acts as a control hub, distributing power to critical systems and protecting them from faults. Power then flows into uninterruptible power supplies or UPS units. These systems maintain power during brief outages or surges. If the grid cuts out, UPS batteries provide power instantaneously and offer a buffer of power to keep systems online just long enough for generators to activate. Next are the backup generators. They often run on diesel or HVO. HVO is a more sustainable fuel than diesel, and it's short for hydrotreated vegetable oil. Now, these generators are on continuously. They're always on standby, and they automatically supply full operational power within seconds of an outage. Many data centers also use redundant generator systems for added resilience. Once stabilized, power moves through redundant feeds across the data centers to the PDUs, the power distribution units. These act like circuit breaker panels for the data center. They allocate electricity to the various systems in the IT rack, servers, storage units, or networking switchgear. PDUs ensure that every device down to the server level receives consistent power. They also allow for monitoring and real-time adjustments. Power density has become a major topic. A few years ago, the average rack might draw four or five kilowatts of power. Today, it's common to see fifteen, thirty, or even a hundred kilowatts of power usage per rack. For the near future, some projections go as far as four hundred kilowatts or even one megawatt. Now, these power densities are mostly driven by the adoption of high-performance workloads such as AI. In daily operations, this entire architecture runs in harmony, but when something fails, it's the coordination between management tools, UPS systems, switchgear, and backup generators that prevents downtime. Power in a data center is not just about electricity. It's about providing that power continuously. It's about providing redundancy and proactive management. Every second of uptime is critical, whether it's for financial markets, healthcare, government, or your cloud applications. "
}
```

### Active spoken narration
None; imported recording owns the audio. Its transcript and caption cues are in the slide fields.

## M2S6: Follow the Power Path
Type: content_diagram

### Authored slide fields
```json
{
  "id": 6,
  "type": "content_diagram",
  "slug": "power_continuity",
  "title": "Follow the Power Path",
  "section_label": "Power Continuity",
  "figure": {
    "path": "figures/module2/power-continuity.mp4",
    "poster": "figures/module2/power-continuity-poster.png",
    "media_type": "video",
    "source": "custom",
    "autoplay": false,
    "loop": false,
    "muted": true,
    "alt": "An illustrative UPS bridges a source transition while the load continues to receive power.",
    "caption": "An illustrative UPS bridges a source transition while the load continues to receive power.",
    "text_inventory": {
      "sha256": "86fe575673f39a6472f82ad1924d414131f45f9593d841822935e26553b7033d",
      "entries": [
        {
          "text": "Illustrative functional path · event spacing expanded",
          "at_seconds": 0
        },
        {
          "text": "Utility supply",
          "at_seconds": 0
        },
        {
          "text": "Distribution & source selection",
          "at_seconds": 0
        },
        {
          "text": "UPS",
          "at_seconds": 0
        },
        {
          "text": "Equipment",
          "at_seconds": 0
        },
        {
          "text": "Backup generator",
          "at_seconds": 0
        },
        {
          "text": "Stored energy",
          "at_seconds": 0
        },
        {
          "text": "Downstream distribution",
          "at_seconds": 0
        },
        {
          "text": "Illustrative reserve",
          "at_seconds": 0
        },
        {
          "text": "Standby",
          "at_seconds": 0
        },
        {
          "text": "Equipment supply",
          "at_seconds": 0
        },
        {
          "text": "Capacity",
          "at_seconds": 0
        },
        {
          "text": "Fuel",
          "at_seconds": 0
        },
        {
          "text": "Controls",
          "at_seconds": 0
        },
        {
          "text": "Maintenance",
          "at_seconds": 0
        },
        {
          "text": "Utility selected · equipment supplied",
          "at_seconds": 0
        },
        {
          "text": "UPS reserve bridges the source transition",
          "at_seconds": 0
        },
        {
          "text": "Ready backup selected · equipment supplied",
          "at_seconds": 0
        },
        {
          "text": "Starting",
          "at_seconds": 0
        },
        {
          "text": "Ready · not selected",
          "at_seconds": 0
        },
        {
          "text": "Ready · selected",
          "at_seconds": 0
        }
      ],
      "reviewed_on": "2026-10-24",
      "review_method": "Astra review of native-resolution causal scenes, measured final-v4 narration timestamps and decoded video states; root geometry and synchronized-player checks. Timing uses Scribe v2 word estimates, not perceptual listening approval."
    },
    "sync_to_narration": true,
    "animation_source": "animations/module2/power-continuity.html"
  },
  "audio": {
    "script_file": "audio/module2/slide_06_power_continuity.txt",
    "wav_file": "audio/module2/slide_06_power_continuity.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 3
    }
  ]
}
```

### Active spoken narration
In a conventional example, the normal supply passes through distribution and an uninterruptible power supply, or U P S, before reaching equipment. If the incoming source fails, stored energy can bridge the transition while a backup generator starts.

The animation illustrates that sequence. Actual designs differ, and backup operation depends on capacity, fuel, controls and maintenance. A generator alone doesn't mean there can be no interruption at the equipment.


## M2S7: Conversion and Expansion Happen Inside the Server
Type: content_two_column

### Authored slide fields
```json
{
  "id": 7,
  "type": "content_two_column",
  "slug": "server_functions",
  "title": "Conversion and Expansion Happen Inside the Server",
  "section_label": "Equipment Functions",
  "bullets": [
    {
      "text": "An AC-input supply converts AC to usable DC."
    },
    {
      "text": "PCIe cards add interfaces and specialized capabilities."
    },
    {
      "text": "Processing, working memory and persistent storage have different roles."
    }
  ],
  "figure": {
    "path": "figures/module2/server-functions.svg",
    "source": "custom",
    "alt": "Power conversion and PCIe expansion solve different equipment needs.",
    "caption": "Power conversion and PCIe expansion solve different equipment needs.",
    "design": {
      "layout": "grid",
      "nodes": [],
      "items": [
        [
          "Power supply",
          "AC input to usable DC"
        ],
        [
          "PCIe expansion",
          "Network, storage or accelerator interfaces"
        ],
        [
          "Processor and memory",
          "Execute work and hold active data"
        ],
        [
          "Persistent storage",
          "Retain information beyond a running process"
        ]
      ]
    },
    "text_inventory": {
      "sha256": "09d72f6b1d97c5c59da148b59ee9c1fae2db7a1faca3c9f35231ff5ebab12685",
      "entries": [
        {
          "text": "Power supply"
        },
        {
          "text": "AC input to usable DC"
        },
        {
          "text": "PCIe expansion"
        },
        {
          "text": "Network, storage or accelerator interfaces"
        },
        {
          "text": "Processor and memory"
        },
        {
          "text": "Execute work and hold active data"
        },
        {
          "text": "Persistent storage"
        },
        {
          "text": "Retain information beyond a running process"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module2/slide_07_server_functions.txt",
    "wav_file": "audio/module2/slide_07_server_functions.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 3
    }
  ],
  "term_refs": [
    "ac",
    "dc",
    "pcie"
  ]
}
```

### Active spoken narration
A conventional A C input server power supply converts alternating current into the lower-voltage direct current the equipment uses. Other rack architectures can deliver direct current through a shared power system, so the input arrangement matters.

Inside the server, P C I E, short for Peripheral Component Interconnect Express, supports expansion cards that add capabilities such as network interfaces, storage controllers or graphics processors. That role is different from the processor executing instructions, working memory holding active data, or a drive retaining stored information.


### Visible static figure text
Power supply
AC input to usable DC
PCIe expansion
Network, storage or accelerator  interfaces
Processor and memory
Execute work and hold active  data
Persistent storage
Retain information beyond a  running process

## M2S8: How Cooling Removes the Heat
Type: content_diagram

### Authored slide fields
```json
{
  "id": 8,
  "type": "content_diagram",
  "slug": "2_3_cooling_systems_1080p",
  "title": "How Cooling Removes the Heat",
  "section_label": "Explanatory Video",
  "media_focus": true,
  "figure": {
    "path": "resources/videos/module2/2-3-cooling-systems-1080p.mp4",
    "poster": "resources/images/module2/video-slide-8-poster.jpg",
    "media_type": "video",
    "role": "original_video",
    "source": "reuse",
    "autoplay": false,
    "loop": false,
    "muted": false,
    "controls": true,
    "alt": "How Cooling Removes the Heat video.",
    "caption": "Match operating temperatures to the equipment’s environmental requirements. Cooling levels alone do not establish redundancy; efficiency gains depend on the whole design.",
    "source_sha256": "49297d4050afcb4109353fe98d90e1ec575a2302c5c75d357627e1f24da959d4",
    "captions": [
      {
        "path": "resources/captions/module2/2-3-cooling-systems-1080p.vtt",
        "language": "en",
        "label": "English (transcribed)"
      }
    ],
    "caption_cues": [
      {
        "start": 3.48,
        "end": 6.4,
        "text": "In every data center, cooling is just as\ncritical as power."
      },
      {
        "start": 7.24,
        "end": 10.68,
        "text": "Servers and networking equipment generate\nheat continuously,"
      },
      {
        "start": 11.4,
        "end": 15.28,
        "text": "and if that heat isn't removed, equipment\nperformance can suffer"
      },
      {
        "start": 15.56,
        "end": 19.48,
        "text": "or, worse, fail completely. That's why\nmodern data centers"
      },
      {
        "start": 19.52,
        "end": 23.48,
        "text": "are engineered with robust cooling\nsystems. These systems work to"
      },
      {
        "start": 23.54,
        "end": 26.92,
        "text": "extract and dissipate heat efficiently,\nmaintaining the"
      },
      {
        "start": 27.38,
        "end": 30.82,
        "text": "optimal operating temperature and ensuring\nreliable uptime."
      },
      {
        "start": 32.2,
        "end": 36.16,
        "text": "So how do these systems work? First, let's\ntake a look at the heat"
      },
      {
        "start": 36.22,
        "end": 39.76,
        "text": "cycle. Heat is produced inside the servers\nand"
      },
      {
        "start": 39.82,
        "end": 43.68,
        "text": "transferred via the air through components\nlike fans or heat exchangers."
      },
      {
        "start": 44.22,
        "end": 47.9,
        "text": "The goal is to move the heat out of the\ndata center as efficient as"
      },
      {
        "start": 47.96,
        "end": 51.86,
        "text": "possible. One of the most common systems\nis air"
      },
      {
        "start": 51.92,
        "end": 55.8,
        "text": "cooling. This uses fans or computer room\nair"
      },
      {
        "start": 55.86,
        "end": 59.8,
        "text": "conditioning units, CRACs, to circulate\nair across hot"
      },
      {
        "start": 59.86,
        "end": 63.52,
        "text": "equipment. The warm air is then moved away\nand cooled,"
      },
      {
        "start": 63.84,
        "end": 67.66,
        "text": "either through chilled water systems or\nrefrigerants. Another"
      },
      {
        "start": 67.72,
        "end": 71.7,
        "text": "approach is liquid cooling, which has\nbecome more popular"
      },
      {
        "start": 71.76,
        "end": 75.5,
        "text": "with the increase in high-performance\ncomputing. These"
      },
      {
        "start": 75.56,
        "end": 79.34,
        "text": "systems use coolants, typically dielectric\nor"
      },
      {
        "start": 79.42,
        "end": 83.24,
        "text": "water-like fluids, to absorb heat directly\nfrom the hardware."
      },
      {
        "start": 83.96,
        "end": 87.94,
        "text": "In liquid cooling systems, cold liquid\nflows close to the"
      },
      {
        "start": 87.96,
        "end": 91.46,
        "text": "processor and other components. They\nabsorb the heat"
      },
      {
        "start": 92.22,
        "end": 96.0,
        "text": "and transport it away to be cooled again,\noften using"
      },
      {
        "start": 96.06,
        "end": 99.8,
        "text": "external heat exchangers or chillers. Data\ncenters"
      },
      {
        "start": 100.42,
        "end": 103.86,
        "text": "may also use evaporative cooling, also\nknown as"
      },
      {
        "start": 103.94,
        "end": 107.64,
        "text": "adiabatic cooling as well. This method\ncools air by"
      },
      {
        "start": 107.7,
        "end": 111.12,
        "text": "allowing water to evaporate into it. It's\nenergy"
      },
      {
        "start": 111.18,
        "end": 115.18,
        "text": "efficient and particularly useful in\nregions with dry climates."
      },
      {
        "start": 116.22,
        "end": 119.88,
        "text": "Another emerging cooling technology with\nliquid"
      },
      {
        "start": 119.98,
        "end": 123.64,
        "text": "cooling is immersion cooling. This is\nwhere servers are"
      },
      {
        "start": 123.88,
        "end": 127.58,
        "text": "fully submerged in a non-conductive\nliquid. This"
      },
      {
        "start": 127.64,
        "end": 131.48,
        "text": "liquid fully absorbs the heat directly\nfrom the hardware, offering"
      },
      {
        "start": 131.56,
        "end": 135.38,
        "text": "high efficient thermal transfers.\nImmersion cooling"
      },
      {
        "start": 135.52,
        "end": 139.5,
        "text": "reduces the need for mechanical fans. It\ncuts energy use and is"
      },
      {
        "start": 139.66,
        "end": 143.32,
        "text": "ideal for high-density computing, such as\nAI"
      },
      {
        "start": 143.38,
        "end": 147.18,
        "text": "workloads. Now, let's consider where"
      },
      {
        "start": 147.24,
        "end": 150.98,
        "text": "this cooling is happening. Cooling can be\nimplemented at"
      },
      {
        "start": 151.04,
        "end": 154.68,
        "text": "different levels: component level, rack\nlevel, room level, and"
      },
      {
        "start": 154.76,
        "end": 158.62,
        "text": "building level. Each level adds a layer of\nredundancy"
      },
      {
        "start": 158.92,
        "end": 162.56,
        "text": "and control. At the room level, hot and\ncold"
      },
      {
        "start": 162.66,
        "end": 166.66,
        "text": "aisles are often used. This technique\narranges servers in a way that"
      },
      {
        "start": 166.72,
        "end": 170.24,
        "text": "hot air is exhausted into one aisle while\ncold"
      },
      {
        "start": 170.34,
        "end": 174.2,
        "text": "air is directly into another, avoiding\nmixing the"
      },
      {
        "start": 174.26,
        "end": 178.02,
        "text": "two. From a systems view, heat is\ncollected and"
      },
      {
        "start": 178.08,
        "end": 181.74,
        "text": "transported and rejected outside the data\ncenter building"
      },
      {
        "start": 181.84,
        "end": 184.56,
        "text": "using chillers, condensers, and cooling\ntowers."
      },
      {
        "start": 185.9,
        "end": 189.48,
        "text": "Now, let's consider a power outage. During\nsuch"
      },
      {
        "start": 189.56,
        "end": 193.52,
        "text": "events, cooling systems, like IT systems,\nmust remain"
      },
      {
        "start": 193.6,
        "end": 197.54,
        "text": "operational. That's why they're often\nconnected to backup"
      },
      {
        "start": 197.6,
        "end": 201.56,
        "text": "power sources like UPS systems or diesel\ngenerators to"
      },
      {
        "start": 201.6,
        "end": 205.48,
        "text": "ensure continuity. Without adequate\ncooling,"
      },
      {
        "start": 206.2,
        "end": 210.02,
        "text": "even for a short time, equipment can reach\ncritical temperatures"
      },
      {
        "start": 210.28,
        "end": 214.14,
        "text": "quickly. This could lead to thermal\nthrottling or sudden"
      },
      {
        "start": 214.2,
        "end": 217.76,
        "text": "shutdowns, risking data loss or, worse,"
      },
      {
        "start": 218.04,
        "end": 222.0,
        "text": "hardware damage. In today's high-density\nenvironments, cooling is"
      },
      {
        "start": 222.06,
        "end": 225.02,
        "text": "about performance, efficiency, and\nreliability."
      },
      {
        "start": 225.9,
        "end": 229.84,
        "text": "Engineers must balance cooling capacity\nwith energy use"
      },
      {
        "start": 231.14,
        "end": 234.66,
        "text": "to optimize both operational cost and\nenvironmental"
      },
      {
        "start": 234.74,
        "end": 238.74,
        "text": "impact. One emerging strategy for\nimproving data center"
      },
      {
        "start": 238.8,
        "end": 242.8,
        "text": "efficiency is to increase the thermal set\npoint, the temperature at"
      },
      {
        "start": 242.86,
        "end": 246.62,
        "text": "which cooling systems begin operation.\nAccording to"
      },
      {
        "start": 246.72,
        "end": 250.66,
        "text": "ASHRAE guidelines, modern equipment can\nsafely operate at higher"
      },
      {
        "start": 250.72,
        "end": 254.56,
        "text": "inlet temperatures, often up to twenty-\nseven degrees"
      },
      {
        "start": 254.66,
        "end": 258.42,
        "text": "or eighty degrees Fahrenheit. By designing\naround these higher"
      },
      {
        "start": 258.54,
        "end": 262.019,
        "text": "temperatures or set points, data centers\ncan reduce"
      },
      {
        "start": 262.079,
        "end": 266.02,
        "text": "reliance on mechanical cooling. They can\nlower energy uses"
      },
      {
        "start": 266.06,
        "end": 269.72,
        "text": "and lower their environmental impact. As\ndata"
      },
      {
        "start": 269.76,
        "end": 273.6,
        "text": "centers grow and computing needs\nintensifies, smarter"
      },
      {
        "start": 273.66,
        "end": 276.86,
        "text": "and more sustainable cooling approaches\nlike liquid cooling,"
      },
      {
        "start": 277.22,
        "end": 280.92,
        "text": "evaporative methods, and higher set points\nwill become essential."
      },
      {
        "start": 281.56,
        "end": 285.56,
        "text": "They not only protect the equipment, but\nalso help organizations meet energy"
      },
      {
        "start": 285.62,
        "end": 287.54,
        "text": "efficiency and climate goals."
      }
    ],
    "assets": [
      "resources/captions/module2/2-3-cooling-systems-1080p.vtt"
    ],
    "text_inventory": {
      "sha256": "49297d4050afcb4109353fe98d90e1ec575a2302c5c75d357627e1f24da959d4",
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
          "text": "/1/",
          "at_seconds": 7.5
        },
        {
          "text": "Fhht",
          "at_seconds": 7.5
        },
        {
          "text": "DISSIPATE",
          "at_seconds": 27.5
        },
        {
          "text": "HEAT",
          "at_seconds": 27.5
        },
        {
          "text": "OPTIMAL",
          "at_seconds": 27.5
        },
        {
          "text": "TEMPERATURE",
          "at_seconds": 27.5
        },
        {
          "text": "BORRIOREED",
          "at_seconds": 42.5
        },
        {
          "text": "00 0 0",
          "at_seconds": 42.5
        },
        {
          "text": "AIR COOLING",
          "at_seconds": 52.5
        },
        {
          "text": "COMPUTER ROOM AIR",
          "at_seconds": 57.5
        },
        {
          "text": "CONDITIONING(CRAC)",
          "at_seconds": 57.5
        },
        {
          "text": "THESE SYSTEMS USE COOLANTS,",
          "at_seconds": 77.5
        },
        {
          "text": "T",
          "at_seconds": 77.5
        },
        {
          "text": "TYPICALLY WATER OR DIELECTRIC",
          "at_seconds": 82.5
        },
        {
          "text": "FLUIDS, TO ABSORB HEAT DIRECTLY",
          "at_seconds": 82.5
        },
        {
          "text": "FROM THE HARDV",
          "at_seconds": 82.5
        },
        {
          "text": "COLD PLATES",
          "at_seconds": 87.5
        },
        {
          "text": "REAR DOOR",
          "at_seconds": 87.5
        },
        {
          "text": "HEAT EXCHANGER",
          "at_seconds": 87.5
        },
        {
          "text": "EVAPORATIVE",
          "at_seconds": 102.5
        },
        {
          "text": "COOLING",
          "at_seconds": 102.5
        },
        {
          "text": "IMMERSION",
          "at_seconds": 117.5
        },
        {
          "text": "COO",
          "at_seconds": 117.5
        },
        {
          "text": "CHIP",
          "at_seconds": 152.5
        },
        {
          "text": "HOT AISLE",
          "at_seconds": 162.5
        },
        {
          "text": "COLD AISLE",
          "at_seconds": 162.5
        },
        {
          "text": "CHILLERS",
          "at_seconds": 182.5
        },
        {
          "text": "DURING SUCH EVENTS,",
          "at_seconds": 192.5
        },
        {
          "text": "COOLING SYSTEMS LIKE IT SYSTEMS,",
          "at_seconds": 192.5
        },
        {
          "text": "UPS SYSTEMS",
          "at_seconds": 202.5
        },
        {
          "text": "DIESEL GENERATORS",
          "at_seconds": 202.5
        },
        {
          "text": "COOLING IS ABOUT",
          "at_seconds": 222.5
        },
        {
          "text": "PERFORMANCE",
          "at_seconds": 222.5
        },
        {
          "text": "30 kW",
          "at_seconds": 227.5
        },
        {
          "text": "25 kW",
          "at_seconds": 227.5
        },
        {
          "text": "TO OPTIMIZE BOTH",
          "at_seconds": 232.5
        },
        {
          "text": "OPERATIONAL",
          "at_seconds": 232.5
        },
        {
          "text": "Winn",
          "at_seconds": 247.5
        },
        {
          "text": "Wiww",
          "at_seconds": 252.5
        },
        {
          "text": "ENERGY USE",
          "at_seconds": 267.5
        },
        {
          "text": "• LIQUID COOLING",
          "at_seconds": 277.5
        },
        {
          "text": "• EVAPORATIVE METHODS",
          "at_seconds": 277.5
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    },
    "source_poster": "resources/images/module2/2-3-cooling-systems-1080p.jpg"
  },
  "audio": null,
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 4
    }
  ],
  "video_transcript": "In every data center, cooling is just as critical as power. Servers and networking equipment generate heat continuously, and if that heat isn't removed, equipment performance can suffer or, worse, fail completely. That's why modern data centers are engineered with robust cooling systems. These systems work to extract and dissipate heat efficiently, maintaining the optimal operating temperature and ensuring reliable uptime. So how do these systems work? First, let's take a look at the heat cycle. Heat is produced inside the servers and transferred via the air through components like fans or heat exchangers. The goal is to move the heat out of the data center as efficient as possible. One of the most common systems is air cooling. This uses fans or computer room air conditioning units, CRACs, to circulate air across hot equipment. The warm air is then moved away and cooled, either through chilled water systems or refrigerants. Another approach is liquid cooling, which has become more popular with the increase in high-performance computing. These systems use coolants, typically dielectric or water-like fluids, to absorb heat directly from the hardware. In liquid cooling systems, cold liquid flows close to the processor and other components. They absorb the heat and transport it away to be cooled again, often using external heat exchangers or chillers. Data centers may also use evaporative cooling, also known as adiabatic cooling as well. This method cools air by allowing water to evaporate into it. It's energy efficient and particularly useful in regions with dry climates. Another emerging cooling technology with liquid cooling is immersion cooling. This is where servers are fully submerged in a non-conductive liquid. This liquid fully absorbs the heat directly from the hardware, offering high efficient thermal transfers. Immersion cooling reduces the need for mechanical fans. It cuts energy use and is ideal for high-density computing, such as AI workloads. Now, let's consider where this cooling is happening. Cooling can be implemented at different levels: component level, rack level, room level, and building level. Each level adds a layer of redundancy and control. At the room level, hot and cold aisles are often used. This technique arranges servers in a way that hot air is exhausted into one aisle while cold air is directly into another, avoiding mixing the two. From a systems view, heat is collected and transported and rejected outside the data center building using chillers, condensers, and cooling towers. Now, let's consider a power outage. During such events, cooling systems, like IT systems, must remain operational. That's why they're often connected to backup power sources like UPS systems or diesel generators to ensure continuity. Without adequate cooling, even for a short time, equipment can reach critical temperatures quickly. This could lead to thermal throttling or sudden shutdowns, risking data loss or, worse, hardware damage. In today's high-density environments, cooling is about performance, efficiency, and reliability. Engineers must balance cooling capacity with energy use to optimize both operational cost and environmental impact. One emerging strategy for improving data center efficiency is to increase the thermal set point, the temperature at which cooling systems begin operation. According to ASHRAE guidelines, modern equipment can safely operate at higher inlet temperatures, often up to twenty-seven degrees or eighty degrees Fahrenheit. By designing around these higher temperatures or set points, data centers can reduce reliance on mechanical cooling. They can lower energy uses and lower their environmental impact. As data centers grow and computing needs intensifies, smarter and more sustainable cooling approaches like liquid cooling, evaporative methods, and higher set points will become essential. They not only protect the equipment, but also help organizations meet energy efficiency and climate goals. ",
  "term_refs": [
    "cold_plate"
  ],
  "narration_enabled": false,
  "transcript": "In every data center, cooling is just as critical as power. Servers and networking equipment generate heat continuously, and if that heat isn't removed, equipment performance can suffer or, worse, fail completely. That's why modern data centers are engineered with robust cooling systems. These systems work to extract and dissipate heat efficiently, maintaining the optimal operating temperature and ensuring reliable uptime. So how do these systems work? First, let's take a look at the heat cycle. Heat is produced inside the servers and transferred via the air through components like fans or heat exchangers. The goal is to move the heat out of the data center as efficient as possible. One of the most common systems is air cooling. This uses fans or computer room air conditioning units, CRACs, to circulate air across hot equipment. The warm air is then moved away and cooled, either through chilled water systems or refrigerants. Another approach is liquid cooling, which has become more popular with the increase in high-performance computing. These systems use coolants, typically dielectric or water-like fluids, to absorb heat directly from the hardware. In liquid cooling systems, cold liquid flows close to the processor and other components. They absorb the heat and transport it away to be cooled again, often using external heat exchangers or chillers. Data centers may also use evaporative cooling, also known as adiabatic cooling as well. This method cools air by allowing water to evaporate into it. It's energy efficient and particularly useful in regions with dry climates. Another emerging cooling technology with liquid cooling is immersion cooling. This is where servers are fully submerged in a non-conductive liquid. This liquid fully absorbs the heat directly from the hardware, offering high efficient thermal transfers. Immersion cooling reduces the need for mechanical fans. It cuts energy use and is ideal for high-density computing, such as AI workloads. Now, let's consider where this cooling is happening. Cooling can be implemented at different levels: component level, rack level, room level, and building level. Each level adds a layer of redundancy and control. At the room level, hot and cold aisles are often used. This technique arranges servers in a way that hot air is exhausted into one aisle while cold air is directly into another, avoiding mixing the two. From a systems view, heat is collected and transported and rejected outside the data center building using chillers, condensers, and cooling towers. Now, let's consider a power outage. During such events, cooling systems, like IT systems, must remain operational. That's why they're often connected to backup power sources like UPS systems or diesel generators to ensure continuity. Without adequate cooling, even for a short time, equipment can reach critical temperatures quickly. This could lead to thermal throttling or sudden shutdowns, risking data loss or, worse, hardware damage. In today's high-density environments, cooling is about performance, efficiency, and reliability. Engineers must balance cooling capacity with energy use to optimize both operational cost and environmental impact. One emerging strategy for improving data center efficiency is to increase the thermal set point, the temperature at which cooling systems begin operation. According to ASHRAE guidelines, modern equipment can safely operate at higher inlet temperatures, often up to twenty-seven degrees or eighty degrees Fahrenheit. By designing around these higher temperatures or set points, data centers can reduce reliance on mechanical cooling. They can lower energy uses and lower their environmental impact. As data centers grow and computing needs intensifies, smarter and more sustainable cooling approaches like liquid cooling, evaporative methods, and higher set points will become essential. They not only protect the equipment, but also help organizations meet energy efficiency and climate goals. "
}
```

### Active spoken narration
None; imported recording owns the audio. Its transcript and caption cues are in the slide fields.

## M2S9: A Cooling System Moves Heat Out
Type: content_diagram

### Authored slide fields
```json
{
  "id": 9,
  "type": "content_diagram",
  "slug": "heat_path",
  "title": "A Cooling System Moves Heat Out",
  "section_label": "Thermal Path",
  "figure": {
    "path": "figures/module2/heat-path.svg",
    "source": "custom",
    "alt": "Heat moves from equipment through room and facility systems to the environment.",
    "caption": "Heat moves from equipment through room and facility systems to the environment.",
    "design": {
      "layout": "flow",
      "nodes": [
        "Equipment heat",
        "Room cooling",
        "Facility heat rejection",
        "Environment"
      ]
    },
    "text_inventory": {
      "sha256": "24c243379b9adc5c8ca542680ada7c5cf66c4d474703d29ee6a40707e69eac28",
      "entries": [
        {
          "text": "Equipment heat"
        },
        {
          "text": "Room cooling"
        },
        {
          "text": "Facility heat rejection"
        },
        {
          "text": "Environment"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "OCP cooling context",
      "url": "https://www.opencompute.org/projects/cooling-environments/"
    }
  ],
  "audio": {
    "script_file": "audio/module2/slide_09_heat_path.txt",
    "wav_file": "audio/module2/slide_09_heat_path.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 4
    }
  ]
}
```

### Active spoken narration
Cooling transfers heat through a chain of systems. In an air-cooled example, air passes through equipment, collects heat and returns to a cooling unit. Heat must then leave the building through the facility's heat-rejection arrangement.

A computer room air conditioner and a computer room air handler can perform similar room roles using different cooling arrangements. The useful question is where the heat goes next. Moving warm air around the room without removing its heat doesn't complete the process.


### Visible static figure text
Equipment heat
Room cooling
Facility heat  rejection
Environment

## M2S10: Keep Supply Air Apart from Exhaust
Type: content_diagram

### Authored slide fields
```json
{
  "id": 10,
  "type": "content_diagram",
  "slug": "airflow_separation",
  "title": "Keep Supply Air Apart from Exhaust",
  "section_label": "Airflow Management",
  "figure": {
    "path": "figures/module2/airflow-separation.svg",
    "source": "custom",
    "alt": "Containment separates equipment intake air from warm exhaust.",
    "caption": "Containment separates equipment intake air from warm exhaust.",
    "design": {
      "layout": "airflow",
      "nodes": []
    },
    "text_inventory": {
      "sha256": "4103ab0bf260148fb2688a0f0a1e2c305a6f34740ca841f4cfcfeff724737e78",
      "entries": [
        {
          "text": "Cool supply air"
        },
        {
          "text": "Equipment"
        },
        {
          "text": "Warm exhaust"
        },
        {
          "text": "Containment separates intake and return paths"
        },
        {
          "text": "Air delivery and room-system arrangements vary"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module2/slide_10_airflow_separation.txt",
    "wav_file": "audio/module2/slide_10_airflow_separation.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 5
    }
  ],
  "term_refs": [
    "containment"
  ]
}
```

### Active spoken narration
Airflow management keeps cool supply air available to equipment inlets and guides warm exhaust back to the cooling system. A cold aisle groups the intake sides; a hot aisle groups the exhaust sides. Containment separates those air streams.

Raised-floor delivery is one example, not a requirement for containment. Sensors and controls help teams understand temperatures and airflow. The layout and cooling system must work together rather than treat a single room temperature as the complete picture.


### Visible static figure text
Cool supply air
Equipment
Warm exhaust
Containment separates intake and return paths
Air delivery and room-system arrangements vary

## M2S11: Containment Reduces Air Mixing
Type: content_diagram

### Authored slide fields
```json
{
  "id": 11,
  "type": "content_diagram",
  "slug": "containment_effect",
  "title": "Containment Reduces Air Mixing",
  "section_label": "Airflow in Motion",
  "figure": {
    "path": "figures/module2/containment-flow.mp4",
    "poster": "figures/module2/containment-flow-poster.png",
    "media_type": "video",
    "source": "custom",
    "autoplay": false,
    "loop": false,
    "muted": true,
    "alt": "Separate supply and return paths reduce recirculation into equipment inlets.",
    "caption": "Separate supply and return paths reduce recirculation into equipment inlets.",
    "text_inventory": {
      "sha256": "641f4561628e6c3550a014479bac88729d3f3961c920b6da665beb5c454537d4",
      "entries": [
        {
          "text": "Cool supply",
          "at_seconds": 0
        },
        {
          "text": "Equipment row",
          "at_seconds": 0
        },
        {
          "text": "Warm return",
          "at_seconds": 0
        },
        {
          "text": "Contained return side",
          "at_seconds": 0
        },
        {
          "text": "Verify inlet conditions",
          "at_seconds": 0
        },
        {
          "text": "Airflow",
          "at_seconds": 0
        },
        {
          "text": "Cooling capacity",
          "at_seconds": 0
        },
        {
          "text": "Controls",
          "at_seconds": 0
        },
        {
          "text": "Mixing: exhaust can return toward the inlet",
          "at_seconds": 0
        },
        {
          "text": "Comparison: containment separates the return side",
          "at_seconds": 0
        },
        {
          "text": "Warmer mixed inlet",
          "at_seconds": 0
        },
        {
          "text": "Reduced recirculation",
          "at_seconds": 0
        }
      ],
      "reviewed_on": "2026-10-24",
      "review_method": "Astra review of native-resolution causal scenes, measured final-v4 narration timestamps and decoded video states; root geometry and synchronized-player checks. Timing uses Scribe v2 word estimates, not perceptual listening approval."
    },
    "sync_to_narration": true,
    "animation_source": "animations/module2/containment-flow.html"
  },
  "audio": {
    "script_file": "audio/module2/slide_11_containment_effect.txt",
    "wav_file": "audio/module2/slide_11_containment_effect.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 5
    }
  ]
}
```

### Active spoken narration
When exhaust mixes back into the intake stream, cooling capacity can be wasted and some equipment can receive warmer air than intended. The animation follows supply air through equipment and shows a separate return path.

Containment supports that separation. It still needs appropriate airflow, cooling capacity and controls. A barrier by itself doesn't prove that every equipment inlet receives the conditions it needs.


## M2S12: Effective Infrastructure Works as a System
Type: content_diagram

### Authored slide fields
```json
{
  "id": 12,
  "type": "content_diagram",
  "slug": "data_center_101_2_4_effective_infrastructure_1080p",
  "title": "Effective Infrastructure Works as a System",
  "section_label": "Explanatory Video",
  "media_focus": true,
  "figure": {
    "path": "resources/videos/module2/data-center-101-2-4-effective-infrastructure-1080p.mp4",
    "poster": "resources/images/module2/video-slide-12-poster.jpg",
    "media_type": "video",
    "role": "original_video",
    "source": "reuse",
    "autoplay": false,
    "loop": false,
    "muted": false,
    "controls": true,
    "alt": "Effective Infrastructure Works as a System video.",
    "caption": "Server size and storage reliability, power, cost and performance vary by product, workload and configuration.",
    "source_sha256": "b285f2360ddadaac1a89be5ca5cb0f7baf99648e2f6152985bc73b0276127ace",
    "captions": [
      {
        "path": "resources/captions/module2/data-center-101-2-4-effective-infrastructure-1080p.vtt",
        "language": "en",
        "label": "English (transcribed)"
      }
    ],
    "caption_cues": [
      {
        "start": 3.36,
        "end": 7.2,
        "text": "Let's take a look inside a typical server.\nWe'll focus on 2U, 2-socket"
      },
      {
        "start": 7.28,
        "end": 11.24,
        "text": "servers. They're most common in data\ncenters today. 2U"
      },
      {
        "start": 11.28,
        "end": 15.22,
        "text": "refers to the server's height in rack\nunits. It's roughly"
      },
      {
        "start": 15.38,
        "end": 19.02,
        "text": "3.5 inches tall, while 2-socket means it\ncan hold two"
      },
      {
        "start": 19.14,
        "end": 22.84,
        "text": "CPUs or processors. These processors work"
      },
      {
        "start": 22.88,
        "end": 26.84,
        "text": "together to handle high-performance tasks.\nInside the"
      },
      {
        "start": 26.9,
        "end": 30.66,
        "text": "server, we'll find several key components:\nthe CPU, the heat"
      },
      {
        "start": 30.74,
        "end": 34.12,
        "text": "sink, memory modules, PCIe cards for\nexpansion,"
      },
      {
        "start": 34.68,
        "end": 38.5,
        "text": "a power supply unit, hard drives or SSDs,\nand multiple"
      },
      {
        "start": 38.58,
        "end": 42.24,
        "text": "cooling fans. These components all work"
      },
      {
        "start": 42.28,
        "end": 46.26,
        "text": "together to process, store, and transmit\ndata across the network."
      },
      {
        "start": 47.98,
        "end": 51.46,
        "text": "The CPU, or processor, is the brain of the\nserver."
      },
      {
        "start": 52.08,
        "end": 55.68,
        "text": "It performs the calculations and\ninstructions that drive applications."
      },
      {
        "start": 56.26,
        "end": 59.78,
        "text": "It's paired with a heat sink and fans to\nmanage the heat it generates."
      },
      {
        "start": 61.14,
        "end": 64.94,
        "text": "Memory, or RAM, stores active data so the\nCPU"
      },
      {
        "start": 65.0,
        "end": 68.54,
        "text": "can quickly access it. Servers also\ninclude"
      },
      {
        "start": 68.74,
        "end": 72.68,
        "text": "PCIe expansion slots, which connect to the\nPCIe"
      },
      {
        "start": 72.88,
        "end": 76.84,
        "text": "bus. It's a high-speed pathway that allows\nthe server to add extra"
      },
      {
        "start": 76.88,
        "end": 80.78,
        "text": "capabilities. This might include GPUs"
      },
      {
        "start": 81.28,
        "end": 84.86,
        "text": "for artificial intelligence processing,\nnetwork interface cards,"
      },
      {
        "start": 85.52,
        "end": 89.26,
        "text": "or high-performance sto- storage\ncontrollers. These"
      },
      {
        "start": 89.3,
        "end": 92.72,
        "text": "components dramatically increase a\nserver's flexibility and"
      },
      {
        "start": 92.78,
        "end": 96.64,
        "text": "performance in specialized workloads.\nServers also"
      },
      {
        "start": 96.68,
        "end": 100.04,
        "text": "need fast, reliable storage. Hard drives\nand"
      },
      {
        "start": 100.14,
        "end": 104.08,
        "text": "solid-state drives, or SSDs, are used\ndepending on the performance"
      },
      {
        "start": 104.18,
        "end": 108.18,
        "text": "needs. SSDs offer faster"
      },
      {
        "start": 108.3,
        "end": 111.86,
        "text": "access times and better durability, making\nthem ideal for"
      },
      {
        "start": 111.9,
        "end": 115.68,
        "text": "high-transaction environments. Traditional\nspindle hard"
      },
      {
        "start": 115.76,
        "end": 119.68,
        "text": "drives offer more capacity for a lower\nprice but have lower performance"
      },
      {
        "start": 119.72,
        "end": 123.44,
        "text": "and require more power. And because they\nhave mechanical parts,"
      },
      {
        "start": 123.76,
        "end": 126.8,
        "text": "they are more likely to fail faster than\nSSDs."
      },
      {
        "start": 128.4,
        "end": 131.98,
        "text": "Of course, none of this would work without\npower. Power"
      },
      {
        "start": 132.04,
        "end": 135.88,
        "text": "supply is a critical component. It\nconverts electrical current from the"
      },
      {
        "start": 135.92,
        "end": 139.82,
        "text": "rack to usable power for the server's\ncomponents. It's"
      },
      {
        "start": 139.86,
        "end": 143.4,
        "text": "connected to a power distribution unit,\nand it has redundant"
      },
      {
        "start": 143.58,
        "end": 147.56,
        "text": "feeds, and there's even a redundant power\nsupply in a system"
      },
      {
        "start": 147.6,
        "end": 151.48,
        "text": "to ensure reliability. Cooling is another\ncritical"
      },
      {
        "start": 151.62,
        "end": 155.4,
        "text": "part of the IT infrastructure. Air flows\nfrom the cold"
      },
      {
        "start": 155.5,
        "end": 158.66,
        "text": "aisle, typically through perforated tiles\nin the floor in front of the"
      },
      {
        "start": 158.72,
        "end": 162.56,
        "text": "server, and it passes over the hot\ncomponents and"
      },
      {
        "start": 162.76,
        "end": 166.74,
        "text": "exits as warm air out the back. This\nairflow"
      },
      {
        "start": 166.8,
        "end": 170.04,
        "text": "ensures components stay within optimal\ntemperature range."
      },
      {
        "start": 171.08,
        "end": 174.34,
        "text": "Beyond servers, data centers rely on other\ninfrastructure."
      },
      {
        "start": 174.84,
        "end": 178.58,
        "text": "Networking equipment like routers and\nswitches connect servers and"
      },
      {
        "start": 178.64,
        "end": 181.74,
        "text": "devices across racks and even the\ninternet."
      },
      {
        "start": 183.08,
        "end": 186.46,
        "text": "Storage appliances manage vast amounts of\ndata,"
      },
      {
        "start": 186.84,
        "end": 190.18,
        "text": "structured and unstructured. Increasingly,"
      },
      {
        "start": 190.6,
        "end": 194.02,
        "text": "AI servers are also being developed. These\nare"
      },
      {
        "start": 194.1,
        "end": 197.96,
        "text": "high-powered machines equipped with\nspecialized GPUs to handle workloads like"
      },
      {
        "start": 198.0,
        "end": 201.84,
        "text": "machine learning and advanced analytics.\nThey typically require"
      },
      {
        "start": 202.24,
        "end": 206.22,
        "text": "higher power and cooling capacity. All of\nthese"
      },
      {
        "start": 206.28,
        "end": 209.68,
        "text": "systems must be highly connected and\nredundant."
      },
      {
        "start": 210.02,
        "end": 213.82,
        "text": "Redundant power feeds, network paths, and\ncomponent backups ensure"
      },
      {
        "start": 213.86,
        "end": 217.6,
        "text": "continuous uptime in servers. These\nredundant"
      },
      {
        "start": 217.74,
        "end": 221.44,
        "text": "architectures and connectivity are what\nmake a modern data"
      },
      {
        "start": 221.48,
        "end": 224.02,
        "text": "center both powerful and resilient."
      }
    ],
    "assets": [
      "resources/captions/module2/data-center-101-2-4-effective-infrastructure-1080p.vtt"
    ],
    "text_inventory": {
      "sha256": "b285f2360ddadaac1a89be5ca5cb0f7baf99648e2f6152985bc73b0276127ace",
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
          "text": "EFFECTIVE IT",
          "at_seconds": 7.5
        },
        {
          "text": "INFRASTRUCTURE",
          "at_seconds": 7.5
        },
        {
          "text": "3.5 IN",
          "at_seconds": 17.5
        },
        {
          "text": "2-SOCKET",
          "at_seconds": 17.5
        },
        {
          "text": "PROCESS",
          "at_seconds": 42.5
        },
        {
          "text": "THE BRAIN OF THE SERVER",
          "at_seconds": 52.5
        },
        {
          "text": "MEMORY, OR RAM, STORES ACTIVE DATA",
          "at_seconds": 62.5
        },
        {
          "text": "Cou",
          "at_seconds": 62.5
        },
        {
          "text": "PCle EXPANSION SLOTS",
          "at_seconds": 72.5
        },
        {
          "text": "• GPUS FOR AI PROCESSING",
          "at_seconds": 82.5
        },
        {
          "text": "• NETWORK INTERFACE CARDS",
          "at_seconds": 87.5
        },
        {
          "text": "• HIGH-PERFORMANCE STORAGE CONTROLLERS",
          "at_seconds": 87.5
        },
        {
          "text": "FLEXIBILITY",
          "at_seconds": 92.5
        },
        {
          "text": "SSD",
          "at_seconds": 102.5
        },
        {
          "text": "HDD",
          "at_seconds": 102.5
        },
        {
          "text": "SSDs: OFFER FASTER ACCESS TIMES AND BETTER",
          "at_seconds": 107.5
        },
        {
          "text": "DURABILITY, MAKING THEM IDEAL FOR HIGH-TRANSACTION",
          "at_seconds": 107.5
        },
        {
          "text": "ENVIRONMENTS",
          "at_seconds": 107.5
        },
        {
          "text": "HDDs: OFFER MORE CAPACITY FOR LOWER PRICE BUT",
          "at_seconds": 117.5
        },
        {
          "text": "HAVE LOWER PERFORMANCE, REQUIRE MORE POWER,",
          "at_seconds": 117.5
        },
        {
          "text": "AND BECAUSE THEY HAVE MECHANICAL PARTS, THEY ARE",
          "at_seconds": 117.5
        },
        {
          "text": "MORE LIKELY TO FAIL FASTER THAN SSDs",
          "at_seconds": 117.5
        },
        {
          "text": "STER ACCESS TIMES AND BETTER",
          "at_seconds": 127.5
        },
        {
          "text": "KING THEM IDEAL FOR HIGH-TRANSACTION",
          "at_seconds": 127.5
        },
        {
          "text": "ORE CAPACITY FOR LOWER PRICE BUT",
          "at_seconds": 127.5
        },
        {
          "text": "RFORMANCE, REQUIRE MORE POWER,",
          "at_seconds": 127.5
        },
        {
          "text": "HEY HAVE MECHANICAL PARTS, THEY ARE",
          "at_seconds": 127.5
        },
        {
          "text": "FAIL FASTER THAN SSDS",
          "at_seconds": 127.5
        },
        {
          "text": "REDUNDANT FEEDS AND REDUNDANT",
          "at_seconds": 147.5
        },
        {
          "text": "POWER SUPPLIES",
          "at_seconds": 147.5
        },
        {
          "text": "JJUUUUUUUUU",
          "at_seconds": 152.5
        },
        {
          "text": "THROUGH PERFORATED TILES IN THE",
          "at_seconds": 157.5
        },
        {
          "text": "1))",
          "at_seconds": 177.5
        },
        {
          "text": "CONNECTS SE",
          "at_seconds": 182.5
        },
        {
          "text": "RACKS AND",
          "at_seconds": 182.5
        },
        {
          "text": "STRUCTURED AND",
          "at_seconds": 187.5
        },
        {
          "text": "UNSTRUCTURED DATA",
          "at_seconds": 187.5
        },
        {
          "text": "Al",
          "at_seconds": 192.5
        },
        {
          "text": "VUCLLCCCLCL",
          "at_seconds": 192.5
        },
        {
          "text": "HIGHER POWER",
          "at_seconds": 202.5
        },
        {
          "text": "POWERFUL",
          "at_seconds": 222.5
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    },
    "source_poster": "resources/images/module2/data-center-101-2-4-effective-infrastructure-1080p.jpg"
  },
  "audio": null,
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 6
    }
  ],
  "video_transcript": "Let's take a look inside a typical server. We'll focus on 2U, 2-socket servers. They're most common in data centers today. 2U refers to the server's height in rack units. It's roughly 3.5 inches tall, while 2-socket means it can hold two CPUs or processors. These processors work together to handle high-performance tasks. Inside the server, we'll find several key components: the CPU, the heat sink, memory modules, PCIe cards for expansion, a power supply unit, hard drives or SSDs, and multiple cooling fans. These components all work together to process, store, and transmit data across the network. The CPU, or processor, is the brain of the server. It performs the calculations and instructions that drive applications. It's paired with a heat sink and fans to manage the heat it generates. Memory, or RAM, stores active data so the CPU can quickly access it. Servers also include PCIe expansion slots, which connect to the PCIe bus. It's a high-speed pathway that allows the server to add extra capabilities. This might include GPUs for artificial intelligence processing, network interface cards, or high-performance sto- storage controllers. These components dramatically increase a server's flexibility and performance in specialized workloads. Servers also need fast, reliable storage. Hard drives and solid-state drives, or SSDs, are used depending on the performance needs. SSDs offer faster access times and better durability, making them ideal for high-transaction environments. Traditional spindle hard drives offer more capacity for a lower price but have lower performance and require more power. And because they have mechanical parts, they are more likely to fail faster than SSDs. Of course, none of this would work without power. Power supply is a critical component. It converts electrical current from the rack to usable power for the server's components. It's connected to a power distribution unit, and it has redundant feeds, and there's even a redundant power supply in a system to ensure reliability. Cooling is another critical part of the IT infrastructure. Air flows from the cold aisle, typically through perforated tiles in the floor in front of the server, and it passes over the hot components and exits as warm air out the back. This airflow ensures components stay within optimal temperature range. Beyond servers, data centers rely on other infrastructure. Networking equipment like routers and switches connect servers and devices across racks and even the internet. Storage appliances manage vast amounts of data, structured and unstructured. Increasingly, AI servers are also being developed. These are high-powered machines equipped with specialized GPUs to handle workloads like machine learning and advanced analytics. They typically require higher power and cooling capacity. All of these systems must be highly connected and redundant. Redundant power feeds, network paths, and component backups ensure continuous uptime in servers. These redundant architectures and connectivity are what make a modern data center both powerful and resilient. ",
  "term_refs": [
    "cpu",
    "ram",
    "gpu",
    "ssd",
    "hdd",
    "rack_unit"
  ],
  "narration_enabled": false,
  "transcript": "Let's take a look inside a typical server. We'll focus on 2U, 2-socket servers. They're most common in data centers today. 2U refers to the server's height in rack units. It's roughly 3.5 inches tall, while 2-socket means it can hold two CPUs or processors. These processors work together to handle high-performance tasks. Inside the server, we'll find several key components: the CPU, the heat sink, memory modules, PCIe cards for expansion, a power supply unit, hard drives or SSDs, and multiple cooling fans. These components all work together to process, store, and transmit data across the network. The CPU, or processor, is the brain of the server. It performs the calculations and instructions that drive applications. It's paired with a heat sink and fans to manage the heat it generates. Memory, or RAM, stores active data so the CPU can quickly access it. Servers also include PCIe expansion slots, which connect to the PCIe bus. It's a high-speed pathway that allows the server to add extra capabilities. This might include GPUs for artificial intelligence processing, network interface cards, or high-performance sto- storage controllers. These components dramatically increase a server's flexibility and performance in specialized workloads. Servers also need fast, reliable storage. Hard drives and solid-state drives, or SSDs, are used depending on the performance needs. SSDs offer faster access times and better durability, making them ideal for high-transaction environments. Traditional spindle hard drives offer more capacity for a lower price but have lower performance and require more power. And because they have mechanical parts, they are more likely to fail faster than SSDs. Of course, none of this would work without power. Power supply is a critical component. It converts electrical current from the rack to usable power for the server's components. It's connected to a power distribution unit, and it has redundant feeds, and there's even a redundant power supply in a system to ensure reliability. Cooling is another critical part of the IT infrastructure. Air flows from the cold aisle, typically through perforated tiles in the floor in front of the server, and it passes over the hot components and exits as warm air out the back. This airflow ensures components stay within optimal temperature range. Beyond servers, data centers rely on other infrastructure. Networking equipment like routers and switches connect servers and devices across racks and even the internet. Storage appliances manage vast amounts of data, structured and unstructured. Increasingly, AI servers are also being developed. These are high-powered machines equipped with specialized GPUs to handle workloads like machine learning and advanced analytics. They typically require higher power and cooling capacity. All of these systems must be highly connected and redundant. Redundant power feeds, network paths, and component backups ensure continuous uptime in servers. These redundant architectures and connectivity are what make a modern data center both powerful and resilient. "
}
```

### Active spoken narration
None; imported recording owns the audio. Its transcript and caption cues are in the slide fields.

## M2S13: An Empty Rack Is Not Spare Capacity
Type: content_grid

### Authored slide fields
```json
{
  "id": 13,
  "type": "content_grid",
  "slug": "capacity_constraints",
  "title": "An Empty Rack Is Not Spare Capacity",
  "section_label": "Deployment Constraints",
  "grid_cols": 2,
  "cards": [
    {
      "title": "Space and structure",
      "body": "Rack positions, dimensions and supported weight."
    },
    {
      "title": "Power",
      "body": "Available capacity and the required delivery arrangement."
    },
    {
      "title": "Heat removal",
      "body": "Air or liquid capacity matched to the equipment."
    },
    {
      "title": "Connectivity and access",
      "body": "Network capability, cabling and service clearances."
    }
  ],
  "audio": {
    "script_file": "audio/module2/slide_13_capacity_constraints.txt",
    "wav_file": "audio/module2/slide_13_capacity_constraints.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 6
    }
  ]
}
```

### Active spoken narration
A rack may have open slots while its available electrical or thermal capacity is already committed. It may also lack suitable network connections, weight capacity or service access for the proposed equipment.

Before adding a workload, check the budgets together. Space tells you where equipment might fit. Power, heat removal, connectivity and access tell you whether it can operate and be maintained there. The first exhausted constraint can limit the whole deployment.


## M2S14: Liquid Cooling Adds a Heat-Transfer Path
Type: content_diagram

### Authored slide fields
```json
{
  "id": 14,
  "type": "content_diagram",
  "slug": "liquid_cooling_path",
  "title": "Liquid Cooling Adds a Heat-Transfer Path",
  "section_label": "Cooling Options",
  "figure": {
    "path": "figures/module2/liquid-cooling-path.svg",
    "source": "custom",
    "alt": "A liquid loop collects component heat; the next system must still reject it.",
    "caption": "A liquid loop collects component heat; the next system must still reject it.",
    "design": {
      "layout": "flow",
      "nodes": [
        "Component\ncold plate",
        "Equipment\ncoolant loop",
        "Heat transfer\ninterface",
        "Facility heat\nremoval"
      ]
    },
    "text_inventory": {
      "sha256": "0a58fbad87c5581b61d20b8af28b99b078400b03cbe281dbc263f7bcd5797fd0",
      "entries": [
        {
          "text": "Component cold plate"
        },
        {
          "text": "Equipment coolant loop"
        },
        {
          "text": "Heat transfer interface"
        },
        {
          "text": "Facility heat removal"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "OCP Cooling Environments",
      "url": "https://www.opencompute.org/projects/cooling-environments/"
    },
    {
      "label": "Brazos liquid-to-air example",
      "url": "https://cloud.google.com/blog/topics/systems/brazos-liquid-cooling-system-for-air-cooled-data-centers"
    }
  ],
  "audio": {
    "script_file": "audio/module2/slide_14_liquid_cooling_path.txt",
    "wav_file": "audio/module2/slide_14_liquid_cooling_path.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 4
    }
  ]
}
```

### Active spoken narration
Direct liquid cooling can collect heat at components through cold plates and carry it through a coolant circuit. A coolant distribution unit, or C D U, can manage the connection between the equipment loop and another heat-transfer system.

Liquid-to-air systems illustrate one retrofit approach: liquid collects heat from equipment, but room air ultimately carries that heat onward. The facility still needs sufficient power and heat rejection. Air and liquid cooling can coexist within one deployment.


### Visible static figure text
Component  cold plate
Equipment  coolant loop
Heat transfer  interface
Facility heat  removal

## M2S15: Open Interfaces Help Teams Coordinate
Type: content_diagram

### Authored slide fields
```json
{
  "id": 15,
  "type": "content_diagram",
  "slug": "open_interfaces",
  "title": "Open Interfaces Help Teams Coordinate",
  "section_label": "Shared Interfaces",
  "figure": {
    "path": "figures/module2/interface-coordination.svg",
    "source": "custom",
    "alt": "Equipment, facility and supplier requirements meet at defined interfaces.",
    "caption": "Equipment, facility and supplier requirements meet at defined interfaces.",
    "design": {
      "layout": "flow",
      "nodes": [
        "Equipment requirements",
        "Common interfaces",
        "Facility capabilities"
      ]
    },
    "text_inventory": {
      "sha256": "b4c2c501ff65557c9a76f985c33c863460a908ecb3f32491078955887b3445e6",
      "entries": [
        {
          "text": "Equipment requirements"
        },
        {
          "text": "Common interfaces"
        },
        {
          "text": "Facility capabilities"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "OCP power-interface work",
      "url": "https://www.opencompute.org/news/powering-the-next-era-of-ai-how-google-microsoft-and-nvidia-are-standardizing-and-accelerating-the-industry-transition-to-lvdc/"
    }
  ],
  "audio": {
    "script_file": "audio/module2/slide_15_open_interfaces.txt",
    "wav_file": "audio/module2/slide_15_open_interfaces.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 4
    }
  ]
}
```

### Active spoken narration
A rack's requirements cross organizational boundaries. Equipment designers, facility teams and suppliers need compatible electrical, mechanical and thermal interfaces.

Current community work on eight hundred volts direct current is an example of aligning requirements for demanding deployments. It is a developing option, not a statement that every facility should replace its existing alternating-current infrastructure. The broader lesson is that common interfaces can make different parts of a system easier to coordinate.


### Visible static figure text
Equipment  requirements
Common  interfaces
Facility  capabilities

## M2S16: Reliable Operation Requires the Whole Chain
Type: takeaways

### Authored slide fields
```json
{
  "id": 16,
  "type": "takeaways",
  "slug": "whole_chain_takeaways",
  "title": "Reliable Operation Requires the Whole Chain",
  "items": [
    "Power continuity depends on the complete supply and backup design.",
    "Cooling must transfer heat all the way out of the equipment and facility.",
    "Containment separates supply air from warm exhaust.",
    "Space, power, cooling, connectivity and access jointly limit deployment."
  ],
  "audio": {
    "script_file": "audio/module2/slide_16_whole_chain_takeaways.txt",
    "wav_file": "audio/module2/slide_16_whole_chain_takeaways.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 8
    }
  ]
}
```

### Active spoken narration
Power delivery and heat removal are connected parts of one system. Backup sources and energy storage have different roles. Airflow separation helps cooling do useful work, and liquid cooling adds another path for moving heat.

Free space is only one part of deployment capacity. Before changing the equipment, consider electrical delivery, thermal conditions, connectivity and service access together. That system view is the foundation for understanding what happens inside a rack.


## M2S17: Check the Function of Each Component
Type: knowledge_check

### Authored slide fields
```json
{
  "id": 17,
  "type": "knowledge_check",
  "slug": "component_functions_check",
  "title": "Check the Function of Each Component",
  "subtitle": "Answer both questions once. Read the feedback and retry whenever useful.",
  "questions": [
    {
      "id": "m2_kc1",
      "source_check_id": "M2-KC1",
      "prompt": "What is the primary function of the power supply in a conventional AC-input server?",
      "choices": [
        {
          "id": "a",
          "text": "Store backup data",
          "correct": false,
          "feedback_incorrect": "Backup data is retained by storage systems. The power supply converts and delivers electrical power to the equipment."
        },
        {
          "id": "b",
          "text": "Convert AC power to lower-voltage DC the server components can use",
          "correct": true
        },
        {
          "id": "c",
          "text": "Generate network traffic",
          "correct": false,
          "feedback_incorrect": "Processors and network interfaces handle communication. The power supply provides the electrical power those components need."
        },
        {
          "id": "d",
          "text": "Monitor cooling airflow",
          "correct": false,
          "feedback_incorrect": "Airflow monitoring uses sensors and management controls. The supply may have its own cooling, but its primary role is electrical conversion."
        }
      ],
      "feedback_correct": "For a conventional AC-input server, the supply converts AC into usable DC. DC-fed rack architectures use a different input arrangement.",
      "feedback_incorrect": "Match the component to electrical conversion rather than storage, communication or environmental monitoring."
    },
    {
      "id": "m2_kc2",
      "source_check_id": "M2-KC2",
      "prompt": "Which component expands a server’s I/O capabilities, often adding a GPU, network interface or storage controller?",
      "choices": [
        {
          "id": "a",
          "text": "CPU",
          "correct": false,
          "feedback_incorrect": "The CPU executes instructions. A PCIe expansion card connects an additional interface or specialized device to the system."
        },
        {
          "id": "b",
          "text": "RAM",
          "correct": false,
          "feedback_incorrect": "RAM holds active working data. It does not provide the expansion interface described in the question."
        },
        {
          "id": "c",
          "text": "PCIe card",
          "correct": true
        },
        {
          "id": "d",
          "text": "Hard disk",
          "correct": false,
          "feedback_incorrect": "A hard disk retains stored information. A PCIe card adds the interface or accelerator capability being tested here."
        }
      ],
      "feedback_correct": "PCIe expansion supports added capabilities such as networking, storage controllers and accelerators.",
      "feedback_incorrect": "Separate execution, working memory and storage from the role of an expansion card."
    }
  ],
  "audio": {
    "script_file": "audio/module2/slide_17_component_functions_check.txt",
    "wav_file": "audio/module2/slide_17_component_functions_check.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 7
    }
  ]
}
```

### Active spoken narration
These questions distinguish equipment functions. Consider what a conventional server power supply changes and what an expansion card adds. Submit each question once to continue. Correct answers aren't required, and the feedback explains the function associated with each choice so you can review and retry.


## M2S18: Next: Inside the Rack
Type: up_next

### Authored slide fields
```json
{
  "id": 18,
  "type": "up_next",
  "slug": "inside_the_rack_next",
  "title": "Next: Inside the Rack",
  "next_module_number": 3,
  "next_module_title": "Inside the Rack",
  "thank_you_message": "Thank you for completing Module 2: Data Center Physical Infrastructure.",
  "audio": {
    "script_file": "audio/module2/slide_18_inside_the_rack_next.txt",
    "wav_file": "audio/module2/slide_18_inside_the_rack_next.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m2",
      "lesson": 8
    }
  ]
}
```

### Active spoken narration
Thank you for completing Data Center Physical Infrastructure. You can now follow the power and heat-removal paths and recognize why deployment constraints belong together.

Module three brings that understanding into the rack. You'll interpret equipment dimensions, compare its roles and consider how a practical layout supports operation and maintenance.
