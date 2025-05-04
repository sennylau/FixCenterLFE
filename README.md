# 🎧 FixCenterLFE

**FixCenterLFE** is a lightweight macOS tool that intercepts multi-channel audio in real time and fixes incorrect channel mapping between the **Center** and **LFE (Subwoofer)** channels — a common issue when running Windows games via **Crossover** or **Wine**.

> ✅ Fixes voice/dialog audio being incorrectly routed to the subwoofer  
> ✅ Works in real-time with low latency using [BlackHole](https://github.com/ExistentialAudio/BlackHole)  
> ✅ Open source, Apache-2.0 licensed

---

## 🔍 Problem

Many Wine-based Windows games assume Windows-style surround sound mapping. On macOS, when using HDMI or multichannel audio devices, the **Center** and **LFE** channels are often flipped. This causes:

- Game narration or voice dialog routed to the subwoofer
- Movies sounding fine, but Wine apps sounding wrong
- No easy way to remap audio channels globally

---

## 🎮 Supported Games

- Black Myth: Wukong (黑神话悟空)
- Split Fiction (双影奇境)
- Other Wine/Crossover games with center/LFE channel issues

## 🎯 Solution

**FixCenterLFE** sits between the system audio output and your real audio hardware, capturing audio in real time, **swapping channel 3 (Center) and channel 4 (LFE)**, and passing the corrected signal to your speakers.

### 🧭 Signal Flow

```text
          ┌──────────────┐
          │ macOS System │
          │ (Wine/Crossover Game) 
          └──────┬───────┘
                 │
          [Multichannel Audio]
                 │
          ▼ BlackHole (Virtual Output)
┌────────────────────────────────────┐
│          FixCenterLFE              │
│  (Python or Native Audio Processor)│
│       ⟶ Swap Channel 3 & 4         │
└────────────┬───────────────────────┘
             │
      [Corrected Multichannel Audio]
             │
      ▼ Real Output Device (e.g. HDMI, Headphones)

## 🤝 Contributing

PRs are welcome! To contribute:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please include:
- Description of changes
- Testing details
- Screenshots if applicable

## 🧪 Testing
Verified working with:
- [x] Black Myth: Wukong
- [x] Split Fiction
- [ ] Other games (please report your tests!)
