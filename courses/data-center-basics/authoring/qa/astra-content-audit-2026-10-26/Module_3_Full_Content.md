# Module 3: Inside the Rack
Course: Data Centers: From Digital Services to Physical Infrastructure
Review packet generated from the current editable course. Narration marked inactive is absent from the runtime.

## M3S1: Inside the Rack
Type: title

### Authored slide fields
```json
{
  "id": 1,
  "type": "title",
  "slug": "inside_the_rack",
  "title": "Inside the Rack",
  "subtitle": "Read equipment dimensions, roles and deployment constraints.",
  "audio": {
    "script_file": "audio/module3/slide_01_inside_the_rack.txt",
    "wav_file": "audio/module3/slide_01_inside_the_rack.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 1
    }
  ]
}
```

### Active spoken narration
Module three: Inside the Rack. A rack organizes equipment into a practical physical system. You'll use its dimensions to interpret a layout, distinguish equipment roles and recognize the constraints that remain even when there are empty mounting positions.


## M3S2: Read a Rack Layout and Its Constraints
Type: objectives

### Authored slide fields
```json
{
  "id": 2,
  "type": "objectives",
  "slug": "read_rack_layout",
  "title": "Read a Rack Layout and Its Constraints",
  "objectives": [
    "Interpret nominal rack width and vertical rack units.",
    "Recognize compute, storage and shared-chassis roles.",
    "Check power, cooling, cabling and service constraints.",
    "Distinguish conventional racks from Open Rack terminology."
  ],
  "audio": {
    "script_file": "audio/module3/slide_02_read_rack_layout.txt",
    "wav_file": "audio/module3/slide_02_read_rack_layout.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 1
    }
  ]
}
```

### Active spoken narration
By the end of this module, you'll be able to distinguish rack width from vertical rack units, recognize common compute and storage arrangements, and explain why power, cooling, cabling and access shape a layout.

You'll also see how Open Rack uses a different mechanical system. This is an introduction to the vocabulary; the Intro to OCP courses provide the deeper architecture and community context.


## M3S3: Rack Equipment Overview
Type: content_diagram

