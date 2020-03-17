# Templates for generate GraphQL queries for mutations.

# To be added EntryPoint, ControlAction, PropertyValueSpecification and Property
from trompace.exceptions import UnsupportedLanguageException
from .. import make_parameters
from . import MUTATION
from ..constants import SUPPORTED_LANGUAGES


def mutation_create(args, mutation_string: str):
    """Returns a mutation for creating an object.
    Arguments:
        args: a dictionary of arguments for the template. The fucntion calling this function is responsible for validating the arguments.

    Returns:
        The string for the mutation for creating the object.
    Raises:
        Assertion error if the input language is not one of the supported languages.
    """

    create_mutation = mutation_string.format(parameters=make_parameters(**args))
    return MUTATION.format(mutation=create_mutation)


def mutation_update(args, mutation_string: str):
    """Returns a mutation for updating an object
    Arguments:
        args: a dictionary of arguments for the template. The fucntion calling this function is responsible for validating the arguments.
    Returns:
        The string for the mutation for updating the object.
    Raises:
        Assertion error if the input language is not one of the supported languages.
    """

    create_mutation = mutation_string.format(parameters=make_parameters(**args))
    return MUTATION.format(mutation=create_mutation)


def mutation_delete(identifier: str, mutation_string: str):
    """Returns a mutation for deleting an object
    Arguments:
        identifier: The unique identifier of the object.
    Returns:
        The string for the mutation for creating the object.
    Raises:
        Assertion error if the input language is not one of the supported languages.
    """

    args = {"identifier": identifier}

    delete_mutation = mutation_string.format(parameters=make_parameters(**args))
    return MUTATION.format(mutation=delete_mutation)


def mutation_link(identifier_1: str, identifier_2: str, mutation_string: str):
    """Returns a mutation for linking two objects based on their identifiers.
    Arguments:
        identifier_1: The unique identifier of the first object.
        identifier_2: The unique identifier of the second object.
    Returns:
        The string for the mutation for the link.
    """

    broad_match_mutation = mutation_string.format(identifier_1=identifier_1, identifier_2=identifier_2)
    return MUTATION.format(mutation=broad_match_mutation)
