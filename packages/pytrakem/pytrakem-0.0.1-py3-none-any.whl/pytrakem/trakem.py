import imagej
import os
from pathlib import Path
import imageio
import numpy as np
import torch
import torchfields
import shutil
import time
import sys
from pytrakem import helpers
trakem_classes = None

class TrakEM2():
    def __init__(self, fiji_path=None, affine_params={}, elastic_params={}, project_dir='/tmp/trakem', invertor_device='cpu'):
        with helpers.stdout_redirector():
            ij = imagej.init('sc.fiji:fiji:2.0.0-pre-10')

            from jnius import autoclass, cast
            import pytrakem.trakem_classes
            global trakem_classes
            trakem_classes = pytrakem.trakem_classes

        self.set_affine_params(affine_params)
        self.set_elastic_params(elastic_params)
        self.project_dir = project_dir
        Path(project_dir).mkdir(exist_ok=True)

        self.elastic_aligner = trakem_classes.ElasticLayerAlignment()
        self.affine_aligner = trakem_classes.AffineAlignment()

        loader = trakem_classes.FSLoader(self.project_dir);
        self.project = trakem_classes.Project.createNewProject(loader, False, None, False)

        self.layerset = self.project.getRootLayerSet()
        self.np_stack = None
        self.invertor_device = invertor_device

    def align(self, np_stack):
        self.import_numpy_stack(np_stack)
        self.np_stack = np_stack
        self._run_alignment()

        result = self._export_displacement_fields()

        return result

    def _run_alignment(self, affine_params=None, elastic_params=None):
        layer_range = self.layerset.getLayers();

        empty_layers = trakem_classes.Set();

        fixed_layers = trakem_classes.Set();
        fixed_layers.add(get_layer_from_set(self.layerset, 0))

        bounds = self.layerset.get2DBounds()
        self.layerset.setMinimumDimensions()

        if affine_params is None:
            affine_params = self.affine_params
        affine_params_object = self.get_affine_params_object(trakem_classes.AffineAlignment,
                                                             **affine_params)

        self.affine_aligner.exec(affine_params_object, layer_range, fixed_layers, empty_layers, bounds,
                                 False, False, None)
        self.layerset.setMinimumDimensions()

        if elastic_params is None:
            elastic_params = self.elastic_params
        elastic_params_object = self.get_elastic_params_object(trakem_classes.ElasticLayerAlignment,
                                                              **elastic_params)
        self.elastic_aligner.exec(elastic_params_object, self.project, layer_range,
                                  fixed_layers, empty_layers, bounds,
                                  False, False, None)
        self.layerset.setMinimumDimensions()

    def _export_displacement_fields(self):
        np_stack = self.np_stack
        size = np_stack.shape[-1]
        result = torch.zeros((np_stack.shape[0], 2, np_stack.shape[1], np_stack.shape[2]),
                            device=self.invertor_device)

        for i in range(self.np_stack.shape[0]):
            layer = get_layer_from_set(self.layerset, i)
            layer.recreateBuckets()
            patch = trakem_classes.AlignmentUtils.filterPatches(layer, None).toArray()[0]
            ct = patch.getFullCoordinateTransform()

            if size % 8 == 0:
                factor = 8
            elif size % 10 == 0:
                factor = 10
            else:
                factor = 2

            raw_res = torch.zeros(1, size//factor, size//factor, 2, device=self.invertor_device)

            for x in range(0, size, factor):
                for y in range(0, size, factor):
                    p = trakem_classes.Point( [x, y] )
                    p.apply( ct )
                    coord_after = p.getW()
                    raw_res[0, x//factor, y//factor, 0] = coord_after[0] - x
                    raw_res[0, x//factor, y//factor, 1] = coord_after[1] - y


            ct_res = raw_res.permute(0, 3, 2, 1).field()
            ct_res_ups = torch.nn.functional.interpolate(ct_res, scale_factor=factor).field()
            ct_res_ups = ct_res_ups.from_pixels()
            ct_res_ups = ~ct_res_ups

            final_layer_res = ct_res_ups

            result[i] = final_layer_res.squeeze(0)

        return get_np(result)

    def render_stack(self, np_stack, disp, fixed_section_id=None):
        stack_var = torch.FloatTensor(np_stack, device=self.invertor_device)
        disp_var = torch.FloatTensor(disp, device=self.invertor_device)
        aligned_np_stack = np.zeros_like(np_stack)
        inverse_to_apply = None
        if fixed_section_id is not None:
            inverse_to_apply = ~(disp_var[fixed_section_id].unsqueeze(0).field())


        for i in range(stack_var.shape[0]):
            img = stack_var[i].unsqueeze(0)
            res = disp_var[i].unsqueeze(0).field()
            if inverse_to_apply is not None:
                res = inverse_to_apply(res)
            aligned_img = res(img)

            aligned_np_stack[i] = get_np(aligned_img.squeeze())

        return aligned_np_stack

    def set_affine_params(self, affine_params):
        self.affine_params = affine_params

    def set_elastic_params(self, elastic_params):
        self.elastic_params = elastic_params

    def import_numpy_stack(self, np_stack):
        assert len(np_stack.shape) == 3
        data_dir = os.path.join(self.project_dir, "data")
        Path(data_dir).mkdir(exist_ok=True)
        spec_file_path = os.path.join(self.project_dir, "data_spec.txt")

        with open(spec_file_path, 'w') as spec_file:
            for i in range(np_stack.shape[0]):
                img_np = np_stack[i]
                file_name = '{:06d}.tiff'.format(i)
                file_path = os.path.join(data_dir, file_name)
                imageio.imsave(file_path, img_np)
                spec_file.write(f"{file_path} 0 0 {i}\n")

        self.load_data(spec_file_path)

    def clean_up(self):
        data_dir = os.path.join(self.project_dir, "data")
        shutil.rmtree(data_dir)

    def load_data(self, spec_file_path):
        loader = self.project.getLoader()
        self.layerset.setSnapshotsMode(1)
        layer = trakem_classes.Layer(self.project, 0, 1, self.layerset)
        self.layerset.add(layer)
        layer.recreateBuckets()
        task = loader.importImages(self.layerset.getNearestLayer(0),
                                   spec_file_path, " ", 1.0, 1.0, False, 1.0, 0)
        task.join()


    def get_affine_params_object(self, aligner_class,
                                 sift_initial_sigma=1.6,
                                 sift_steps=3,
                                 sift_min_octave_size=200,
                                 sift_max_octave_size=1024,
                                 sift_fd_size=4,
                                 sift_fd_bins=8,
                                 sift_rod=0.92,
                                 sift_clear_cache=True,
                                 sift_max_num_threads=8,
                                 max_epsilon=50.0,
                                 min_inlier_ratio=0.0,
                                 min_num_inliers=12,
                                 expected_model_index=0,
                                 multiple_hypotheses=True,
                                 reject_identity=False,
                                 identity_tolerance=0.0,
                                 max_num_neighbors=10,
                                 max_num_failures=3,
                                 max_num_threads=8,
                                 desired_model_index=3,
                                 regularize=True,
                                 max_interations_optimize=2000,
                                 max_plateauw_width_optimize=2000,
                                 regularizer_index=0,
                                 visualize=False,
                                 affine_lambda=0.1
                                ):
        param_affine = aligner_class.getClass().getDeclaredFields()[0].getType().newInstance()

        param_affine.ppm.sift.initialSigma = sift_initial_sigma
        param_affine.ppm.sift.steps = sift_steps
        param_affine.ppm.sift.minOctaveSize = sift_min_octave_size
        param_affine.ppm.sift.maxOctaveSize = sift_max_octave_size
        param_affine.ppm.sift.fdSize = sift_fd_size
        param_affine.ppm.sift.fdBins = sift_fd_bins
        param_affine.ppm.rod = sift_rod
        param_affine.ppm.clearCache = sift_clear_cache
        param_affine.ppm.maxNumThreadsSift = sift_max_num_threads

        param_affine.maxEpsilon = max_epsilon
        param_affine.minInlierRatio = min_inlier_ratio
        param_affine.minNumInliers = min_num_inliers
        param_affine.expectedModelIndex = expected_model_index
        param_affine.multipleHypotheses = multiple_hypotheses
        param_affine.rejectIdentity = reject_identity
        param_affine.identityTolerance = identity_tolerance
        param_affine.maxNumNeighbors = max_num_neighbors
        param_affine.maxNumFailures = max_num_failures
        param_affine.maxNumThreads = max_num_threads

        param_affine.desiredModelIndex = desired_model_index
        param_affine.regularize = regularize
        param_affine.maxIterationsOptimize = max_interations_optimize
        param_affine.maxPlateauwidthOptimize = max_plateauw_width_optimize
        param_affine.regularizerIndex = regularizer_index
        param_affine.visualize = visualize
        param_affine.__setattr__('lambda', affine_lambda) #lambda is a keyword in python

        return param_affine

    def get_elastic_params_object(self, aligner_class,
                                  layer_scale=0.5,
                                  search_radius=64,
                                  block_radius=128,
                                  resolution_spring_mesh=16,
                                  min_r=0.6,
                                  mac_curvature_r=10.0,
                                  rod_r=0.92,
                                  use_local_smoothness_filter=True,
                                  local_model_index=3,
                                  local_region_sigma=1000.0,
                                  max_local_epxilon=1.0,
                                  max_local_trust=4.0,

                                  max_num_failures=3,
                                  max_num_neighbors=1,
                                  max_num_threads=8,
                                  desired_model_index=1,
                                  max_iterations_optimize=1000,
                                  max_plateau_width_optimize=200,
                                  stiffness_spring_mesh=0.25,
                                  max_stretch_spring_mesh=2000.0,
                                  max_iterations_spring_mesh=5000,
                                  max_plateau_width_spring_mesh=200,
                                  damp_srping_mesh=0.9,
                                  use_legacy_optimizer=False
                                 ):
        param_elastic = aligner_class.getClass().getDeclaredFields()[0].getType().newInstance()

        param_elastic.layerScale = layer_scale
        param_elastic.searchRadius = search_radius
        param_elastic.blockRadius = block_radius

        param_elastic.resolutionSpringMesh = resolution_spring_mesh

        param_elastic.minR = min_r
        param_elastic.maxCurvatureR = mac_curvature_r
        param_elastic.rodR = rod_r

        param_elastic.useLocalSmoothnessFilter = use_local_smoothness_filter
        param_elastic.localModelIndex = local_model_index
        param_elastic.localRegionSigma = local_region_sigma
        param_elastic.maxLocalEpsilon = max_local_epxilon
        param_elastic.maxLocalTrust = max_local_trust

        param_elastic.isAligned = True
        param_elastic.maxNumFailures = max_num_failures
        param_elastic.maxNumNeighbors = max_num_neighbors
        param_elastic.maxNumThreads = max_num_threads

        param_elastic.desiredModelIndex = desired_model_index
        param_elastic.maxIterationsOptimize = max_iterations_optimize
        param_elastic.maxPlateauwidthOptimize = max_plateau_width_optimize

        param_elastic.stiffnessSpringMesh = stiffness_spring_mesh
        param_elastic.maxStretchSpringMesh = max_stretch_spring_mesh
        param_elastic.maxIterationsSpringMesh = max_plateau_width_spring_mesh
        param_elastic.maxPlateauwidthSpringMesh = max_plateau_width_spring_mesh
        param_elastic.dampSpringMesh = damp_srping_mesh
        param_elastic.useLegacyOptimizer = use_legacy_optimizer

        return param_elastic


def get_np(pt):
        return pt.cpu().detach().numpy()

def get_layer_from_set(layerset, i):
    layers = layerset.getLayers()
    layer = layers[i]
    return layer

def layer_to_np(layer, shape=(1000,1000)):
    px = layer.displayableList[0].getImagePlus().getProcessor().getPixels()
    px_np = np.asarray(px.tolist()).reshape(shape)
    return px_np