### Authored slide fields
```json
{
  "id": 3,
  "type": "content_diagram",
  "slug": "data_center_101_3_1_rack_equipment_overview_1080p",
  "title": "Rack Equipment Overview",
  "section_label": "Explanatory Video",
  "media_focus": true,
  "figure": {
    "path": "resources/videos/module3/data-center-101-3-1-rack-equipment-overview-1080p.mp4",
    "poster": "resources/images/module3/video-slide-3-poster.jpg",
    "media_type": "video",
    "role": "original_video",
    "source": "reuse",
    "autoplay": false,
    "loop": false,
    "muted": false,
    "controls": true,
    "alt": "Rack Equipment Overview video.",
    "caption": "19 in is the nominal equipment front-panel width. 1U = 44.45 mm (1.75 in). Mounting-hole spacing and cabinet dimensions are separate measurements; U measures space, not performance.",
    "source_sha256": "91dbe7935c1ffc1572db587265662d6e5e29d691b2d69beffb69d64565f98f82",
    "captions": [
      {
        "path": "resources/captions/module3/data-center-101-3-1-rack-equipment-overview-1080p.vtt",
        "language": "en",
        "label": "English (transcribed)"
      }
    ],
    "caption_cues": [
      {
        "start": 3.48,
        "end": 6.76,
        "text": "When we talk about data centers, the\nserver rack is where it all begins."
      },
      {
        "start": 7.5,
        "end": 11.02,
        "text": "In the same way that a standardized\nshipping container is a standard form"
      },
      {
        "start": 11.12,
        "end": 15.06,
        "text": "factor for everything we ship in the real\nworld, a server rack is a"
      },
      {
        "start": 15.1,
        "end": 18.56,
        "text": "purpose-built standard form factor for IT\nequipment."
      },
      {
        "start": 19.58,
        "end": 23.34,
        "text": "The most common size is a 19-inch rack.\nThe 19-inch"
      },
      {
        "start": 23.46,
        "end": 27.2,
        "text": "rack format has been around for decades,\nand it remains essential"
      },
      {
        "start": 27.66,
        "end": 30.96,
        "text": "in today's IT infrastructure. The term\n19-inch"
      },
      {
        "start": 31.36,
        "end": 35.1,
        "text": "refers to the horizontal width of the\nrack, specifically the"
      },
      {
        "start": 35.14,
        "end": 38.7,
        "text": "distance between the mounting rails. This\nis the"
      },
      {
        "start": 38.82,
        "end": 42.76,
        "text": "standard form factor for rack-mountable IT\nequipment. This"
      },
      {
        "start": 42.84,
        "end": 45.86,
        "text": "standard measurements of 19 inch, which is\nabout"
      },
      {
        "start": 46.04,
        "end": 50.02,
        "text": "48.2 centimeters, makes it possible to\nmount"
      },
      {
        "start": 50.12,
        "end": 54.08,
        "text": "a wide variety of servers, switches, patch\npanels, and other"
      },
      {
        "start": 54.16,
        "end": 57.4,
        "text": "IT equipment, even from different\nmanufacturers,"
      },
      {
        "start": 58.04,
        "end": 61.56,
        "text": "all in the same rack. While the width is\nstandard,"
      },
      {
        "start": 62.3,
        "end": 66.02,
        "text": "it's worth noting that the rack depth can\nvary on the equipment"
      },
      {
        "start": 66.38,
        "end": 70.14,
        "text": "and use case. Data centers typically use\ndeeper racks to support"
      },
      {
        "start": 70.2,
        "end": 74.02,
        "text": "higher performance or dense compute gear,\nwhile shallower depths"
      },
      {
        "start": 74.2,
        "end": 78.16,
        "text": "might be found in edge or telco\nenvironments. But"
      },
      {
        "start": 78.24,
        "end": 82.22,
        "text": "racks don't just help with physical space.\nThey're an essential part of"
      },
      {
        "start": 82.94,
        "end": 86.78,
        "text": "organization of equipment, maintenance,\nairflow"
      },
      {
        "start": 86.92,
        "end": 90.8,
        "text": "management, and security. By vertically\nstacking"
      },
      {
        "start": 90.9,
        "end": 94.72,
        "text": "equipment in a rack, it helps you save\nspace and keep things"
      },
      {
        "start": 94.82,
        "end": 98.78,
        "text": "manageable. A key measurement you'll often\nhear is a rack"
      },
      {
        "start": 98.88,
        "end": 102.76,
        "text": "unit or simply a U. One rack unit is"
      },
      {
        "start": 102.92,
        "end": 106.46,
        "text": "1.75 inches or approximately 44.45"
      },
      {
        "start": 106.52,
        "end": 109.96,
        "text": "centimeters in height. Most standard racks\nare"
      },
      {
        "start": 110.18,
        "end": 113.72,
        "text": "42U tall, meaning they can hold equipment"
      },
      {
        "start": 114.14,
        "end": 117.76,
        "text": "that adds up to about 73.5"
      },
      {
        "start": 117.82,
        "end": 121.68,
        "text": "inches or roughly 1.87 meters in total\nheight."
      },
      {
        "start": 122.48,
        "end": 126.46,
        "text": "IT equipment is typically labeled by its U\nheight,"
      },
      {
        "start": 127.26,
        "end": 130.639,
        "text": "like a 1U server or a 2U"
      },
      {
        "start": 131.0,
        "end": 134.78,
        "text": "switch. But in the industry, we don't talk\nabout the physical height in"
      },
      {
        "start": 134.84,
        "end": 137.92,
        "text": "inches or meters unless we are shipping\nthe equipment."
      },
      {
        "start": 138.66,
        "end": 142.66,
        "text": "Typically, we label the equipment and\nracks by their U height. The"
      },
      {
        "start": 142.74,
        "end": 146.56,
        "text": "larger the U size, the more capability or\nfunction the"
      },
      {
        "start": 146.62,
        "end": 150.18,
        "text": "equipment tends to have, but it also takes\nup more rack space."
      },
      {
        "start": 150.98,
        "end": 154.82,
        "text": "Racks are designed to allow for good\nairflow and front and rear"
      },
      {
        "start": 154.92,
        "end": 158.48,
        "text": "access to all components. This makes"
      },
      {
        "start": 158.56,
        "end": 162.52,
        "text": "maintenance easier and supports good cable\nmanagement. Neatly"
      },
      {
        "start": 162.58,
        "end": 166.48,
        "text": "routed cables not only look better, they\nreduce the risk of error"
      },
      {
        "start": 166.54,
        "end": 169.98,
        "text": "and make the airflow more efficient.\nSpeaking of airflow,"
      },
      {
        "start": 170.78,
        "end": 174.54,
        "text": "cooling is built into the design.\nEquipment sucks"
      },
      {
        "start": 174.62,
        "end": 178.36,
        "text": "cool air from the front and pushes warm\nair out the back."
      },
      {
        "start": 179.1,
        "end": 182.88,
        "text": "That's why racks are often arranged in hot\nand cold aisles."
      },
      {
        "start": 183.66,
        "end": 187.44,
        "text": "This separation allows facilities to\nbetter manage temperature and"
      },
      {
        "start": 187.52,
        "end": 191.5,
        "text": "energy usage. Mounting equipment is done\nusing rails along"
      },
      {
        "start": 191.54,
        "end": 195.38,
        "text": "the sides of the rack. These rails have\nholes spaced at standard"
      },
      {
        "start": 195.46,
        "end": 199.26,
        "text": "intervals, so equipment can be locked in\nwith screws or quick-release"
      },
      {
        "start": 199.32,
        "end": 203.0,
        "text": "tabs. This keeps everything secure and\naligned properly."
      },
      {
        "start": 203.96,
        "end": 207.28,
        "text": "So why does standardization matter? Well,"
      },
      {
        "start": 208.04,
        "end": 211.72,
        "text": "because it makes it easy to scale. Need to\nadd another"
      },
      {
        "start": 211.78,
        "end": 215.3,
        "text": "server? You know exactly how much rack\nspace you have left"
      },
      {
        "start": 215.78,
        "end": 219.76,
        "text": "and what size fits. That consistency\nsupports"
      },
      {
        "start": 219.8,
        "end": 223.02,
        "text": "both operations and future growth. Now,"
      },
      {
        "start": 223.46,
        "end": 227.32,
        "text": "racks can also have doors, front and rear,\nthat are perforated to"
      },
      {
        "start": 227.38,
        "end": 230.58,
        "text": "allow for airflow, but they also provide\nsecurity."
      },
      {
        "start": 231.54,
        "end": 235.04,
        "text": "In summary, a 19-inch rack may seem\nsimple,"
      },
      {
        "start": 235.46,
        "end": 239.26,
        "text": "but it plays a crucial role in the data\ncenter. It's the"
      },
      {
        "start": 239.54,
        "end": 242.58,
        "text": "standardized form factor, and it's the\nbackbone"
      },
      {
        "start": 243.5,
        "end": 247.26,
        "text": "of building blocks in the data center. It\nensures"
      },
      {
        "start": 247.3,
        "end": 250.84,
        "text": "compatibility, it enables organization, it"
      },
      {
        "start": 250.9,
        "end": 254.68,
        "text": "improves cooling, and it supports\nsecurity, all while"
      },
      {
        "start": 254.72,
        "end": 257.079,
        "text": "helping scale operations efficiently."
      }
    ],
    "assets": [
      "resources/captions/module3/data-center-101-3-1-rack-equipment-overview-1080p.vtt"
    ],
    "text_inventory": {
      "sha256": "91dbe7935c1ffc1572db587265662d6e5e29d691b2d69beffb69d64565f98f82",
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
          "text": "A SERVER RACK IS A",
          "at_seconds": 17.5
        },
        {
          "text": "PURPOSE-BUILT STANDARD",
          "at_seconds": 17.5
        },
        {
          "text": "FORM FACTOR FOR IT EQUIPMENT",
          "at_seconds": 17.5
        },
        {
          "text": "THE MOST COMMON SIZE IS THE 19-INCH RACK",
          "at_seconds": 22.5
        },
        {
          "text": "HAS BEEN AROUND FOR DECADES AND REMAINS",
          "at_seconds": 27.5
        },
        {
          "text": "ESSENTIAL",
          "at_seconds": 27.5
        },
        {
          "text": "THE HORIZONTAL WIDTH OF T",
          "at_seconds": 32.5
        },
        {
          "text": "19-INCH",
          "at_seconds": 32.5
        },
        {
          "text": "19-IN",
          "at_seconds": 37.5
        },
        {
          "text": "THE HORIZONTAL W",
          "at_seconds": 37.5
        },
        {
          "text": "SPECIFICALLY,THE C",
          "at_seconds": 37.5
        },
        {
          "text": "THE MOUNT",
          "at_seconds": 37.5
        },
        {
          "text": "19 INCHES IS THE STANDARD",
          "at_seconds": 42.5
        },
        {
          "text": "FOR MOUNTING IT EQUIPMENT",
          "at_seconds": 42.5
        },
        {
          "text": "• 19 INCHES",
          "at_seconds": 42.5
        },
        {
          "text": "48.26 СM",
          "at_seconds": 47.5
        },
        {
          "text": "-bba",
          "at_seconds": 52.5
        },
        {
          "text": "8888",
          "at_seconds": 57.5
        },
        {
          "text": "600 MM",
          "at_seconds": 62.5
        },
        {
          "text": "1200 MM",
          "at_seconds": 62.5
        },
        {
          "text": "RACK DEPTH C",
          "at_seconds": 67.5
        },
        {
          "text": "DATA CENTERS TYPICALLY",
          "at_seconds": 72.5
        },
        {
          "text": "USE DEEPER RACKS",
          "at_seconds": 72.5
        },
        {
          "text": "THEY'RE AN ESSENTIAL PART OF",
          "at_seconds": 82.5
        },
        {
          "text": "ORGANIZATION",
          "at_seconds": 87.5
        },
        {
          "text": "MAINTENANCE",
          "at_seconds": 87.5
        },
        {
          "text": "AIRFLOW MANAGEMENT",
          "at_seconds": 87.5
        },
        {
          "text": "RACKS HELP YOU SAVE SPACE",
          "at_seconds": 92.5
        },
        {
          "text": "1.75 INCHES",
          "at_seconds": 107.5
        },
        {
          "text": "OR 44.45MM",
          "at_seconds": 107.5
        },
        {
          "text": "•000",
          "at_seconds": 112.5
        },
        {
          "text": "L",
          "at_seconds": 112.5
        },
        {
          "text": "LUI",
          "at_seconds": 117.5
        },
        {
          "text": "LL",
          "at_seconds": 117.5
        },
        {
          "text": "-",
          "at_seconds": 117.5
        },
        {
          "text": "73.5 INCHES",
          "at_seconds": 117.5
        },
        {
          "text": "EQUI",
          "at_seconds": 122.5
        },
        {
          "text": "EQUIPMENT IS TYPICALLY LABELED BY ITS U HEIGHT",
          "at_seconds": 127.5
        },
        {
          "text": "1U",
          "at_seconds": 127.5
        },
        {
          "text": "2U",
          "at_seconds": 127.5
        },
        {
          "text": "4U",
          "at_seconds": 127.5
        },
        {
          "text": "10",
          "at_seconds": 132.5
        },
        {
          "text": "THE",
          "at_seconds": 142.5
        },
        {
          "text": "THE LARGER THE U SIZE,",
          "at_seconds": 147.5
        },
        {
          "text": "THE MORE CAPABILITY OR FUNCTION",
          "at_seconds": 147.5
        },
        {
          "text": "THE EQUIPMENT TENDS TO HAVE",
          "at_seconds": 147.5
        },
        {
          "text": "RACKS ARE DESIGNED TO ALLOW FOR GOOD AIRFLOW",
          "at_seconds": 152.5
        },
        {
          "text": "THEY REDUCE THE RISK OF ERROR",
          "at_seconds": 167.5
        },
        {
          "text": "AND MAKE AIRFLOW MORE EFFICIENT",
          "at_seconds": 167.5
        },
        {
          "text": "HOT AISLE",
          "at_seconds": 182.5
        },
        {
          "text": "COLD AISLE",
          "at_seconds": 182.5
        },
        {
          "text": "FEEEA",
          "at_seconds": 187.5
        },
        {
          "text": "THHHHA",
          "at_seconds": 187.5
        },
        {
          "text": "RAILS",
          "at_seconds": 192.5
        },
        {
          "text": "THESE RAILS HAVE HOLES SPACED",
          "at_seconds": 197.5
        },
        {
          "text": "AT STANDARDIZED INTERVALS,",
          "at_seconds": 197.5
        },
        {
          "text": "SO EQUIPMENT CAN BE LOCKED IN",
          "at_seconds": 197.5
        },
        {
          "text": "WHY DOES STANDARDIZATION MATTER?",
          "at_seconds": 207.5
        },
        {
          "text": "NEED TO ADD ANOTHER",
          "at_seconds": 212.5
        },
        {
          "text": "PERFORATED DOORS",
          "at_seconds": 227.5
        },
        {
          "text": "0000|",
          "at_seconds": 232.5
        },
        {
          "text": "0000",
          "at_seconds": 232.5
        },
        {
          "text": "100",
          "at_seconds": 232.5
        },
        {
          "text": "000",
          "at_seconds": 232.5
        },
        {
          "text": "IT PLAYS A CRITICAL ROLE IN THE BACKBONE",
          "at_seconds": 237.5
        },
        {
          "text": "OF DATA CENTER INFRASTRUCTURE",
          "at_seconds": 237.5
        },
        {
          "text": "• ENSURES COMPATIBILITY",
          "at_seconds": 247.5
        },
        {
          "text": "• ENABLES ORGANIZATION",
          "at_seconds": 252.5
        },
        {
          "text": "• IMPROVES COOLING",
          "at_seconds": 252.5
        },
        {
          "text": "• SUPPORTS SEC",
          "at_seconds": 252.5
        },
        {
          "text": "• IINRHOVES COOLING",
          "at_seconds": 257.5
        },
        {
          "text": "• SUPPORTS SECURITY",
          "at_seconds": 257.5
        },
        {
          "text": "• HELPING SCALE OPERATIONS",
          "at_seconds": 257.5
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    },
    "source_poster": "resources/images/module3/data-center-101-3-1-rack-equipment-overview-1080p.jpg"
  },
  "audio": null,
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ],
  "video_transcript": "When we talk about data centers, the server rack is where it all begins. In the same way that a standardized shipping container is a standard form factor for everything we ship in the real world, a server rack is a purpose-built standard form factor for IT equipment. The most common size is a 19-inch rack. The 19-inch rack format has been around for decades, and it remains essential in today's IT infrastructure. The term 19-inch refers to the horizontal width of the rack, specifically the distance between the mounting rails. This is the standard form factor for rack-mountable IT equipment. This standard measurements of 19 inch, which is about 48.2 centimeters, makes it possible to mount a wide variety of servers, switches, patch panels, and other IT equipment, even from different manufacturers, all in the same rack. While the width is standard, it's worth noting that the rack depth can vary on the equipment and use case. Data centers typically use deeper racks to support higher performance or dense compute gear, while shallower depths might be found in edge or telco environments. But racks don't just help with physical space. They're an essential part of organization of equipment, maintenance, airflow management, and security. By vertically stacking equipment in a rack, it helps you save space and keep things manageable. A key measurement you'll often hear is a rack unit or simply a U. One rack unit is 1.75 inches or approximately 44.45 centimeters in height. Most standard racks are 42U tall, meaning they can hold equipment that adds up to about 73.5 inches or roughly 1.87 meters in total height. IT equipment is typically labeled by its U height, like a 1U server or a 2U switch. But in the industry, we don't talk about the physical height in inches or meters unless we are shipping the equipment. Typically, we label the equipment and racks by their U height. The larger the U size, the more capability or function the equipment tends to have, but it also takes up more rack space. Racks are designed to allow for good airflow and front and rear access to all components. This makes maintenance easier and supports good cable management. Neatly routed cables not only look better, they reduce the risk of error and make the airflow more efficient. Speaking of airflow, cooling is built into the design. Equipment sucks cool air from the front and pushes warm air out the back. That's why racks are often arranged in hot and cold aisles. This separation allows facilities to better manage temperature and energy usage. Mounting equipment is done using rails along the sides of the rack. These rails have holes spaced at standard intervals, so equipment can be locked in with screws or quick-release tabs. This keeps everything secure and aligned properly. So why does standardization matter? Well, because it makes it easy to scale. Need to add another server? You know exactly how much rack space you have left and what size fits. That consistency supports both operations and future growth. Now, racks can also have doors, front and rear, that are perforated to allow for airflow, but they also provide security. In summary, a 19-inch rack may seem simple, but it plays a crucial role in the data center. It's the standardized form factor, and it's the backbone of building blocks in the data center. It ensures compatibility, it enables organization, it improves cooling, and it supports security, all while helping scale operations efficiently. ",
  "term_refs": [
    "energy",
    "edge_data_center",
    "rack_unit",
    "container"
  ],
  "narration_enabled": false,
  "transcript": "When we talk about data centers, the server rack is where it all begins. In the same way that a standardized shipping container is a standard form factor for everything we ship in the real world, a server rack is a purpose-built standard form factor for IT equipment. The most common size is a 19-inch rack. The 19-inch rack format has been around for decades, and it remains essential in today's IT infrastructure. The term 19-inch refers to the horizontal width of the rack, specifically the distance between the mounting rails. This is the standard form factor for rack-mountable IT equipment. This standard measurements of 19 inch, which is about 48.2 centimeters, makes it possible to mount a wide variety of servers, switches, patch panels, and other IT equipment, even from different manufacturers, all in the same rack. While the width is standard, it's worth noting that the rack depth can vary on the equipment and use case. Data centers typically use deeper racks to support higher performance or dense compute gear, while shallower depths might be found in edge or telco environments. But racks don't just help with physical space. They're an essential part of organization of equipment, maintenance, airflow management, and security. By vertically stacking equipment in a rack, it helps you save space and keep things manageable. A key measurement you'll often hear is a rack unit or simply a U. One rack unit is 1.75 inches or approximately 44.45 centimeters in height. Most standard racks are 42U tall, meaning they can hold equipment that adds up to about 73.5 inches or roughly 1.87 meters in total height. IT equipment is typically labeled by its U height, like a 1U server or a 2U switch. But in the industry, we don't talk about the physical height in inches or meters unless we are shipping the equipment. Typically, we label the equipment and racks by their U height. The larger the U size, the more capability or function the equipment tends to have, but it also takes up more rack space. Racks are designed to allow for good airflow and front and rear access to all components. This makes maintenance easier and supports good cable management. Neatly routed cables not only look better, they reduce the risk of error and make the airflow more efficient. Speaking of airflow, cooling is built into the design. Equipment sucks cool air from the front and pushes warm air out the back. That's why racks are often arranged in hot and cold aisles. This separation allows facilities to better manage temperature and energy usage. Mounting equipment is done using rails along the sides of the rack. These rails have holes spaced at standard intervals, so equipment can be locked in with screws or quick-release tabs. This keeps everything secure and aligned properly. So why does standardization matter? Well, because it makes it easy to scale. Need to add another server? You know exactly how much rack space you have left and what size fits. That consistency supports both operations and future growth. Now, racks can also have doors, front and rear, that are perforated to allow for airflow, but they also provide security. In summary, a 19-inch rack may seem simple, but it plays a crucial role in the data center. It's the standardized form factor, and it's the backbone of building blocks in the data center. It ensures compatibility, it enables organization, it improves cooling, and it supports security, all while helping scale operations efficiently. "
}
```

