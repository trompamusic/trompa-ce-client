# Generate GraphQL queries for mutations pertaining to mediaobject objects.
from trompace.exceptions import UnsupportedLanguageException, NotAMimeTypeException
from . import StringConstant, _Neo4jDate
from .templates import mutation_create, mutation_update, mutation_delete
from ..constants import SUPPORTED_LANGUAGES

CREATE_MEDIAOBJECT = '''CreateMediaObject(
        {parameters}
    ) {{
      identifier
    }}'''

UPDATE_MEDIAOBJECT = '''UpdateMediaObject(
      {parameters}
    ) {{
      identifier
    }}'''

DELETE_MEDIAOBJECT = '''DeleteMediaObject(
      {parameters}
    ) {{
      identifier
    }}'''


def mutation_create_mediaobject(creator: str, encodingFormat: str, contentUrl: str, embedUrl: str, title: str=None, source: str=None):
    """Returns a mutation for creating a media object.
    Arguments:
        creator: The person, organization or service who created the web resource pertaining to the media object.
        encodingFormat: a mime type representing the format of the encoding. 
        contentUrl: The url of the content.
        embedUrl: The url of the embeded work.
        title: The title of the page from which the person information was extracted.   
        source: The URL of the web resource to be represented by the node. Defaults to contentUrl if not provided.
    Returns:
        The string for the mutation for creating the media object.
    Raises:
        NotAMimeTypeException: If encodingFormat is not a valid mime type. 
    """


    if "/" not in encodingFormat:
        raise NotAMimeTypeException(encodingFormat)

    args = {
        "creator": creator,
        "encodingFormat": encodingFormat,
        "contentUrl": contentUrl,
        "embedUrl": embedUrl,
    }
    if title:
        args["title"] = title
    if date:
        args["source"] = source
    return mutation_create(args, CREATE_MEDIAOBJECT)


def mutation_update_mediaobject(identifier: str, encodingFormat: str=None, contentUrl: str=None, embedUrl: str=None, title: str=None, source: str=None):
    """Returns a mutation for updating a person media object based on the identifier.
    Arguments:
        identifier: The unique identifier of the media object
        creator: The person, organization or service who created the web resource pertaining to the media object.
        encodingFormat: a mime type representing the format of the encoding. 
        contentUrl: The url of the content.
        embedUrl: The url of the embeded work.
        title: The title of the page from which the person information was extracted.   
        source: The URL of the web resource to be represented by the node. Defaults to contentUrl if not provided.

    Returns:
        The string for the mutation for updating the media object.
    Raises:
        NotAMimeTypeException: If encodingFormat is not a valid mime type. 
    """
    args = {"identifier": identifier}
    if encodingFormat:
        if "/" not in encodingFormat:
            raise NotAMimeTypeException(encodingFormat)
        else: args["encodingFormat"] = encodingFormat
    if contentUrl:
        args["contentUrl"] = contentUrl
    if embedUrl:
        args["embedUrl"] = embedUrl
    if title:
        args["title"] = title
    if date:
        args["source"] = source
    return mutation_create(args, UPDATE_MEDIAOBJECT)


def mutation_delete_mediaobject(identifier: str):
    """Returns a mutation for deleting a media object based on the identifier.
    Arguments:
        identifier: The unique identifier of the media object.
    Returns:
        The string for the mutation for deleting the media object based on the identifier.
    """

    return mutation_delete(identifier, DELETE_MEDIAOBJECT)
