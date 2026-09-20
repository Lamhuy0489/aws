import Cocoa
import Vision

let args = CommandLine.arguments
guard args.count > 1 else {
    fputs("Usage: swift ocr.swift <image_path>\n", stderr)
    exit(1)
}

let path = args[1]
guard let image = NSImage(contentsOfFile: path),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    fputs("Failed to load image at: \(path)\n", stderr)
    exit(1)
}

let request = VNRecognizeTextRequest { (request, error) in
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    let width = CGFloat(cgImage.width)
    let height = CGFloat(cgImage.height)
    for obs in observations {
        guard let candidate = obs.topCandidates(1).first else { continue }
        let box = obs.boundingBox
        // Apple Vision bounding box is normalized with (0,0) at bottom-left
        let x = box.origin.x * width
        let y = (1.0 - box.origin.y - box.size.height) * height
        let w = box.size.width * width
        let h = box.size.height * height
        let sanitized = candidate.string
            .replacingOccurrences(of: "\\", with: "\\\\")
            .replacingOccurrences(of: "\"", with: "\\\"")
        print(String(format: "{\"text\": \"%@\", \"x\": %.1f, \"y\": %.1f, \"w\": %.1f, \"h\": %.1f}", sanitized, x, y, w, h))
    }
}

request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
} catch {
    fputs("OCR Error: \(error)\n", stderr)
    exit(1)
}
