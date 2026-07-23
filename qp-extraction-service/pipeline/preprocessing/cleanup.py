import cv2
import numpy as np
from .orientation import correct_orientation

def compute_skew_angle(image: np.ndarray, angle_range=(-50, 50), coarse_step=2, fine_step=0.2) -> float:
    def score_angle(angle):
        h, w = image.shape
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
        row_sums = np.sum(rotated < 128, axis=1)
        return np.var(row_sums)

    # Coarse pass across the full range
    best_angle, best_score = 0, -1
    for angle in np.arange(angle_range[0], angle_range[1] + coarse_step, coarse_step):
        score = score_angle(angle)
        if score > best_score:
            best_score, best_angle = score, angle

    # Fine pass around the coarse best
    refined_angle, refined_score = best_angle, best_score
    for angle in np.arange(best_angle - coarse_step, best_angle + coarse_step, fine_step):
        score = score_angle(angle)
        if score > refined_score:
            refined_score, refined_angle = score, angle

    return refined_angle

def clean_scanned_page(image: np.ndarray) -> np.ndarray:
    image = correct_orientation(image)  # fixes 90/180/270 first

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    angle = compute_skew_angle(denoised)
    print(f"[cleanup] detected skew angle: {angle:.2f}")

    h, w = denoised.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(denoised, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    binarized = cv2.adaptiveThreshold(deskewed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)
    return binarized