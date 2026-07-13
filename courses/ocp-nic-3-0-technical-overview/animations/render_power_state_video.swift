import AVFoundation
import CoreGraphics
import CoreText
import CoreVideo
import Foundation

let width = 1280
let height = 720
let fps: Int32 = 30
let duration = 22.0
let totalFrames = Int(duration * Double(fps))

let outputPath = CommandLine.arguments.dropFirst().first
    ?? "courses/ocp-nic-3-0-technical-overview/figures/ocp_nic_power_state_sequence.mp4"
let outputURL = URL(fileURLWithPath: outputPath)

try? FileManager.default.removeItem(at: outputURL)

func cgColor(_ hex: UInt32, alpha: CGFloat = 1.0) -> CGColor {
    let r = CGFloat((hex >> 16) & 0xff) / 255.0
    let g = CGFloat((hex >> 8) & 0xff) / 255.0
    let b = CGFloat(hex & 0xff) / 255.0
    return CGColor(red: r, green: g, blue: b, alpha: alpha)
}

let white = cgColor(0xffffff)
let ink = cgColor(0x3f4145)
let muted = cgColor(0x6f7379)
let lineGray = cgColor(0xcbd0d5)
let panelGray = cgColor(0xf4f6f7)
let green = cgColor(0x8dc63f)
let greenDark = cgColor(0x6fa030)
let greenTint = cgColor(0xf2f9e9)
let blue = cgColor(0x343895)
let blueTint = cgColor(0xf1f2fb)
let amber = cgColor(0xc78a18)
let amberTint = cgColor(0xfff7e8)

func topRect(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat) -> CGRect {
    CGRect(x: x, y: CGFloat(height) - y - h, width: w, height: h)
}

func topPoint(_ x: CGFloat, _ y: CGFloat) -> CGPoint {
    CGPoint(x: x, y: CGFloat(height) - y)
}

func smoothstep(_ edge0: Double, _ edge1: Double, _ value: Double) -> CGFloat {
    if value <= edge0 { return 0 }
    if value >= edge1 { return 1 }
    let x = (value - edge0) / (edge1 - edge0)
    return CGFloat(x * x * (3 - 2 * x))
}

func roundedRect(
    _ ctx: CGContext,
    x: CGFloat,
    y: CGFloat,
    w: CGFloat,
    h: CGFloat,
    radius: CGFloat,
    fill: CGColor,
    stroke: CGColor,
    lineWidth: CGFloat = 2
) {
    let path = CGPath(
        roundedRect: topRect(x, y, w, h),
        cornerWidth: radius,
        cornerHeight: radius,
        transform: nil
    )
    ctx.addPath(path)
    ctx.setFillColor(fill)
    ctx.fillPath()
    ctx.addPath(path)
    ctx.setStrokeColor(stroke)
    ctx.setLineWidth(lineWidth)
    ctx.strokePath()
}

enum TextAlign {
    case left
    case center
    case right
}

func drawText(
    _ ctx: CGContext,
    _ text: String,
    x: CGFloat,
    y: CGFloat,
    width: CGFloat,
    size: CGFloat,
    color: CGColor,
    fontName: String = "HelveticaNeue",
    align: TextAlign = .left
) {
    let font = CTFontCreateWithName(fontName as CFString, size, nil)
    let attributes: [CFString: Any] = [
        kCTFontAttributeName: font,
        kCTForegroundColorAttributeName: color,
    ]
    let attributed = CFAttributedStringCreate(nil, text as CFString, attributes as CFDictionary)!
    let line = CTLineCreateWithAttributedString(attributed)
    var ascent: CGFloat = 0
    var descent: CGFloat = 0
    var leading: CGFloat = 0
    let measured = CGFloat(CTLineGetTypographicBounds(line, &ascent, &descent, &leading))
    let drawX: CGFloat
    switch align {
    case .left:
        drawX = x
    case .center:
        drawX = x + max(0, (width - measured) / 2)
    case .right:
        drawX = x + max(0, width - measured)
    }
    ctx.textMatrix = .identity
    ctx.textPosition = CGPoint(x: drawX, y: CGFloat(height) - y - ascent)
    CTLineDraw(line, ctx)
}

