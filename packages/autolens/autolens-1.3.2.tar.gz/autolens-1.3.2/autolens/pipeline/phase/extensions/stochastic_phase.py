from autoconf import conf
import autofit as af
from autogalaxy.pipeline.phase import abstract
from autogalaxy.pipeline.phase import extensions

import numpy as np

# noinspection PyAbstractClass
class StochasticPhase(extensions.ModelFixingHyperPhase):
    def __init__(
        self,
        phase: abstract.AbstractPhase,
        search,
        model_classes=tuple(),
        histogram_samples=100,
        histogram_bins=10,
    ):

        self.is_stochastic = True
        self.histogram_samples = histogram_samples
        self.histogram_bins = histogram_bins

        super().__init__(
            phase=phase,
            search=search,
            model_classes=model_classes,
            hyper_name="stochastic",
        )

    def make_model(self, instance):
        return instance.as_model(self.model_classes)

    def run_hyper(
        self,
        dataset,
        results: af.ResultsCollection,
        info=None,
        pickle_files=None,
        **kwargs,
    ):
        """
        Run the phase, overriding the search's model instance with one created to
        only fit pixelization hyperparameters.
        """

        self.results = results

        log_likelihood_cap_file = f"{conf.instance.output_path}/{self.paths.path_prefix}/{self.paths.name}/log_likelihood_cap.txt"

        try:
            with open(log_likelihood_cap_file) as f:
                log_likelihood_cap = float(f.read())
        except FileNotFoundError:
            print(results)
            print(results.last)
            log_evidences = results.last.stochastic_log_evidences(
                histogram_samples=self.histogram_samples
            )
            log_likelihood_cap = np.median(log_evidences)
            with open(log_likelihood_cap_file, "w+") as f:
                f.write(str(log_likelihood_cap))

        phase = self.make_hyper_phase(include_path_prefix=False)

        phase.settings.log_likelihood_cap = log_likelihood_cap
        phase.meta_dataset.settings.log_likelihood_cap = log_likelihood_cap
        phase.paths.tag = phase.settings.phase_no_inversion_tag

        phase.use_as_hyper_dataset = False

        phase.model = self.make_model(results.last.instance)

        # TODO : HACK

        from autogalaxy.profiles import mass_profiles as mp

        mass = af.PriorModel(mp.EllipticalPowerLaw)

        mass.centre = af.last[-1].model.galaxies.lens.mass.centre
        mass.elliptical_comps = af.last[-1].model.galaxies.lens.mass.elliptical_comps
        mass.einstein_radius = af.last[-1].model.galaxies.lens.mass.einstein_radius

        phase.model.galaxies.lens.mass = mass

        return phase.run(
            dataset,
            mask=results.last.mask,
            results=results,
            info=info,
            pickle_files=pickle_files,
        )
