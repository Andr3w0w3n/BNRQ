import json


filepath = r"V:\NUKE Addons - KEEP\Created Scripts\RenderQ\FourCharacter-Codes.json"


four_cc_list = {
    '1': "Uncompressed 1-bit Indexed Color",
    '2': "Uncompressed 2-bit Indexed Color",
    '2vuy': "Component Y'CbCr 8-bit 4:2:2 ordered Cb Y'0 Cr Y'1",
    '4': "Uncompressed 4-bit Indexed Color",
    '8': "Uncompressed 8-bit Indexed Color",
    '8BPS': "Planar RGB",
    '16': "Uncompressed 16-bit RGB 555 (Big Endian)",
    '24': "Uncompressed 24-bit RGB",
    '24BG': "Uncompressed 24-bit BGR",
    '32': "Uncompressed 32-bit ARGB",
    '33': "Uncompressed 1-bit Grayscale",
    '34': "Uncompressed 2-bit Grayscale",
    '36': "Uncompressed 4-bit Grayscale",
    '40': "Uncompressed 8-bit Grayscale",
    '5551': "Uncompressed 16-bit RGB 5551 (Little Endian)",
    'a2vy': "Two-Plane Component Y'CbCr,A 8-bit 4:2:2,4",
    'ABGR': "Uncompressed 32-bit ABGR",
    'ai5p': "AVC-Intra  50M 720p24/30/60",
    'ai5q': "AVC-Intra  50M 720p25/50",
    'ai52': "AVC-Intra  50M 1080p25/50",
    'ai53': "AVC-Intra  50M 1080p24/30/60",
    'ai55': "AVC-Intra  50M 1080i50",
    'ai56': "AVC-Intra  50M 1080i60",
    'ai1p': "AVC-Intra 100M 720p24/30/60",
    'ai1q': "AVC-Intra 100M 720p25/50",
    'ai12': "AVC-Intra 100M 1080p25/50",
    'ai13': "AVC-Intra 100M 1080p24/30/60",
    'ai15': "AVC-Intra 100M 1080i50",
    'ai16': "AVC-Intra 100M 1080i60",
    'ACTL': "Streambox ACT-L2",
    'ap4h': "Apple ProRes 4444",
    'ap4x': "Apple ProRes 4444 (XQ)",
    'apch': "Apple ProRes 422 (HQ)",
    'apcn': "Apple ProRes 422",
    'apco': "Apple ProRes 422 (Proxy)",
    'apcs': "Apple ProRes 422 (LT)",
    'appr': "Apple ProRes",
    'avc1': "H.264",
    'AVdn': "Avid DNxHD",
    'AVdh': "Avid DNxHR",
    'AVRn': "Avid Motion JPEG",
    'AVDJ': "Avid Motion JPEG",
    'ADJV': "Avid Motion JPEG",
    'avr': "Motion JPEG AVR",
    'b16g': "Uncompressed 16-bit Grayscale",
    'b32a': "Uncompressed 32-bit AlphaGray",
    'b48r': "Uncompressed 48-bit RGB",
    'b64a': "Uncompressed 64-bit ARGB",
    'B565': "Uncompressed 16-bit RGB 565 (Big Endian)",
    'BGRA': "Uncompressed 32-bit BGRA",
    'cvid': "Cinepak",
    'dmb1': "Motion JPEG OpenDML",
    'drmi': "AVC0 Media",
    'dv1p': "DV Video C Pro 100 PAL",
    'dv1n': "DV Video C Pro 100 NTSC",
    'dv5n': "DVCPRO50 - NTSC",
    'dv5p': "DVCPRO50 - PAL",
    'dvc': "DV/DVCPRO NTSC",
    'dvcp': "DVC - PAL",
    'dvh2': "DVCPRO HD (1080p25)",
    'dvh3': "DVCPRO HD (1080p30)",
    'dvh5': "DVCPRO HD (1080i50)",
    'dvh6': "DVCPRO HD (1080i60)",
    'dvhp': "DVCPRO HD (720p60)",
    'dvhq': "DVCPRO HD (720p50)",
    'dvp': "DV Video Pro",
    'dvpp': "DVCPRO - PAL",
    'flv': "Flash",
    'gif': "GIF",
    'h261': "H.261",
    'h263': "H.263",
    'h264': "H.264",
    'hdv1': "HDV (720p30)",
    'hdv2': "HDV (1080i60)",
    'hdv3': "HDV (1080i50)",
    'hdv4': "HDV (720p24)",
    'hdv5': "HDV (720p25)",
    'hdv6': "HDV (1080p24)",
    'hdv7': "HDV (1080p25)",
    'hdv8': "HDV (1080p30)",
    'hdv9': "HDV (720p60)",
    'hdva': "HDV (720p50)",
    'icod': "Apple Intermediate Codec",
    'IV41': "Intel Indeo Video 4.3",
    'IV50': "Indeo video 5.1",
    'jpeg': "Photo - JPEG",
    'Jvt3': "Apple H.264/AVC Video (Preview)",
    'L555': "Uncompressed 16-bit RGB 555 (Little Endian)",
    'L565': "Uncompressed 16-bit RGB 565 (Little Endian)",
    'mjp2': "JPEG 2000",
    'mjpa': "Motion JPEG A",
    'mjpb': "Motion JPEG B",
    'mjpg': "Motion JPEG",
    'mpg4': "MPEG-4 Video",
    'mp1v': "MPEG-1 Video",
    'mp2v': "MPEG-2 Video",
    'mp4v': "MPEG-4 Video",
    'mplo': "Implode",
    'png': "PNG",
    '\"png \"': "PNG",
    'pxlt': "Apple Pixlet Video",
    'r210': "Blackmagic Uncompressed RAW 10bit",
    'r408': "Component Y'CbCrA 8-bit 4:4:4:4 ordered A Y' Cb Cr",
    'RGBA': "Uncompressed 32-bit RGBA",
    'rle': "Animation",
    '\"rle \"': "Animation",
    'rpza': "Video",
    's263': "H.263",
    'smc': "Graphics",
    'theo': "Xiph.org's Theora Video",
    'v210': "Component Y'CbCr 10-bit 4:2:2, Uncompressed",
    'v216': "Component Y'CbCr 10,12,14,16-bit 4:2:2",
    'v264': "H.264",
    'v308': "Component Y'CbCr 8-bit 4:4:4",
    'v408': "Component Y'CbCrA 8-bit 4:4:4:4 ordered Cb Y' Cr A",
    'v410': "Component Y'CbCr 10-bit 4:4:4",
    'VP30': "On2 VP3 Video 3.2",
    'VP31': "On2 VP3 Video 3.2",
    'VP50': "On2's VP5 Video",
    'VP60': "On2's VP6 Video",
    'VP70': "On2's VP7 Video",
    'wmv1': "Windows Media Video 7",
    'wmv2': "Windows Media Video 8",
    'wmv3': "Windows Media Video 9",
    'x264': "H.264",
    'xd5a': "XDCAM HD422 (720p50)",
    'xd59': "XDCAM HD422 (720p60)",
    'xdv1': "XDCAM EX (720p30)",
    'xdv2': "XDCAM HD (1080i60)",
    'xdv3': "XDCAM HD (1080i50)",
    'xdv4': "XDCAM EX (720p24)",
    'xdv5': "XDCAM EX (720p25)",
    'xdv6': "XDCAM HD (1080p24)",
    'xdv7': "XDCAM HD (1080p25)",
    'xdv8': "XDCAM HD (1080p30)",
    'xdv9': "XDCAM EX (720p60)",
    'xdva': "XDCAM EX (720p50)",
    'xplo': "Implode",
    'y420': "Three-Plane Component Y'CbCr 8-bit 4:2:0",
    'yuvs': "Component Y'CbCr 8-bit 4:2:2 ordered Y'0 Cb Y'1 Cr",
    'zygo': "ZyGoVideo",
}


json.dump(four_cc_list, open(filepath, "w"))