func drawPill(
    _ ctx: CGContext,
    text: String,
    x: CGFloat,
    y: CGFloat,
    w: CGFloat,
    fill: CGColor,
    stroke: CGColor,
    textColor: CGColor,
    textSize: CGFloat = 15
) {
    roundedRect(ctx, x: x, y: y, w: w, h: 34, radius: 17, fill: fill, stroke: stroke, lineWidth: 1.5)
    drawText(ctx, text, x: x, y: y + 8, width: w, size: textSize, color: textColor, fontName: "HelveticaNeue-Medium", align: .center)
}

func drawArrow(
    _ ctx: CGContext,
    fromX: CGFloat,
    toBoundaryX: CGFloat,
    y: CGFloat,
    progress: CGFloat,
    color: CGColor
) {
    if progress <= 0.01 { return }
    let tipX = fromX + (toBoundaryX - fromX) * progress
    let head = min(CGFloat(16), max(0, tipX - fromX))
    let backX = tipX - head
    ctx.setStrokeColor(color)
    ctx.setLineWidth(5)
    ctx.setLineCap(.round)
    ctx.move(to: topPoint(fromX, y))
    ctx.addLine(to: topPoint(backX, y))
    ctx.strokePath()
    if progress > 0.04 {
        let path = CGMutablePath()
        path.move(to: topPoint(tipX, y))
        path.addLine(to: topPoint(backX, y - 10))
        path.addLine(to: topPoint(backX, y + 10))
        path.closeSubpath()
        ctx.addPath(path)
        ctx.setFillColor(color)
        ctx.fillPath()
    }
}

func drawVerticalArrow(
    _ ctx: CGContext,
    x: CGFloat,
    fromY: CGFloat,
    toBoundaryY: CGFloat,
    progress: CGFloat,
    color: CGColor
) {
    if progress <= 0.01 { return }
    let tipY = fromY + (toBoundaryY - fromY) * progress
    let head = min(CGFloat(15), max(0, fromY - tipY))
    let backY = tipY + head
    ctx.setStrokeColor(color)
    ctx.setLineWidth(4)
    ctx.setLineCap(.round)
    ctx.setLineDash(phase: 0, lengths: [8, 7])
    ctx.move(to: topPoint(x, fromY))
    ctx.addLine(to: topPoint(x, backY))
    ctx.strokePath()
    ctx.setLineDash(phase: 0, lengths: [])
    if progress > 0.08 {
        let path = CGMutablePath()
        path.move(to: topPoint(x, tipY))
        path.addLine(to: topPoint(x - 10, backY))
        path.addLine(to: topPoint(x + 10, backY))
        path.closeSubpath()
        ctx.addPath(path)
        ctx.setFillColor(color)
        ctx.fillPath()
    }
}

struct StateCard {
    let title: String
    let subtitle: String
    let rail33: String
    let rail12: String
    let note: String
    let x: CGFloat
}

let cards = [
    StateCard(title: "NIC POWER OFF", subtitle: "Rails unavailable", rail33: "+3.3 V  OFF", rail12: "+12 V  OFF", note: "AUX / MAIN disabled", x: 20),
    StateCard(title: "ID MODE", subtitle: "Identity and FRU access", rail33: "+3.3 V  ON", rail12: "+12 V  OPTIONAL", note: "AUX = 0   MAIN = 0", x: 340),
    StateCard(title: "AUX POWER", subtitle: "Management domain active", rail33: "+3.3 V  ON", rail12: "+12 V  ON", note: "PERST# asserted", x: 660),
    StateCard(title: "MAIN POWER", subtitle: "Full NIC operation", rail33: "+3.3 V  ON", rail12: "+12 V  ON", note: "PCIe link enabled", x: 980),
]