### Active spoken narration
None; imported recording owns the audio. Its transcript and caption cues are in the slide fields.

## M3S4: What the 19-Inch Dimension Measures
Type: content_diagram

### Authored slide fields
```json
{
  "id": 4,
  "type": "content_diagram",
  "slug": "rack_width",
  "title": "What the 19-Inch Dimension Measures",
  "section_label": "Mechanical Dimensions",
  "figure": {
    "path": "figures/module3/rack-width.svg",
    "source": "custom",
    "alt": "Nominal panel width, mounting-hole spacing and cabinet dimensions are distinct.",
    "caption": "Nominal panel width, mounting-hole spacing and cabinet dimensions are distinct.",
    "design": {
      "layout": "rack_width",
      "nodes": []
    },
    "text_inventory": {
      "sha256": "bb0dabcda24a6f6c64e4a816549343b07fd088a7e1e39c240e024a9c0dbd7394",
      "entries": [
        {
          "text": "Nominal panel width: 19 in (482.6 mm)"
        },
        {
          "text": "Hole centers: about 18.312 in (465.1 mm)"
        },
        {
          "text": "Cabinet outside width and usable depth are separate dimensions"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "19-inch front-panel example",
      "url": "https://www.metcaseusa.com/en/19-Front-Panels/M6019010.htm"
    },
    {
      "label": "Mounting-hole spacing",
      "url": "https://www.cyberpowersystems.com/faqs/what-is-the-standard-rack-horizontal-hole-spacing/"
    }
  ],
  "source_correction": "The source keyed answer incorrectly equated nineteen inches with spacing between mounting rails.",
  "audio": {
    "script_file": "audio/module3/slide_04_rack_width.txt",
    "wav_file": "audio/module3/slide_04_rack_width.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ]
}
```

