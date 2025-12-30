import numpy as np
import cv2

def onCook(scriptOp):
    # Parameters you can tweak
    RECT_W = 1  # Width of the box drawn
    RECT_H = 1  # Height of the box drawn
    MODE = 'area' # Options: 'area', 'width', 'height'
    COLOR_MODE = 'grayscale' # Options: 'grayscale', 'rgb'

    # 1. Get input from the first connected node
    if not scriptOp.inputs: return
    input_data = scriptOp.inputs[0].numpyArray(delayed=False)
    
    # TouchDesigner works in 0-1 floats, OpenCV needs 0-255 integers
    # We take the first 3 channels (RGB)
    img_u8 = (input_data[:, :, :3] * 255).astype(np.uint8)

    # 2. Process image to find contours
    gray = cv2.cvtColor(img_u8, cv2.COLOR_RGB2GRAY)
    # Threshold might need adjustment depending on your video brightness
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        # If no movement found, output a black frame
        h_img, w_img = img_u8.shape[:2]
        black = np.zeros((h_img, w_img, 4), dtype=np.float32)
        scriptOp.copyNumpyArray(black)
        return

    # 3. Analyze blobs
    rects = []
    values = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        rects.append((x, y, w, h))

        if MODE == 'area':
            val = w * h
        elif MODE == 'width':
            val = w
        elif MODE == 'height':
            val = h
        else:
            val = w * h
        
        values.append(val)

    # 4. Normalize values for coloring
    vals = np.array(values, dtype=np.float32)
    if len(vals) > 0:
        vmin, vmax = vals.min(), vals.max()
        if vmax - vmin == 0:
            norm_vals = np.zeros_like(vals)
        else:
            norm_vals = (vals - vmin) / (vmax - vmin)
    else:
        norm_vals = []

    # 5. Draw the output
    h_img, w_img = img_u8.shape[:2]
    # Create black background
    out = np.zeros((h_img, w_img, 3), dtype=np.uint8)

    for i, (x, y, w, h) in enumerate(rects):
        cx = x + w // 2
        cy = y + h // 2
        
        # Ensure no drawing outside image bounds
        x1 = max(cx - RECT_W // 2, 0)
        y1 = max(cy - RECT_H // 2, 0)
        x2 = min(cx + RECT_W // 2, w_img)
        y2 = min(cy + RECT_H // 2, h_img)

        v = norm_vals[i]
        
        if COLOR_MODE == 'grayscale':
            color = (int(v * 255),) * 3
        elif COLOR_MODE == 'rgb':
            color = (
                int(255 * (1 - v)),
                int(255 * v),
                int(127 + 128 * np.sin(v * np.pi))
            )
        else:
            color = (255, 255, 255)

        cv2.rectangle(out, (x1, y1), (x2, y2), color, -1)

    # 6. Convert back to TouchDesigner format (add Alpha channel, convert to float)
    out_rgba = np.dstack([out, np.full((h_img, w_img), 255, dtype=np.uint8)])
    out_rgba = out_rgba.astype(np.float32) / 255.0
    
    scriptOp.copyNumpyArray(out_rgba)