func drawCard(_ ctx: CGContext, card: StateCard, index: Int, activeIndex: Int, completedThrough: Int, recap: Bool) {
    let active = index == activeIndex || recap
    let completed = index <= completedThrough || recap
    let fill = active ? greenTint : white
    let stroke = completed ? green : lineGray
    roundedRect(ctx, x: card.x, y: 300, w: 280, h: 214, radius: 18, fill: fill, stroke: stroke, lineWidth: active ? 4 : 2)

    let badgeFill = completed ? green : lineGray
    ctx.setFillColor(badgeFill)
    ctx.fillEllipse(in: topRect(card.x + 18, 318, 34, 34))
    drawText(ctx, String(index + 1), x: card.x + 18, y: 326, width: 34, size: 16, color: white, fontName: "HelveticaNeue-Bold", align: .center)

    drawText(ctx, card.title, x: card.x + 60, y: 319, width: 202, size: 21, color: active ? greenDark : ink, fontName: "HelveticaNeue-Bold")
    drawText(ctx, card.subtitle, x: card.x + 20, y: 367, width: 240, size: 17, color: muted, fontName: "HelveticaNeue-Medium")

    let rail33Fill = card.rail33.hasSuffix("ON") ? greenTint : panelGray
    let rail33Stroke = card.rail33.hasSuffix("ON") ? green : lineGray
    drawPill(ctx, text: card.rail33, x: card.x + 16, y: 404, w: 108, fill: rail33Fill, stroke: rail33Stroke, textColor: card.rail33.hasSuffix("ON") ? greenDark : muted)

    let rail12On = card.rail12.hasSuffix("ON")
    let rail12Optional = card.rail12.contains("OPTIONAL")
    drawPill(
        ctx,
        text: card.rail12,
        x: card.x + 136,
        y: 404,
        w: 128,
        fill: rail12On ? greenTint : (rail12Optional ? amberTint : panelGray),
        stroke: rail12On ? green : (rail12Optional ? amber : lineGray),
        textColor: rail12On ? greenDark : (rail12Optional ? amber : muted),
        textSize: rail12Optional ? 14 : 15
    )
    drawText(ctx, card.note, x: card.x + 20, y: 463, width: 240, size: 17, color: active ? ink : muted, fontName: "HelveticaNeue-Medium", align: .center)
}