### Active spoken narration
In the conventional nineteen-inch system, the nominal dimension describes the equipment front-panel width, including its mounting ears. It doesn't describe the cabinet's outside width, its depth or the distance between the centers of its mounting holes.

Those are different dimensions. The common horizontal hole-center spacing is about eighteen point three one two inches. When checking fit, use the equipment and rack drawings rather than treating every measurement as nineteen inches.


### Visible static figure text
Nominal panel width: 19 in (482.6 mm)
Hole centers: about 18.312 in (465.1 mm)
Cabinet outside width and usable depth are separate dimensions

## M3S5: Rack Units Measure Vertical Allocation
Type: content_diagram

### Authored slide fields
```json
{
  "id": 5,
  "type": "content_diagram",
  "slug": "rack_units",
  "title": "Rack Units Measure Vertical Allocation",
  "section_label": "Vertical Allocation",
  "figure": {
    "path": "figures/module3/rack-units.svg",
    "source": "custom",
    "alt": "1U, 2U and 4U are vertical allocations, not workload or performance categories.",
    "caption": "1U, 2U and 4U are vertical allocations, not workload or performance categories.",
    "design": {
      "layout": "rack_units",
      "nodes": []
    },
    "text_inventory": {
      "sha256": "1fa91e1333ecc207d20e3de1af5cce73fd6c6e595df0aff580bc3841b9c3b757",
      "entries": [
        {
          "text": "1U = 44.45 mm"
        },
        {
          "text": "2U = 88.90 mm"
        },
        {
          "text": "4U = 177.80 mm"
        },
        {
          "text": "Nominal vertical allocation; manufactured panels include clearance"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "Rack dimensional guidance",
      "url": "https://www.canford.co.uk/TechZone/Article/19InchRackDimensions"
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_05_rack_units.txt",
    "wav_file": "audio/module3/slide_05_rack_units.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ],
  "term_refs": [
    "power"
  ]
}
```

