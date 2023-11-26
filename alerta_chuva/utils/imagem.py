import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def transparency_mask(img: np.ndarray) -> np.ndarray:
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # Encontre os pixels pretos (com todos os canais R, G, B iguais a 0)
    black_pixels = np.all(img_rgba[:, :, :3] == [0, 0, 0], axis=2)
    # Atribua transparência (canal alfa = 0) aos pixels pretos
    img_rgba[black_pixels] = [0, 0, 0, 0]
    return img_rgba


def screenshot_map(url: str, filename: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div"))
    ).screenshot(filename)
    return filename