func renderFrame(_ pixelBuffer: CVPixelBuffer, time: Double) {
    CVPixelBufferLockBaseAddress(pixelBuffer, [])
    defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, []) }

    guard let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer) else { return }
    let bytesPerRow = CVPixelBufferGetBytesPerRow(pixelBuffer)
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bitmapInfo = CGBitmapInfo.byteOrder32Little.rawValue | CGImageAlphaInfo.premultipliedFirst.rawValue
    guard let ctx = CGContext(
        data: baseAddress,
        width: width,
        height: height,
        bitsPerComponent: 8,
        bytesPerRow: bytesPerRow,
        space: colorSpace,
        bitmapInfo: bitmapInfo
    ) else { return }

    ctx.setFillColor(white)
    ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    ctx.setShouldAntialias(true)

    drawText(ctx, "OCP NIC 3.0 POWER STATE SEQUENCE", x: 40, y: 34, width: 860, size: 34, color: ink, fontName: "HelveticaNeue-Bold")
    drawText(ctx, "Specification v1.6.0", x: 930, y: 43, width: 310, size: 19, color: blue, fontName: "HelveticaNeue-Bold", align: .right)
    ctx.setStrokeColor(green)
    ctx.setLineWidth(6)
    ctx.move(to: topPoint(40, 90))
    ctx.addLine(to: topPoint(235, 90))
    ctx.strokePath()
    drawText(ctx, "Four mandatory states", x: 40, y: 106, width: 450, size: 20, color: muted, fontName: "HelveticaNeue-Medium")

    let p1 = smoothstep(3.7, 4.8, time)
    let p2 = smoothstep(7.7, 8.8, time)
    let p3 = smoothstep(11.7, 12.8, time)
    let pOptional = smoothstep(16.2, 17.4, time)
    let recap = time >= 19.2

    let activeIndex: Int
    let completedThrough: Int
    let status: String
    let phaseLabel: String
    if time < 4.2 {
        activeIndex = 0
        completedThrough = 0
        status = "Start: +3.3 V_EDGE and +12 V_EDGE are off."
        phaseLabel = "POWER OFF"
    } else if time < 8.2 {
        activeIndex = 1
        completedThrough = 1
        status = "+3.3 V_EDGE applied - FRU EEPROM identity becomes available."
        phaseLabel = "ID MODE"
    } else if time < 12.2 {
        activeIndex = 2
        completedThrough = 2
        status = "AUX_PWR_EN = 1 - PERST# remains asserted while AUX-domain rails stabilize."
        phaseLabel = "AUX POWER"
    } else if time < 16.5 {
        activeIndex = 3
        completedThrough = 3
        status = "MAIN_PWR_EN = 1 - main circuitry and PCIe operation are enabled."
        phaseLabel = "MAIN POWER"
    } else if time < 19.2 {
        activeIndex = 1
        completedThrough = 3
        status = "Programming Mode is an optional baseboard-controlled branch from ID Mode."
        phaseLabel = "OPTIONAL FIELD UPDATE"
    } else {
        activeIndex = -1
        completedThrough = 3
        status = "Mandatory sequence: Power Off -> ID -> Aux -> Main. Programming Mode is optional."
        phaseLabel = "SEQUENCE COMPLETE"
    }

    // The optional branch is separate from the mandatory left-to-right sequence.
    let programmingActive = time >= 16.5 && time < 19.2
    roundedRect(
        ctx,
        x: 365,
        y: 145,
        w: 230,
        h: 102,
        radius: 16,
        fill: programmingActive ? blueTint : panelGray,
        stroke: programmingActive ? blue : lineGray,
        lineWidth: programmingActive ? 4 : 2
    )
    drawText(ctx, "PROGRAMMING", x: 383, y: 158, width: 194, size: 18, color: programmingActive ? blue : muted, fontName: "HelveticaNeue-Bold", align: .center)
    drawText(ctx, "MODE", x: 383, y: 181, width: 194, size: 18, color: programmingActive ? blue : muted, fontName: "HelveticaNeue-Bold", align: .center)
    drawText(ctx, "OPTIONAL", x: 407, y: 212, width: 146, size: 13, color: programmingActive ? blue : muted, fontName: "HelveticaNeue-Bold", align: .center)

    for index in cards.indices {
        drawCard(ctx, card: cards[index], index: index, activeIndex: activeIndex, completedThrough: completedThrough, recap: recap)
    }

    let cardWidth: CGFloat = 280
    let centerY: CGFloat = 407
    drawArrow(ctx, fromX: cards[0].x + cardWidth, toBoundaryX: cards[1].x, y: centerY, progress: 1, color: lineGray)
    drawArrow(ctx, fromX: cards[1].x + cardWidth, toBoundaryX: cards[2].x, y: centerY, progress: 1, color: lineGray)
    drawArrow(ctx, fromX: cards[2].x + cardWidth, toBoundaryX: cards[3].x, y: centerY, progress: 1, color: lineGray)
    drawArrow(ctx, fromX: cards[0].x + cardWidth, toBoundaryX: cards[1].x, y: centerY, progress: p1, color: green)
    drawArrow(ctx, fromX: cards[1].x + cardWidth, toBoundaryX: cards[2].x, y: centerY, progress: p2, color: green)
    drawArrow(ctx, fromX: cards[2].x + cardWidth, toBoundaryX: cards[3].x, y: centerY, progress: p3, color: green)

    drawVerticalArrow(ctx, x: 480, fromY: 300, toBoundaryY: 247, progress: 1, color: lineGray)
    drawVerticalArrow(ctx, x: 480, fromY: 300, toBoundaryY: 247, progress: pOptional, color: blue)
    drawText(ctx, "FIELD UPDATE", x: 495, y: 264, width: 120, size: 13, color: pOptional > 0.25 ? blue : lineGray, fontName: "HelveticaNeue-Bold")

    roundedRect(ctx, x: 40, y: 558, w: 1200, h: 108, radius: 18, fill: panelGray, stroke: lineGray, lineWidth: 1.5)
    drawText(ctx, phaseLabel, x: 68, y: 578, width: 260, size: 16, color: recap ? greenDark : blue, fontName: "HelveticaNeue-Bold")
    drawText(ctx, status, x: 68, y: 611, width: 1110, size: 22, color: ink, fontName: "HelveticaNeue-Medium")

    // A small progress rail reinforces the direction of the mandatory sequence.
    ctx.setStrokeColor(lineGray)
    ctx.setLineWidth(5)
    ctx.setLineCap(.round)
    ctx.move(to: topPoint(910, 587))
    ctx.addLine(to: topPoint(1172, 587))
    ctx.strokePath()
    let progress = min(CGFloat(1), CGFloat(time / 19.2))
    ctx.setStrokeColor(green)
    ctx.move(to: topPoint(910, 587))
    ctx.addLine(to: topPoint(910 + 262 * progress, 587))
    ctx.strokePath()

    let fadeIn = smoothstep(0.0, 0.65, time)
    let fadeOut = 1 - smoothstep(21.35, 22.0, time)
    let visible = min(fadeIn, fadeOut)
    if visible < 1 {
        ctx.setFillColor(cgColor(0xffffff, alpha: 1 - visible))
        ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    }
}