### Active spoken narration
A rack unit, written U, describes vertical allocation. One U has a pitch of one point seven five inches, or forty-four point four five millimeters. Two U and four U reserve two and four times that vertical pitch.

Actual front panels include clearance, so their manufactured height is slightly smaller than the nominal allocation. The unit tells you how much vertical space is reserved. It doesn't tell you the equipment's compute performance, drive count, power demand or workload.


### Visible static figure text
1U = 44.45 mm
2U = 88.90 mm
4U = 177.80 mm
Nominal vertical allocation; manufactured panels include clearance

## M3S6: Compute Comes in Many Chassis
Type: content_grid

### Authored slide fields
```json
{
  "id": 6,
  "type": "content_grid",
  "slug": "compute_chassis",
  "title": "Compute Comes in Many Chassis",
  "section_label": "Compute Roles",
  "grid_cols": 2,
  "cards": [
    {
      "title": "Compact compute",
      "body": "A 1U example for a compact server."
    },
    {
      "title": "Dual-node chassis",
      "body": "A 2U example with two independent nodes."
    },
    {
      "title": "Multi-node platform",
      "body": "A 4U example with shared chassis infrastructure."
    },
    {
      "title": "General-purpose or GPU system",
      "body": "Configuration and power/cooling needs vary by design."
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_06_compute_chassis.txt",
    "wav_file": "audio/module3/slide_06_compute_chassis.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 3
    }
  ],
  "term_refs": [
    "gpu"
  ]
}
```

### Active spoken narration
A compact server may use one U, while other designs place multiple independent nodes in a shared chassis. General-purpose and accelerator systems can reserve more space for processors, memory, devices, airflow or liquid-cooling connections.

The illustrated one U, two U and four U arrangements are examples. A two-node chassis doesn't automatically deliver twice the useful performance of another system. Workload behavior and the actual processor, memory, storage and interface configuration determine what the equipment can accomplish.


## M3S7: Storage Designs Balance Access and Capacity
Type: content_diagram

### Authored slide fields
```json
{
  "id": 7,
  "type": "content_diagram",
  "slug": "storage_roles",
  "title": "Storage Designs Balance Access and Capacity",
  "section_label": "Storage Roles",
  "figure": {
    "path": "figures/module3/storage-roles.svg",
    "source": "custom",
    "alt": "Storage form factors serve different capacity, access and service needs.",
    "caption": "Storage form factors serve different capacity, access and service needs.",
    "design": {
      "layout": "grid",
      "nodes": [],
      "items": [
        [
          "NVMe enclosure",
          "High-speed access to compatible solid-state storage"
        ],
        [
          "Capacity-focused server",
          "Many drive positions for large datasets"
        ],
        [
          "High-bay enclosure",
          "A 4U-plus example with many bays"
        ],
        [
          "Selection criteria",
          "Capacity, performance, protection and service access"
        ]
      ]
    },
    "text_inventory": {
      "sha256": "c8e819b74b58f80ac3028a4966b58f282923820af1b08b8eefeb2781d7b81ec7",
      "entries": [
        {
          "text": "NVMe enclosure"
        },
        {
          "text": "High-speed access to compatible solid-state storage"
        },
        {
          "text": "Capacity-focused server"
        },
        {
          "text": "Many drive positions for large datasets"
        },
        {
          "text": "High-bay enclosure"
        },
        {
          "text": "A 4U-plus example with many bays"
        },
        {
          "text": "Selection criteria"
        },
        {
          "text": "Capacity, performance, protection and service access"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module3/slide_07_storage_roles.txt",
    "wav_file": "audio/module3/slide_07_storage_roles.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 3
    }
  ],
  "term_refs": [
    "nvme",
    "virtual_machine"
  ]
}
```

