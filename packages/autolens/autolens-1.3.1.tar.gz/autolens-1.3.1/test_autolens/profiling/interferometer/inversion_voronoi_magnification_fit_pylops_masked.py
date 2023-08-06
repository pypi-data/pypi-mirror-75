import time

import autolens as al
import numpy as np
from projects.lops import nufft_lop

repeats = 5

kspace_shape = 512
total_visibilities = 1000000

real_space_shape = 256
real_space_shape_2d = (real_space_shape, real_space_shape)
real_space_pixels = real_space_shape_2d[0] * real_space_shape_2d[1]
real_space_pixel_scales = 0.05
real_space_sub_size = 1
real_space_radius = 3.0
pixelization_shape_2d = (30, 30)

image_pixels = real_space_shape_2d[0] * real_space_shape_2d[1]
source_pixels = pixelization_shape_2d[0] * pixelization_shape_2d[1]

shape_data = 8 * total_visibilities
shape_preloads = total_visibilities * image_pixels * 2
shape_mapping_matrix = total_visibilities * source_pixels

total_shape = shape_data + shape_preloads + shape_mapping_matrix

print("Data Memory Use (GB) = " + str(shape_data * 8e-9))
print("PreLoad Memory Use (GB) = " + str(shape_preloads * 8e-9))
print("Mapping Matrix Memory Use (GB) = " + str(shape_mapping_matrix * 8e-9))
print("Total Memory Use (GB) = " + str(total_shape * 8e-9))
print()

# Only delete this if the memory use looks... Okay
# stop

# vis = np.ones(shape=(total_visibilities, 2))
vis = np.random.uniform(low=-5.0, high=5.0, size=(total_visibilities, 2))

visibilities = al.Visibilities.manual_1d(visibilities=vis)

uv_wavelengths = np.ones(shape=(total_visibilities, 2))
noise_map = al.Visibilities.ones(shape_1d=(total_visibilities,))

interferometer = al.Interferometer(
    visibilities=visibilities, noise_map=noise_map, uv_wavelengths=uv_wavelengths
)

print("Real space sub grid size = " + str(real_space_sub_size))
print("Real space circular mask radius = " + str(real_space_radius) + "\n")
print("pixelization shape = " + str(pixelization_shape_2d) + "\n")

lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), einstein_radius=1.6, elliptical_comps=(0.17647, 0.0)
    ),
)

pixelization = al.pix.VoronoiMagnification(shape=pixelization_shape_2d)

source_galaxy = al.Galaxy(
    redshift=1.0,
    pixelization=pixelization,
    regularization=al.reg.Constant(coefficient=1.0),
)

mask = al.Mask.circular(
    shape_2d=real_space_shape_2d,
    pixel_scales=real_space_pixel_scales,
    sub_size=real_space_sub_size,
    radius=real_space_radius,
)

masked_interferometer = al.MaskedInterferometer(
    interferometer=interferometer,
    real_space_mask=mask,
    visibilities_mask=np.full(fill_value=False, shape=visibilities.shape),
    transformer_class=al.TransformerNUFFT,
)

print("Number of points = " + str(masked_interferometer.grid.sub_shape_1d) + "\n")
print(
    "Number of visibilities = "
    + str(masked_interferometer.visibilities.shape_1d)
    + "\n"
)

start_overall = time.time()

tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])
traced_grid = tracer.traced_grids_of_planes_from_grid(grid=masked_interferometer.grid)[
    -1
]
traced_sparse_grid = tracer.traced_sparse_grids_of_planes_from_grid(
    grid=masked_interferometer.grid
)[-1]

mapper = pixelization.mapper_from_grid_and_sparse_grid(
    grid=traced_grid, sparse_grid=traced_sparse_grid, inversion_uses_border=True
)

from scipy import sparse

mapping_matrix = sparse.bsr_matrix(mapper.mapping_matrix)

import pylops
from projects.lops import nufft_lop

transformer = al.TransformerNUFFT(
    uv_wavelengths=np.ones(shape=(total_visibilities, 2)),
    grid=al.Grid.uniform(
        shape_2d=(real_space_shape, real_space_shape), pixel_scales=1.0
    ),
    real_space_mask=mask,
)

Aop = pylops.MatrixMult(mapping_matrix, dtype="complex64")
Fop = nufft_lop.NUFFT2DMasked(
    transformer=transformer,
    real_space_pixels=mask.pixels_in_mask,
    dims_fft=visibilities.shape[0],
    dtype="complex128",
)

Op = Fop * Aop

y = np.apply_along_axis(lambda args: [complex(*args)], 1, vis)

x = pylops.NormalEquationsInversion(Op=Op, Regs=None, data=y)

start = time.time()

for i in range(repeats):
    x = pylops.NormalEquationsInversion(Op=Op, Regs=None, data=y)
diff = time.time() - start
print("Time to compute transformed mapping matrices = {}".format(diff / repeats))
# print(x)