let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
let compression: [String: Any] = [
    AVVideoAverageBitRateKey: 3_500_000,
    AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
]
let videoSettings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height,
    AVVideoCompressionPropertiesKey: compression,
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
input.expectsMediaDataInRealTime = false

let pixelAttributes: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA),
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height,
    kCVPixelBufferIOSurfacePropertiesKey as String: [:] as [String: Any],
]
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: pixelAttributes)

guard writer.canAdd(input) else {
    fatalError("Unable to add the video input")
}
writer.add(input)
guard writer.startWriting() else {
    fatalError("Unable to start video writer: \(writer.error?.localizedDescription ?? "unknown error")")
}
writer.startSession(atSourceTime: .zero)

for frame in 0..<totalFrames {
    while !input.isReadyForMoreMediaData {
        Thread.sleep(forTimeInterval: 0.002)
    }
    guard let pool = adaptor.pixelBufferPool else {
        fatalError("Video pixel buffer pool is unavailable")
    }
    var maybeBuffer: CVPixelBuffer?
    let status = CVPixelBufferPoolCreatePixelBuffer(nil, pool, &maybeBuffer)
    guard status == kCVReturnSuccess, let buffer = maybeBuffer else {
        fatalError("Unable to allocate frame \(frame): \(status)")
    }
    let time = Double(frame) / Double(fps)
    renderFrame(buffer, time: time)
    let presentationTime = CMTime(value: Int64(frame), timescale: fps)
    if !adaptor.append(buffer, withPresentationTime: presentationTime) {
        fatalError("Unable to append frame \(frame): \(writer.error?.localizedDescription ?? "unknown error")")
    }
}

input.markAsFinished()
let completion = DispatchSemaphore(value: 0)
writer.finishWriting {
    completion.signal()
}
completion.wait()

guard writer.status == .completed else {
    fatalError("Video export failed: \(writer.error?.localizedDescription ?? "unknown error")")
}

print("wrote \(outputURL.path) (\(totalFrames) frames at \(fps) fps)")
