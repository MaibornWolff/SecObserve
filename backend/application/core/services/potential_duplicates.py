from application.core.models import Observation, Potential_Duplicate


def find_potential_duplicates(observations: set[Observation]) -> None:
    if observations:
        potential_duplicate_observations = Observation.objects.filter(
            product=list(observations)[0].product,
            branch=list(observations)[0].branch,
            origin_service=list(observations)[0].origin_service,
            current_status=Observation.STATUS_OPEN,
        )

    for observation in observations:
        Potential_Duplicate.objects.filter(observation=observation).delete()
        initial_has_potential_duplicates = observation.has_potential_duplicates
        observation.has_potential_duplicates = False
        if observation.current_status == Observation.STATUS_OPEN:
            for potential_duplicate_observation in potential_duplicate_observations:
                if observation != potential_duplicate_observation:
                    potential_duplicate_type = None
                    if (
                        observation.origin_component_name
                        and potential_duplicate_observation.origin_component_name
                        and observation.title == potential_duplicate_observation.title
                    ):
                        potential_duplicate_type = (
                            Potential_Duplicate.POTENTIAL_DUPLICATE_TYPE_COMPONENT
                        )
                    if (
                        observation.origin_source_file
                        and observation.origin_source_line_start
                        and observation.origin_source_file
                        == potential_duplicate_observation.origin_source_file
                        and observation.origin_source_line_start
                        == potential_duplicate_observation.origin_source_line_start
                        and observation.scanner
                        != potential_duplicate_observation.scanner
                    ):
                        potential_duplicate_type = (
                            Potential_Duplicate.POTENTIAL_DUPLICATE_TYPE_SOURCE
                        )
                    if potential_duplicate_type:
                        Potential_Duplicate.objects.create(
                            observation=observation,
                            potential_duplicate_observation=potential_duplicate_observation,
                            type=potential_duplicate_type,
                        )
                        observation.has_potential_duplicates = True
            if observation.has_potential_duplicates != initial_has_potential_duplicates:
                observation.save()


def set_potential_duplicate_both_ways(observation: Observation) -> None:
    set_potential_duplicate(observation)

    potential_duplicate_observations = Potential_Duplicate.objects.filter(
        potential_duplicate_observation=observation
    )
    for potential_duplicate_observation in potential_duplicate_observations:
        set_potential_duplicate(potential_duplicate_observation.observation)


def set_potential_duplicate(observation: Observation) -> None:
    initial_has_potential_duplicates = observation.has_potential_duplicates

    if observation.current_status == Observation.STATUS_OPEN:
        open_potential_duplicates = Potential_Duplicate.objects.filter(
            observation=observation,
            potential_duplicate_observation__current_status=Observation.STATUS_OPEN,
        ).count()
        if open_potential_duplicates == 0:
            observation.has_potential_duplicates = False
        else:
            observation.has_potential_duplicates = True
    else:
        observation.has_potential_duplicates = False

    if initial_has_potential_duplicates != observation.has_potential_duplicates:
        observation.save()
