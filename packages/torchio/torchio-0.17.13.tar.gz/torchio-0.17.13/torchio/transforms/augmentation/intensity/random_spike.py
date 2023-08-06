from typing import Tuple, Optional, Union
import torch
import numpy as np
import SimpleITK as sitk
from ....torchio import DATA, AFFINE
from ....data.subject import Subject
from .. import RandomTransform


class RandomSpike(RandomTransform):
    r"""Add random MRI spike artifacts.

    Args:
        num_spikes: Number of spikes :math:`n` presnet in k-space.
            If a tuple :math:`(a, b)` is provided, then
            :math:`n \sim \mathcal{U}(a, b) \cap \mathbb{N}`.
            Larger values generate more distorted images.
        intensity: Ratio :math:`r` between the spike intensity and the maximum
            of the spectrum.
            Larger values generate more distorted images.
        p: Probability that this transform will be applied.
        seed: See :py:class:`~torchio.transforms.augmentation.RandomTransform`.

    .. note:: The execution time of this transform does not depend on the
        number of spikes.
    """
    def __init__(
            self,
            num_spikes: Union[int, Tuple[int, int]] = 1,
            intensity: Union[float, Tuple[float, float]] = (1, 3),
            p: float = 1,
            seed: Optional[int] = None,
            ):
        super().__init__(p=p, seed=seed)
        self.intensity_range = self.parse_range(
            intensity, 'intensity_range')
        if isinstance(num_spikes, int):
            self.num_spikes_range = num_spikes, num_spikes
        else:
            self.num_spikes_range = num_spikes

    def apply_transform(self, sample: Subject) -> dict:
        random_parameters_images_dict = {}
        for image_name, image_dict in sample.get_images_dict().items():
            params = self.get_params(
                self.num_spikes_range,
                self.intensity_range,
            )
            spikes_positions_param, intensity_param = params
            random_parameters_dict = {
                'intensity': intensity_param,
                'spikes_positions': spikes_positions_param,
            }
            random_parameters_images_dict[image_name] = random_parameters_dict
            image_dict[DATA] = self.add_artifact(
                image_dict.as_sitk(),
                spikes_positions_param,
                intensity_param,
            )
            # Add channels dimension
            image_dict[DATA] = image_dict[DATA][np.newaxis, ...]
            image_dict[DATA] = torch.from_numpy(image_dict[DATA])
        sample.add_transform(self, random_parameters_images_dict)
        return sample

    @staticmethod
    def get_params(
            num_spikes_range: Tuple[int, int],
            intensity_range: Tuple[float, float],
            ) -> Tuple:
        ns_min, ns_max = num_spikes_range
        num_spikes_param = torch.randint(ns_min, ns_max + 1, (1,)).item()
        intensity_param = torch.FloatTensor(1).uniform_(*intensity_range)
        spikes_positions = torch.rand(num_spikes_param, 3).numpy()
        return spikes_positions, intensity_param.item()

    def add_artifact(
            self,
            image: sitk.Image,
            spikes_positions: np.ndarray,
            intensity_factor: float,
            ):
        array = sitk.GetArrayViewFromImage(image).transpose()
        spectrum = self.fourier_transform(array)
        shape = np.array(spectrum.shape)
        mid_shape = shape // 2
        indices = np.floor(spikes_positions * shape).astype(int)
        for index in indices:
            diff = index - mid_shape
            i, j, k = mid_shape + diff
            spectrum[i, j, k] = spectrum.max() * intensity_factor
            # If we wanted to add a pure cosine, we should add spikes to both
            # sides of k-space. However, having only one is a better
            # representation og the actual cause of the artifact in real
            # scans.
            #i, j, k = mid_shape - diff
            #spectrum[i, j, k] = spectrum.max() * intensity_factor
        result = np.real(self.inv_fourier_transform(spectrum))
        return result.astype(np.float32)