### Active spoken narration
Storage equipment is organized around the information it must hold and how it must be accessed. N V M E, short for Non-Volatile Memory Express, defines how host software communicates with non-volatile memory. Compatible enclosures support fast access to solid-state storage. Capacity-focused servers can provide many drive positions for large datasets, backup or archives.

The illustrated layout includes a high-bay enclosure of four U or more. That is one design example, not a rule for every storage system. Compare capacity, access performance, interfaces, protection and service needs rather than choosing by height alone.


### Visible static figure text
NVMe enclosure
High-speed access to compatible  solid-state storage
Capacity-focused server
Many drive positions for large  datasets
High-bay enclosure
A 4U-plus example with many bays
Selection criteria
Capacity, performance,  protection and service access

## M3S8: Shared Chassis and Utility Nodes Have Distinct Roles
Type: content_two_column

### Authored slide fields
```json
{
  "id": 8,
  "type": "content_two_column",
  "slug": "shared_and_utility_nodes",
  "title": "Shared Chassis and Utility Nodes Have Distinct Roles",
  "section_label": "Shared Infrastructure",
  "bullets": [
    {
      "text": "Blade systems group compute modules within a chassis."
    },
    {
      "text": "Shared infrastructure affects failure and service boundaries."
    },
    {
      "text": "Utility and management nodes are defined by function."
    }
  ],
  "figure": {
    "path": "figures/module3/shared-chassis.svg",
    "source": "custom",
    "alt": "Compute modules and management roles have different dependencies.",
    "caption": "Compute modules and management roles have different dependencies.",
    "design": {
      "layout": "layers",
      "nodes": [
        "Compute modules or utility services",
        "Chassis and management dependencies",
        "Rack power, cooling and connections"
      ]
    },
    "text_inventory": {
      "sha256": "b8910d87c7b8eb1e135fa3a6e3aceb73e4c7bec42ac7e6d3e837d9f3f76a2c84",
      "entries": [
        {
          "text": "Compute modules or utility services"
        },
        {
          "text": "Chassis and management dependencies"
        },
        {
          "text": "Rack power, cooling and connections"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module3/slide_08_shared_and_utility_nodes.txt",
    "wav_file": "audio/module3/slide_08_shared_and_utility_nodes.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 3
    }
  ]
}
```

### Active spoken narration
A blade system groups replaceable compute modules within a shared chassis. Power, cooling or other supporting functions may be shared, depending on the product. That arrangement affects both density and the consequences of a shared-component problem.

A utility or management node is identified by its role: monitoring, backup coordination or another service. Its physical appearance alone doesn't establish what it controls. Read the system function and its dependencies alongside the rack position.


### Visible static figure text
Compute modules or utility services
Chassis and management dependencies
Rack power, cooling and connections

## M3S9: Equipment Choice Consumes Several Budgets
Type: content_diagram

### Authored slide fields
```json
{
  "id": 9,
  "type": "content_diagram",
  "slug": "rack_budgets",
  "title": "Equipment Choice Consumes Several Budgets",
  "section_label": "Capacity in Motion",
  "figure": {
    "path": "figures/module3/rack-budgets.mp4",
    "poster": "figures/module3/rack-budgets-poster.png",
    "media_type": "video",
    "source": "custom",
    "autoplay": false,
    "loop": false,
    "muted": true,
    "alt": "An illustrative cooling limit is reached while rack space remains available.",
    "caption": "An illustrative cooling limit is reached while rack space remains available.",
    "text_inventory": {
      "sha256": "1bb6652826fe897c71b127cb94d6553834bcffdfb77b25af2e883ccf45739b27",
      "entries": [
        {
          "text": "Illustrative used share of independent allocations",
          "at_seconds": 0
        },
        {
          "text": "Rack positions",
          "at_seconds": 0
        },
        {
          "text": "Space remains",
          "at_seconds": 0
        },
        {
          "text": "Space used",
          "at_seconds": 0
        },
        {
          "text": "100%",
          "at_seconds": 0
        },
        {
          "text": "Power used",
          "at_seconds": 0
        },
        {
          "text": "Cooling used",
          "at_seconds": 0
        },
        {
          "text": "Network traffic also changes",
          "at_seconds": 0
        },
        {
          "text": "Next device: review",
          "at_seconds": 18.84
        },
        {
          "text": "Cooling allocation full · review before adding",
          "at_seconds": 18.84
        },
        {
          "text": "25%",
          "at_seconds": 0
        },
        {
          "text": "38%",
          "at_seconds": 0
        },
        {
          "text": "50%",
          "at_seconds": 0
        },
        {
          "text": "30%",
          "at_seconds": 0
        },
        {
          "text": "55%",
          "at_seconds": 0
        },
        {
          "text": "82%",
          "at_seconds": 0
        },
        {
          "text": "35%",
          "at_seconds": 0
        },
        {
          "text": "65%",
          "at_seconds": 0
        }
      ],
      "reviewed_on": "2026-10-24",
      "review_method": "Astra review of native-resolution causal scenes, measured final-v4 narration timestamps and decoded video states; root geometry and synchronized-player checks. Timing uses Scribe v2 word estimates, not perceptual listening approval."
    },
    "sync_to_narration": true,
    "animation_source": "animations/module3/rack-budgets.html"
  },
  "audio": {
    "script_file": "audio/module3/slide_09_rack_budgets.txt",
    "wav_file": "audio/module3/slide_09_rack_budgets.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 3
    }
  ]
}
```

### Active spoken narration
Adding equipment changes more than the number of empty rack positions. It can increase electrical demand, heat-removal requirements and network traffic at different rates.

In this illustrative animation, the cooling allocation reaches its limit while mounting space remains available. The values explain a relationship, not a recommended rack design. The practical lesson is to identify the limiting budget before deciding that another device can be installed.


## M3S10: Cables and Airflow Need Their Own Space
Type: content_diagram

