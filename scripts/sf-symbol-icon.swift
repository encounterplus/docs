#!/usr/bin/env swift

// Renders SF Symbols to PNGs for use as inline icons in the docs.
//
// Symbol *names* are stable API, so the icon set is described by a name list
// (scripts/symbols.txt) and regenerated from it rather than exported by hand.
//
//   ./scripts/sf-symbol-icon.swift --list scripts/symbols.txt --out public/assets/symbols
//   ./scripts/sf-symbol-icon.swift wrench.and.screwdriver --out public/assets/symbols
//
// Output is flat monochrome on transparent, which is what the docs' dark-mode rule needs
// — src/styles/custom.css recolours these with `filter: invert(1)`, and that only works
// for flat single-colour art. Do not switch this to hierarchical or multicolour rendering.
//
// The default tint is a mid grey rather than black. Inline icons sit in running text, and
// pure black inverts to pure white, which reads brighter than the body text around it. A
// grey inverts to a lighter grey and stays level with the prose in both themes.
//
// PNG rather than SVG: AppKit rasterises symbol artwork on the way into any context
// (an NSSymbolImageRep drawn into a PDF context emits an embedded bitmap, not paths),
// and the vector outlines in SF Symbols.app's SFSymbolsFallback.otf are keyed by
// private-use codepoints with no published name mapping. Icons render at 1.5rem, so
// a 3x asset is indistinguishable from vector at any display density.

import AppKit
import Foundation

struct RenderError: LocalizedError {
    let message: String
    var errorDescription: String? { message }
}

func png(for name: String, pointSize: CGFloat, weight: NSFont.Weight, scale: NSImage.SymbolScale, factor: Int, tint: NSColor) throws -> Data {
    guard let base = NSImage(systemSymbolName: name, accessibilityDescription: name) else {
        throw RenderError(message: "no such SF Symbol: \(name)")
    }
    let config = NSImage.SymbolConfiguration(pointSize: pointSize, weight: weight, scale: scale)
    guard let image = base.withSymbolConfiguration(config) else {
        throw RenderError(message: "could not apply symbol configuration to \(name)")
    }

    let size = image.size
    let pixelsWide = Int((size.width * CGFloat(factor)).rounded())
    let pixelsHigh = Int((size.height * CGFloat(factor)).rounded())
    guard let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: pixelsWide, pixelsHigh: pixelsHigh,
                                     bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                                     colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0) else {
        throw RenderError(message: "could not create a bitmap for \(name)")
    }
    rep.size = size

    let bounds = CGRect(origin: .zero, size: size)
    let previous = NSGraphicsContext.current
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
    image.draw(in: bounds)
    // Symbol images always draw black; recolour by painting the tint through the alpha
    // the symbol just laid down.
    tint.set()
    bounds.fill(using: .sourceIn)
    NSGraphicsContext.current = previous

    guard let data = rep.representation(using: .png, properties: [:]) else {
        throw RenderError(message: "could not encode \(name) as PNG")
    }
    return data
}

func usage() -> Never {
    FileHandle.standardError.write("""
    usage: sf-symbol-icon.swift [NAME ...] [--list FILE] --out DIR
                                [--weight regular|light|medium|semibold|bold]
                                [--scale small|medium|large] [--point-size N] [--factor N]
                                [--tint HEX]

    Names may be given on the command line, in a --list file (one per line, # comments
    ignored), or both. Each becomes DIR/<name>.png.
    """.appending("\n").data(using: .utf8)!)
    exit(2)
}

var names: [String] = []
var outDir: String?
var listFile: String?
var pointSize: CGFloat = 24
var factor = 3
var weight: NSFont.Weight = .regular
var scale: NSImage.SymbolScale = .medium
// Inverts to #999999 for dark mode; see the note at the top of this file.
var tint = NSColor(red: 0.4, green: 0.4, blue: 0.4, alpha: 1)

var args = Array(CommandLine.arguments.dropFirst())
while let arg = args.first {
    args.removeFirst()
    func value() -> String {
        guard let v = args.first else { usage() }
        args.removeFirst()
        return v
    }
    switch arg {
    case "--out": outDir = value()
    case "--list": listFile = value()
    case "--point-size":
        guard let n = Double(value()) else { usage() }
        pointSize = CGFloat(n)
    case "--factor":
        guard let n = Int(value()), n > 0 else { usage() }
        factor = n
    case "--weight":
        let map: [String: NSFont.Weight] = [
            "ultralight": .ultraLight, "thin": .thin, "light": .light, "regular": .regular,
            "medium": .medium, "semibold": .semibold, "bold": .bold, "heavy": .heavy, "black": .black,
        ]
        guard let w = map[value().lowercased()] else { usage() }
        weight = w
    case "--scale":
        let map: [String: NSImage.SymbolScale] = ["small": .small, "medium": .medium, "large": .large]
        guard let s = map[value().lowercased()] else { usage() }
        scale = s
    case "--tint":
        let hex = value().trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        guard hex.count == 6, let rgb = Int(hex, radix: 16) else { usage() }
        tint = NSColor(red: CGFloat((rgb >> 16) & 0xFF) / 255,
                       green: CGFloat((rgb >> 8) & 0xFF) / 255,
                       blue: CGFloat(rgb & 0xFF) / 255, alpha: 1)
    case "-h", "--help": usage()
    default:
        if arg.hasPrefix("-") { usage() }
        names.append(arg)
    }
}

if let listFile {
    guard let contents = try? String(contentsOfFile: listFile, encoding: .utf8) else {
        FileHandle.standardError.write("cannot read \(listFile)\n".data(using: .utf8)!)
        exit(1)
    }
    for line in contents.split(separator: "\n", omittingEmptySubsequences: false) {
        let trimmed = line.prefix { $0 != "#" }.trimmingCharacters(in: .whitespaces)
        if !trimmed.isEmpty { names.append(trimmed) }
    }
}

guard let outDir, !names.isEmpty else { usage() }
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)

var failed = 0
for name in names {
    do {
        let data = try png(for: name, pointSize: pointSize, weight: weight, scale: scale, factor: factor, tint: tint)
        let path = (outDir as NSString).appendingPathComponent("\(name).png")
        try data.write(to: URL(fileURLWithPath: path))
        print("wrote \(path)")
    } catch {
        FileHandle.standardError.write("error: \(error.localizedDescription)\n".data(using: .utf8)!)
        failed += 1
    }
}
exit(failed == 0 ? 0 : 1)
