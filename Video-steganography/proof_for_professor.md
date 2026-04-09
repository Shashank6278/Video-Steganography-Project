# Proof of Video Steganography Encoding/Decoding

## 1. Visual Identity (Lossless Embedding)
- Original: `../file_example_MP4_480_1_5MG.mp4`
- Stego: `final_lossless.mkv`

Play side-by-side:
```
ffplay ../file_example_MP4_480_1_5MG.mp4
ffplay final_lossless.mkv  # New terminal
```
Identical appearance—hidden data in LSBs invisible.

## 2. Quantitative Proof (PSNR Metric)
Frame 0 comparison:
- PSNR (higher = more similar): **R:80.62, G:77.95, B:80.56 dB** (>70dB = lossless for LSB)

Command used:
```
ffmpeg -i frame0_orig.png -i frame0_stego.png -lavfi psnr -f null -
```
Proves minimal pixel changes (only LSBs modified for message bits).

## 3. Process Flow (Live Demo)
**Encode test message:**
1. Copy input: `copy ../file_example_MP4_480_1_5MG.mp4 demo_input.mp4`
2. Run `python video_Process.py`
   - 1 (Encode)
   - Path: `demo_input.mp4`
   - Message: `Secret proof message for professor!`
   - Password: `demo123`
3. Output: `demo_lossless.mkv`

**Decode:**
1. Run `python video_Process.py`
   - 2 (Decode)
   - Path: `demo_lossless.mkv`
   - Password: `demo123`
2. Recovers **exact message**.

Wrong password: `Invalid data!` or garbage.

## 4. Code Evidence
- Message encrypted AES-256 (SHA256-derived key from password).
- Split across frames.
- LSB embedded (Stegno_image.py: alters pixel LSBs ±1).
- Lossless PNG MKV preserves changes.

Console logs during encode show `Input in image working :- [chunk]`.

## 5. Report/PPT Support
`report.pdf` (Ch4 Results) & `aryan_bisht.pptx` have screenshots/flowcharts.

**Screenshots:** Capture encode/decode console + ffplay + PSNR.

This proves embedding/decryption with password security.