### Authored slide fields
```json
{
  "id": 10,
  "type": "content_diagram",
  "slug": "cables_and_airflow",
  "title": "Cables and Airflow Need Their Own Space",
  "section_label": "Operational Layout",
  "figure": {
    "path": "figures/module3/rack-access.svg",
    "source": "custom",
    "alt": "The equipment layout must leave appropriate intake, exhaust, cable and service space.",
    "caption": "The equipment layout must leave appropriate intake, exhaust, cable and service space.",
    "design": {
      "layout": "grid",
      "nodes": [],
      "items": [
        [
          "Intake side",
          "Maintain the required air or liquid connections"
        ],
        [
          "Exhaust side",
          "Preserve the intended heat-removal path"
        ],
        [
          "Cable space",
          "Respect routing and connection requirements"
        ],
        [
          "Service access",
          "Allow the required maintenance movements"
        ]
      ]
    },
    "text_inventory": {
      "sha256": "be1bd145d4ebe4778299ff4799a266ff1db804ee5d4c649e3ccc30496a7f0c12",
      "entries": [
        {
          "text": "Intake side"
        },
        {
          "text": "Maintain the required air or liquid connections"
        },
        {
          "text": "Exhaust side"
        },
        {
          "text": "Preserve the intended heat- removal path"
        },
        {
          "text": "Cable space"
        },
        {
          "text": "Respect routing and connection requirements"
        },
        {
          "text": "Service access"
        },
        {
          "text": "Allow the required maintenance movements"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "audio": {
    "script_file": "audio/module3/slide_10_cables_and_airflow.txt",
    "wav_file": "audio/module3/slide_10_cables_and_airflow.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ]
}
```

### Active spoken narration
A layout must support the equipment's intake and exhaust directions and leave room for the cables and connections it needs. Crowded cabling can obstruct airflow or make a component difficult to reach.

Service access also matters when equipment moves on rails or a connection must be replaced. Follow the equipment's physical requirements rather than assuming every device has the same front-to-rear arrangement. A tidy-looking layout still needs to work during maintenance.


### Visible static figure text
Intake side
Maintain the required air or  liquid connections
Exhaust side
Preserve the intended heat-  removal path
Cable space
Respect routing and connection  requirements
Service access
Allow the required maintenance  movements

## M3S11: Physical Security Supports Serviceability
Type: content_grid

### Authored slide fields
```json
{
  "id": 11,
  "type": "content_grid",
  "slug": "physical_security",
  "title": "Physical Security Supports Serviceability",
  "section_label": "Authorized Access",
  "grid_cols": 2,
  "cards": [
    {
      "title": "Access control",
      "body": "Define who may reach the area and equipment."
    },
    {
      "title": "Tenant separation",
      "body": "Respect contracted boundaries in shared facilities."
    },
    {
      "title": "Asset identification",
      "body": "Know which device and connection is being serviced."
    },
    {
      "title": "Service procedures",
      "body": "Authorize and record legitimate maintenance."
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_11_physical_security.txt",
    "wav_file": "audio/module3/slide_11_physical_security.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ]
}
```

### Active spoken narration
Racks can help control access to equipment, especially where several customers share a facility. Doors, access permissions, asset identification and service procedures work together to support that control.

A locked rack doesn't replace system security, monitoring or authorization for changes. People still need a safe, traceable way to perform legitimate work. Consider who can enter the area, reach each device and connect to its management interfaces, and how their work is recorded.


## M3S12: Open Rack Is a Different Mechanical System
Type: content_diagram

### Authored slide fields
```json
{
  "id": 12,
  "type": "content_diagram",
  "slug": "open_rack_orientation",
  "title": "Open Rack Is a Different Mechanical System",
  "section_label": "OCP Orientation",
  "figure": {
    "path": "figures/module3/rack-systems.svg",
    "source": "custom",
    "alt": "Conventional U and Open Unit belong to different mechanical systems.",
    "caption": "Conventional U and Open Unit belong to different mechanical systems.",
    "design": {
      "layout": "grid",
      "nodes": [],
      "items": [
        [
          "Conventional rack",
          "Nominal 19-inch equipment front-panel system"
        ],
        [
          "Open Rack",
          "A different mechanical and equipment-space system"
        ],
        [
          "U",
          "Conventional vertical allocation unit"
        ],
        [
          "Open Unit",
          "Use the applicable Open Rack specification"
        ]
      ]
    },
    "text_inventory": {
      "sha256": "05b6613b2385998acf028cc8a90547463a955bad83a87f55ab3689f3e9a35b12",
      "entries": [
        {
          "text": "Conventional rack"
        },
        {
          "text": "Nominal 19-inch equipment front- panel system"
        },
        {
          "text": "Open Rack"
        },
        {
          "text": "A different mechanical and equipment-space system"
        },
        {
          "text": "U"
        },
        {
          "text": "Conventional vertical allocation unit"
        },
        {
          "text": "Open Unit"
        },
        {
          "text": "Use the applicable Open Rack specification"
        }
      ],
      "reviewed_on": "2026-10-23",
      "review_method": "Visible media text, OCR-assisted contact sheets and final encoded animation states; original speech independently transcribed. Original-video sampling is every five seconds, not a claim of continuous playback review."
    }
  },
  "reference_links": [
    {
      "label": "OCP Rack and Power",
      "url": "https://www.opencompute.org/projects/rack-and-power"
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_12_open_rack_orientation.txt",
    "wav_file": "audio/module3/slide_12_open_rack_orientation.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 2
    }
  ],
  "term_refs": [
    "open_unit"
  ]
}
```

### Active spoken narration
Open Rack uses a different equipment-space and mechanical approach from the conventional nineteen-inch system. Its commonly described twenty-one-inch equipment space should not be confused with the cabinet's outside width.

Open Rack also uses the Open Unit, which is distinct from the conventional U. Shared power and service arrangements are part of the broader architecture. This vocabulary prepares you for the Intro to OCP series, where the evolution and version-specific design receive a fuller explanation.


### Visible static figure text
Conventional rack
Nominal 19-inch equipment front-  panel system
Open Rack
A different mechanical and  equipment-space system
U
Conventional vertical allocation  unit
Open Unit
Use the applicable Open Rack  specification

## M3S13: Interpret the Layout Before Adding Hardware
Type: content_bullets

