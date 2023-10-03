from dataclasses import dataclass

import numpy as np
import torch


@dataclass
class Patch:
    start_line: int
    end_line: int
    start_column: int
    end_column: int


def split_image_in_patches(shape, p_width, p_height) -> list[Patch]:
    patches = []
    height, width = shape
    for i in range(0, height, p_height):
        for j in range(0, width, p_width):
            patches.append(Patch(i, i + p_height, j, j + p_width))
    return patches


def get_patch_indexes(shape, probability, p_width, p_height) -> list[Patch]:
    patches = split_image_in_patches(shape, p_width, p_height)
    applied_patches = []
    for patch in patches:
        if np.random.rand() < probability:
            applied_patches.append(patch)
    return applied_patches


class PatchMasker(object):
    def __init__(self, patch_width, patch_height, probability):
        self.patch_width = patch_width
        self.patch_height = patch_height
        self.probability = probability

    def __call__(self, data):
        masked = data.clone()
        patches = get_patch_indexes(masked[0].shape, self.probability, self.patch_width, self.patch_height)
        for patch in patches:
            masked[:, patch.start_line:patch.end_line, patch.start_column:patch.end_column] = 0
        return masked
