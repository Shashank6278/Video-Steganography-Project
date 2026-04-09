# Video Steganography Proof for Professor

## Overview
The MKV shows random letters in text editors because it's **binary video data**, not text. Hidden message is in **LSB (Least Significant Bit)** of pixel values—invisible changes.

## Quantitative Proofs
**PSNR (Peak Signal-to-Noise Ratio)**: Frame 0 orig vs stego
- R: 80.62 dB, G: 77.95 dB, B: 80.56 dB
- **>70dB = visually identical** (only LSB changed).

**Pixel Differences** (OpenCV analysis):
```
Pixels differing: 282 / 129600 (0.22%)
```
Minimal changes = lossless embedding.

**LSB Proof** (Red channel top-left 3x3 pixels):
```
Orig LSB: [[0 0 0]
           [0 0 0]
           [0 0 0]]

Stego LSB: [[0 1 0]
            [0 0 0]
            [0 0 0]]
```
**Position (1,2) changed 0→1**: Pixel value e.g., 100 (binary ...01100100) → 101 (....01100101). LSB flip embeds 1 message bit. **Proves LSB steganography**—script alters LSB to hide encrypted message bits.

## Full Process
1. **Encode**: Message → AES encrypt (password key) → split → LSB frames → lossless MKV.
2. **Console**: Shows \"Input in image working :- [chunk]\" per frame.
3. **Decode**: MKV → frames → LSB extract → AES decrypt → message.

## Live Demo
```
copy file_example_MP4_480_1_5MG.mp4 demo.mp4
python video_Process.py  # 1 Encode, msg:\"Professor proof\", pwd:\"123\"
python video_Process.py  # 2 Decode, same pwd → exact msg
```
Wrong pwd: garbage/\"Invalid data!\".

## Commands Run (Proof Generated)
1. Extract frames → success.
2. PSNR → high values.
3. Python → LSB diffs.

**Irrefutable**: Visual same + LSB changes + decode recovery + password protection.

Use with `report.pdf` screenshots.
