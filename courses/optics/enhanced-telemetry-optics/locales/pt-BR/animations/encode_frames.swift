import AppKit
import AVFoundation
import CoreGraphics
import CoreVideo
import Foundation
import ImageIO

struct EncodeError: Error, CustomStringConvertible {
  let description: String
}

func fail(_ message: String) throws -> Never {
  throw EncodeError(description: message)
}

func cgImage(from url: URL) throws -> CGImage {
  let data = try Data(contentsOf: url)
  guard let source = CGImageSourceCreateWithData(data as CFData, nil),
        let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    try fail("Could not read image: \(url.path)")
  }
  return image
}

func pixelBuffer(from image: CGImage, width: Int, height: Int) throws -> CVPixelBuffer {
  let attrs: [String: Any] = [
    kCVPixelBufferCGImageCompatibilityKey as String: true,
    kCVPixelBufferCGBitmapContextCompatibilityKey as String: true,
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height,
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB
  ]

  var buffer: CVPixelBuffer?
  let status = CVPixelBufferCreate(
    kCFAllocatorDefault,
    width,
    height,
    kCVPixelFormatType_32ARGB,
    attrs as CFDictionary,
    &buffer
  )
  guard status == kCVReturnSuccess, let pixelBuffer = buffer else {
    try fail("Could not create pixel buffer")
  }

  CVPixelBufferLockBaseAddress(pixelBuffer, [])
  defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, []) }

  let colorSpace = CGColorSpaceCreateDeviceRGB()
  guard let context = CGContext(
    data: CVPixelBufferGetBaseAddress(pixelBuffer),
    width: width,
    height: height,
    bitsPerComponent: 8,
    bytesPerRow: CVPixelBufferGetBytesPerRow(pixelBuffer),
    space: colorSpace,
    bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
  ) else {
    try fail("Could not create bitmap context")
  }

  context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
  return pixelBuffer
}

func encode(framesDir: URL, outputURL: URL, fps: Int32) throws {
  let frameURLs = try FileManager.default
    .contentsOfDirectory(at: framesDir, includingPropertiesForKeys: nil)
    .filter { $0.pathExtension.lowercased() == "png" }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }

  guard let firstURL = frameURLs.first else {
    try fail("No PNG frames found in \(framesDir.path)")
  }

  let first = try cgImage(from: firstURL)
  let width = first.width
  let height = first.height

  try? FileManager.default.removeItem(at: outputURL)

  let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
  let settings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height,
    AVVideoCompressionPropertiesKey: [
      AVVideoAverageBitRateKey: 4_000_000,
      AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel
    ]
  ]

  let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
  input.expectsMediaDataInRealTime = false
  guard writer.canAdd(input) else {
    try fail("Could not add video input")
  }
  writer.add(input)

  let adaptor = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: input,
    sourcePixelBufferAttributes: [
      kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
      kCVPixelBufferWidthKey as String: width,
      kCVPixelBufferHeightKey as String: height
    ]
  )

  writer.startWriting()
  writer.startSession(atSourceTime: .zero)

  for (index, url) in frameURLs.enumerated() {
    while !input.isReadyForMoreMediaData {
      Thread.sleep(forTimeInterval: 0.01)
    }
    let image = try cgImage(from: url)
    let buffer = try pixelBuffer(from: image, width: width, height: height)
    let time = CMTime(value: CMTimeValue(index), timescale: fps)
    if !adaptor.append(buffer, withPresentationTime: time) {
      try fail("Failed to append frame \(url.lastPathComponent)")
    }
  }

  input.markAsFinished()
  let semaphore = DispatchSemaphore(value: 0)
  writer.finishWriting {
    semaphore.signal()
  }
  semaphore.wait()

  guard writer.status == .completed else {
    let message = writer.error?.localizedDescription ?? "unknown AVAssetWriter error"
    try fail("Encoding failed: \(message)")
  }

  print("Encoded \(frameURLs.count) frames at \(fps) fps -> \(outputURL.path)")
}

do {
  guard CommandLine.arguments.count >= 3 else {
    try fail("Usage: swift encode_frames.swift <frames-dir> <output.mp4> [fps]")
  }
  let framesDir = URL(fileURLWithPath: CommandLine.arguments[1])
  let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
  let fps = Int32(CommandLine.arguments.dropFirst(3).first ?? "24") ?? 24
  try encode(framesDir: framesDir, outputURL: outputURL, fps: fps)
} catch {
  FileHandle.standardError.write(Data("\(error)\n".utf8))
  exit(1)
}