### Authored slide fields
```json
{
  "id": 13,
  "type": "content_bullets",
  "slug": "rack_layout_case",
  "title": "Interpret the Layout Before Adding Hardware",
  "section_label": "Apply the Layout",
  "bullets": [
    {
      "text": "The proposed equipment fits the available U space."
    },
    {
      "text": "Cooling allocation is already committed."
    },
    {
      "text": "The required network interface is not available."
    },
    {
      "text": "Identify the infrastructure changes or an alternative placement."
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_13_rack_layout_case.txt",
    "wav_file": "audio/module3/slide_13_rack_layout_case.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 3
    }
  ]
}
```

### Active spoken narration
A team finds several unused positions in a rack and proposes adding a compute system. The new equipment fits mechanically, but the cooling allocation is already committed and its network connection requires a different interface.

What should the team investigate before proceeding? Check the proposed system's electrical, thermal, connectivity and service requirements against the available capacity. The right response may involve another rack, a changed configuration or an infrastructure upgrade. Empty positions alone don't resolve those constraints.


## M3S14: A Rack Is More Than a Stack of Servers
Type: takeaways

### Authored slide fields
```json
{
  "id": 14,
  "type": "takeaways",
  "slug": "rack_takeaways",
  "title": "A Rack Is More Than a Stack of Servers",
  "items": [
    "Nominal panel width and mounting-hole spacing are different dimensions.",
    "U measures vertical allocation, not function or performance.",
    "Equipment roles and chassis arrangements vary by design.",
    "Power, heat removal, connections, access and security shape the layout."
  ],
  "audio": {
    "script_file": "audio/module3/slide_14_rack_takeaways.txt",
    "wav_file": "audio/module3/slide_14_rack_takeaways.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 5
    }
  ]
}
```

### Active spoken narration
Rack dimensions make equipment arrangements repeatable, but they don't determine what every device does. Front-panel width, vertical allocation and cabinet dimensions answer different questions. Compute, storage and shared-chassis designs come in many sizes.

A workable layout also respects power, cooling, cabling, service access and authorized entry. Carry those constraints together when interpreting a rack. They connect the equipment's physical arrangement to the reliable service the facility must support.


## M3S15: Verify Dimensions and Example Form Factors
Type: knowledge_check

### Authored slide fields
```json
{
  "id": 15,
  "type": "knowledge_check",
  "slug": "rack_checks",
  "title": "Verify Dimensions and Example Form Factors",
  "subtitle": "One dimension question and one matching exercise. Submit both to continue.",
  "questions": [
    {
      "id": "m3_kc1",
      "source_check_id": "M3-KC1",
      "prompt": "What does the “19” in a conventional EIA 19-inch rack system refer to?",
      "choices": [
        {
          "id": "a",
          "text": "The height of the rack in inches",
          "correct": false,
          "feedback_incorrect": "Rack height is specified separately, commonly using U. Nineteen inches is the nominal equipment front-panel width."
        },
        {
          "id": "b",
          "text": "The nominal width of the equipment front panel, including its mounting ears",
          "correct": true
        },
        {
          "id": "c",
          "text": "The number of components a rack can hold",
          "correct": false,
          "feedback_incorrect": "Equipment count depends on height and deployment constraints. The nineteen-inch designation is a mechanical width, not a device count."
        },
        {
          "id": "d",
          "text": "The standard depth of a rack",
          "correct": false,
          "feedback_incorrect": "Rack and equipment depths vary. Check the drawings for usable depth; the nineteen-inch designation concerns the front panel."
        }
      ],
      "feedback_correct": "The nominal equipment front-panel width is nineteen inches. Mounting-hole centers are spaced more narrowly, about 18.312 inches.",
      "feedback_incorrect": "Separate panel width, hole spacing, height and depth rather than treating them as one dimension."
    },
    {
      "id": "m3_kc2",
      "type": "matching",
      "source_check_id": "M3-KC2",
      "prompt": "In the illustrated example layout, match each rack-unit allocation to its equipment example.",
      "pairs": [
        {
          "id": "one_u",
          "prompt": "1U",
          "match": "Compact compute server",
          "feedback": "The illustration assigns this compact compute example one U. Other compute systems use different heights."
        },
        {
          "id": "two_u",
          "prompt": "2U",
          "match": "General-purpose enterprise server",
          "feedback": "The illustration uses two U for this general-purpose example. General-purpose servers also exist in other sizes."
        },
        {
          "id": "four_u",
          "prompt": "4U",
          "match": "High-Density Storage Server",
          "feedback": "The illustrated storage example occupies four U. Storage roles do not imply a universal height."
        }
      ],
      "feedback_correct": "These are the sizes of the illustrated examples. U measures height allocation, while actual workloads and products vary.",
      "feedback_incorrect": "Use the example layout to match the pairs. Do not infer a universal size from a server’s role."
    }
  ],
  "audio": {
    "script_file": "audio/module3/slide_15_rack_checks.txt",
    "wav_file": "audio/module3/slide_15_rack_checks.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 4
    }
  ]
}
```

### Active spoken narration
First, identify what the conventional nineteen-inch dimension measures. Then match the illustrated rack-unit examples to their equipment roles. The sizes belong to this example layout; they aren't universal requirements for those workloads.

Submit both questions once to continue. The explanations clarify the dimensions and remind you where real equipment can vary.


## M3S16: Next: Management and Trends
Type: up_next

### Authored slide fields
```json
{
  "id": 16,
  "type": "up_next",
  "slug": "operations_next",
  "title": "Next: Management and Trends",
  "next_module_number": 4,
  "next_module_title": "Management and Trends",
  "thank_you_message": "Thank you for completing Module 3: Inside the Rack.",
  "audio": {
    "script_file": "audio/module3/slide_16_operations_next.txt",
    "wav_file": "audio/module3/slide_16_operations_next.wav",
    "approved": true
  },
  "source_refs": [
    {
      "source": "rise_m3",
      "lesson": 5
    }
  ]
}
```

### Active spoken narration
Thank you for completing Inside the Rack. You can now interpret dimensions and equipment roles while keeping deployment constraints in view.

Module four connects that physical system to ownership, day-to-day management and resource efficiency. You'll consider how teams decide what to improve and how emerging technologies change those decisions.
