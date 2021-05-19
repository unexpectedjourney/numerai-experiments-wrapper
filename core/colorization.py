import asyncio
import colorsys
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import sparse
from scipy.sparse import linalg

from utils.database.file_version import insert_file_version
from utils.files import generate_filename
from utils.logger import setup_logger

log = setup_logger(__name__)


def yiq_to_rgb(y, i, q):
    r = y + 0.948262 * i + 0.624013 * q
    g = y - 0.276066 * i - 0.639810 * q
    b = y - 1.105450 * i + 1.729860 * q
    r[r < 0] = 0
    r[r > 1] = 1
    g[g < 0] = 0
    g[g > 1] = 1
    b[b < 0] = 0
    b[b > 1] = 1
    return r, g, b


def preprocess(original_filepath, marked_filepath):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    original = cv2.imread(os.path.join(dir_path, original_filepath))
    marked = cv2.imread(os.path.join(dir_path, marked_filepath))

    marked = cv2.cvtColor(marked, cv2.COLOR_BGR2RGB)

    original = original.astype(float) / 255
    marked = marked.astype(float) / 255

    is_colored = abs(original - marked).sum(2) > 0.01

    (Y, _, _) = colorsys.rgb_to_yiq(
        original[:, :, 0], original[:, :, 1], original[:, :, 2])
    (_, I, Q) = colorsys.rgb_to_yiq(
        marked[:, :, 0], marked[:, :, 1], marked[:, :, 2])

    output_image = np.zeros(original.shape)
    output_image[:, :, 0] = Y
    output_image[:, :, 1] = I
    output_image[:, :, 2] = Q
    return output_image, is_colored


def _colorize(image, marks):
    height, width, channels = image.shape
    image_size = height * width

    indices_matrix = np.arange(image_size).reshape(
        height, width, order='F').copy()
    wd = 1
    nr_of_px_in_wd = (2 * wd + 1) ** 2
    max_nr = image_size * nr_of_px_in_wd
    row_inds = np.zeros(max_nr, dtype=np.int64)
    col_inds = np.zeros(max_nr, dtype=np.int64)
    vals = np.zeros(max_nr)

    length = 0
    pixel_nr = 0

    for j in range(width):
        for i in range(height):
            if not marks[i, j]:
                window_index = 0
                window_vals = np.zeros(nr_of_px_in_wd)

                for ii in range(max(0, i - wd), min(i + wd + 1, height)):
                    for jj in range(max(0, j - wd), min(j + wd + 1, width)):
                        if ii != i or jj != j:
                            row_inds[length] = pixel_nr
                            col_inds[length] = indices_matrix[ii, jj]
                            window_vals[window_index] = image[ii, jj, 0]
                            length += 1
                            window_index += 1

                center = image[i, j, 0].copy()
                window_vals[window_index] = center
                variance = np.mean((window_vals[0:window_index + 1] - np.mean(
                    window_vals[0:window_index + 1])) ** 2)
                sigma = variance * 0.6

                mgv = min((window_vals[0:window_index + 1] - center) ** 2)
                if sigma < (-mgv / np.log(0.01)):
                    sigma = -mgv / np.log(0.01)
                if sigma < 0.000002:
                    sigma = 0.000002

                window_vals[0:window_index] = np.exp(
                    -((window_vals[0:window_index] - center) ** 2) / sigma)
                window_vals[0:window_index] = window_vals[
                                              0:window_index] / np.sum(
                    window_vals[0:window_index])
                vals[length - window_index:length] = -window_vals[
                                                      0:window_index]

            row_inds[length] = pixel_nr
            col_inds[length] = indices_matrix[i, j]
            vals[length] = 1
            length += 1
            pixel_nr += 1

    vals = vals[0:length]
    col_inds = col_inds[0:length]
    row_inds = row_inds[0:length]

    A = sparse.csr_matrix((vals, (row_inds, col_inds)), (pixel_nr, image_size))
    b = np.zeros((A.shape[0]))
    colorized = np.zeros(image.shape)
    colorized[:, :, 0] = image[:, :, 0]
    color_copy_for_nonzero = marks.reshape(image_size, order='F').copy()
    colored_inds = np.nonzero(color_copy_for_nonzero)

    for t in [1, 2]:
        cur_im = image[:, :, t].reshape(image_size, order='F').copy()
        b[colored_inds] = cur_im[colored_inds]
        new_vals = linalg.spsolve(A, b)
        colorized[:, :, t] = new_vals.reshape(height, width, order='F')

    return colorized


def postprocess(colorized):
    (R, G, B) = yiq_to_rgb(
        colorized[:, :, 0], colorized[:, :, 1], colorized[:, :, 2])
    colorizedRGB = np.zeros(colorized.shape)
    colorizedRGB[:, :, 0] = R
    colorizedRGB[:, :, 1] = G
    colorizedRGB[:, :, 2] = B

    return colorizedRGB


def colorize(original_filepath, marked_filepath, output_filepath):
    (output_image, marks) = preprocess(original_filepath, marked_filepath)
    output_image = _colorize(output_image, marks)
    output_image = postprocess(output_image)

    plt.imsave(output_filepath, output_image)


def add_background(filepath):
    image = Image.open(filepath)
    size = (300, 300)
    image.thumbnail(size, Image.ANTIALIAS)
    new = Image.new('RGBA', size, (255, 255, 255, 0))  # with alpha
    new.paste(
        image, ((int(size[0] - image.size[0]) // 2),
                int((size[1] - image.size[1]) // 2))
    )
    new.save(filepath)


async def colorize_file(params):
    log.info("Colorization has started")
    original_filename = params.get("original_filename")
    if not original_filename:
        log.error("No 'original_filename' in params")
        return

    painted_filename = params.get("painted_filename")
    if not painted_filename:
        log.error("No 'painted_filename' in params")
        return

    pure_filename = params.get("pure_filename")
    if not painted_filename:
        log.error("No 'painted_filename' in params")
        return

    file_id = params.get("file_id")
    if not file_id:
        log.error("No 'file_id' in params")
        return

    colorized_filename = generate_filename(pure_filename)
    log.info(colorized_filename)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None, colorize, original_filename, painted_filename,
        colorized_filename)

    await loop.run_in_executor(None, add_background, colorized_filename)

    await insert_file_version(filepath=colorized_filename, file_id=file_id)
    log.info("Colorization has finished")
    return original_filename
