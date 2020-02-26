# Generate GraphQL queries for mutations pertaining to digital document objects.
from trompace.exceptions import UnsupportedLanguageException, MimeTypeException
from . import StringConstant
from .templates import mutation_create, mutation_delete, mutation_link
from ..constants import SUPPORTED_LANGUAGES

ADD_MUSIC_COMPOSITION_BROAD_MATCH = '''AddMusicCompositionBroadMatch(
    from: {{identifier: "{identifier_1}" }}
    to: {{identifier: "{identifier_2}" }}
  ) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
  }}'''

REMOVE_DIGITAL_DOCUMENT_BROAD_MATCH = '''RemoveMusicCompositionBroadMatch(
    from: {{identifier: "{identifier_1}" }}
    to: {{identifier: "{identifier_2}" }}
  ) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
  }}'''

ADD_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION = '''AddDMusicCompositionExampleOfWork(
    from: {{identifier: "{identifier_1}"}}
    to: {{identifier: "{identifier_2}"}}
) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
}}'''

MERGE_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION = '''MergeMusicCompositionExampleOfWork(
    from: {{identifier: "{identifier_1}"}}
    to: {{identifier: "{identifier_2}"}}
) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
}}'''

REMOVE_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION = '''RemoveMusicCompositionExampleOfWork(
    from: {{identifier: "{identifier_1}"}}
    to: {{identifier: "{identifier_2}"}}
) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
}}'''

CREATE_DIGITAL_DOCUMENT = '''CreateMusicComposition(
        {parameters}
  ) {{
    identifier
  }}'''

UPDATE_DIGITAL_DOCUMENT = '''UpdateMusicComposition(
        {parameters}
) {{
  identifier
}}'''

DELETE_DIGITAL_DOCUMENT = '''DeleteMusicComposition(
    {parameters}
  ) {{
    identifier
  }}'''

ADD_DIGITAL_DOCUMENT_TO_CONTROL_ACTION_MUTATION = """AddActionInterfaceThingInterface (
            from: {{identifier: "{identifier_2}", type: ControlAction}}
            to: {{identifier: "{identifier_1}", type: MusicComposition}}
            field: result
        ) {{
            from {{
                __typename
            }}
            to {{
                __typename
            }}
        }}"""


def mutation_create_music_composition(title: str, contributor: str, creator: str, source: str, publisher: str,
                           language: str, inLanguage:str, formatin:str="text/html", name: str=None, description: str=None):
    """Returns a mutation for creating a music composition object
    Arguments:
        title: The title of the page from which the music composition information was extracted.      
        contributor: A person, an organization, or a service responsible for contributing the music composition to the web resource. This can be either a name or a base URL.
        creator: The person, organization or service who created the thing the web resource is about.
        source: The URL of the web resource to be represented by the node.
        language: The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr
        inLanguage: The language of the music composition. Currently supported languages are en,es,ca,nl,de,fr
        formatin: A MimeType of the format of the music composition, default is "text/html"
        name: The name of the music composition.
        description: An account of the music composition..


    Returns:
        The string for the mutation for creating the music composition.
    Raises:
        UnsupportedLanguageException if the input language or inLanguage is not one of the supported languages.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    if inLanguage not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(inLanguage)

    if "/" not in formatin:
        raise MimeTypeException(formatin)

    args = {
        "title": title,
        "publisher": publisher,
        "contributor": contributor,
        "creator": creator,
        "source": source,
        "subject": subject,
        "description": description,
        "format": formatin,
        "language": StringConstant(language.lower()),
    }
    return mutation_create(args, CREATE_DIGITAL_DOCUMENT)


def mutation_update_document(identifier: str, document_name=None, publisher=None, contributor=None, creator=None,
                             source=None, description=None, language=None):
    """Returns a mutation for updating a digital document object.
    Arguments:
        identifier: The unique identifier of the digital document.
        document_name (optional): The name of the digital document.
        publisher (optional): The person, organization or service responsible for making the artist inofrmation available.
        contributor (optional): A person, an organization, or a service responsible for contributing the artist to the web resource. This can be either a name or a base URL.
        creator (optional): The person, organization or service who created the document that the web resource is about.
        sourcer (optional): The URL of the web resource to be represented by the node.
        description (optional): An account of the artist.
        language (optional): The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr.
    Returns:
        The string for the mutation for creating the artist.
    Raises:
        Assertion error if the input language is not one of the supported languages.
    """

    return mutation_update(identifier, UPDATE_DIGITAL_DOCUMENT, document_name, publisher, contributor, creator, source,
                           description, language)


def mutation_delete_document(identifier: str):
    """Returns a mutation for deleting a digital document object based on the identifier.
    Arguments:
        identifier: The unique identifier of the digital document object.
    Returns:
        The string for the mutation for deleting the digital document object based on the identifier.
    """

    return mutation_delete(identifier, DELETE_DIGITAL_DOCUMENT)


def mutation_add_broad_match_document(from_identifier: str, to_identifier: str):
    """Returns a mutation for creating a broad match between two digital document objects.
    Arguments:
        from_identifier: The unique identifier of the digital document object from which to create the broad match.
        to_identifier: The unique identifier of the digital document object to which the broad match should be created.
    Returns:
        The string for the mutation for creating the broad match between the two documents.
    """

    return mutation_link(from_identifier, to_identifier, ADD_DIGITAL_DOCUMENT_BROAD_MATCH)


def mutation_remove_broad_match_document(from_identifier: str, to_identifier: str):
    """Returns a mutation for removing a broad match between two digital document objects.
    Arguments:
        from_identifier: The unique identifier of the digital document object from which to remove the broad match.
        to_identifier: The unique identifier of the digital document object to which the broad match should be removed.
    Returns:
        The string for the mutation for removing the broad match between the two documents.
    """

    return mutation_link(from_identifier, to_identifier, REMOVE_DIGITAL_DOCUMENT_BROAD_MATCH)


def mutation_add_digital_document_work_example_composition(document_id: str, composition_id: str):
    """Returns a mutation for adding a digital document as an exampleOf a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for adding the document as an exampleOf the composition.
    """

    return mutation_link(document_id, composition_id, ADD_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION)


def mutation_merge_digital_document_work_example_composition(document_id: str, composition_id: str):
    """Returns a mutation for merging a digital document as an exampleOf a composition.
    Merging means that the connection will be added only if it does not exist.

    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for merging the document as an exampleOf the composition.
    """

    return mutation_link(document_id, composition_id, MERGE_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION)


def mutation_remove_digital_document_work_example_composition(document_id: str, composition_id: str):
    """Returns a mutation for removing a digital document as an exampleOf a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for removing the document as an exampleOf the composition.
    """

    return mutation_link(document_id, composition_id, REMOVE_DIGITAL_DOCUMENT_WORK_EXAMPLE_COMPOSITION)


def mutation_add_digital_document_controlaction(document_id: str, controlaction_id: str):
    """Returns a mutation for adding a digital document as a subject of a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for adding the document as a subject of the composition.
    """

    return mutation_link(document_id, controlaction_id, ADD_DIGITAL_DOCUMENT_TO_CONTROL_ACTION_MUTATION)