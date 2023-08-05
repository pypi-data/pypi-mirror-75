import uuid
import random
import time
import imagesize
import logging
import json

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Union

from ..helpers import get_image_type
from instauto.api.structs import WhereToPost

logger = logging.getLogger(__name__)


@dataclass
class _PostBase:
    """Contains values that are pretty much shared across all API requests."""
    _csrftoken: str = None
    _uid: str = None  # user id
    _uuid: str = None
    delivery_class: str = 'organic'
    radio_type: str = 'wifi-none'
    is_carousel_bumped_post: str = 'False'
    container_module: str = None
    media_id: str = None

    def _create(self, **kwargs):
        """Creates an instance of the class, this method should be overwritten in the individual classes with
        arguments that are required, so it is clear which arguments are needed for which action.

        If the class has an attribute, the default value can be overwritten by providing an argument named after the
        attribute. This is probably not used often, since the default values should work for basically all cases,
        but it is nice to have the option.
        """
        for k, v in kwargs.items():
            if hasattr(self,  k):
                setattr(self, k, v)
            else:
                logger.warning("{} was sent as a keyword argument, but isn't supported.")


@dataclass
class PostUnlike(_PostBase):
    inventory_source: str = 'media_or_source'
    action = 'unlike'

    @classmethod
    def create(cls, media_id: str, **kwargs) -> "PostUnlike":
        """Instantiates a instance of the class.
        Parameters
        ----------
        media_id : str
            The media_id of the post to unlike
        kwargs
            Kwargs can be used to overwrite any of the default values.
        Returns
        -------
        PostUnlike
            The newly instantiated class instance.
        """
        i = cls()
        i._create(media_id=media_id, **kwargs)
        return i


@dataclass
class PostLike(_PostBase):
    action = 'like'

    @classmethod
    def create(cls, media_id: str, **kwargs) -> "PostLike":
        """Instantiates a instance of the class.
        Parameters
        ----------
        media_id : str
            The media_id of the post to like
        kwargs
            Kwargs can be used to overwrite any of the default values.
        Returns
        -------
        PostLike
            The newly instantiated class instance.
        """
        i = cls()
        i._create(media_id=media_id, **kwargs)
        return i


@dataclass
class PostSave(_PostBase):
    action = 'save'

    @classmethod
    def create(cls, media_id: str, **kwargs) -> "PostSave":
        """Instantiates a instance of the class.
        Parameters
        ----------
        media_id : str
            The media_id of the post to save
        kwargs
            Kwargs can be used to overwrite any of the default values.
        Returns
        -------
        PostSave
            The newly instantiated class instance.
        """
        i = cls()
        i._create(media_id=media_id, **kwargs)
        return i


@dataclass
class PostComment(_PostBase):
    idempotence_token: str = field(default_factory=lambda: str(uuid.uuid4()))  # random uuid
    comment_text: str = None
    user_breadcrumb: str = None
    action = 'save'

    @classmethod
    def create(cls, media_id: str, comment_text: str, **kwargs) -> "PostComment":
        """Instantiates a instance of the class.
        Parameters
        ----------
        media_id : str
            The media_id of the post to comment on
        comment_text : str
            The text of the comment to post, is probably limited to a certain length, haven't tested. TODO
        kwargs
            Kwargs can be used to overwrite any of the default values.
        Returns
        -------
        PostComment
            The newly instantiated class instance.
        """
        i = cls()
        i._create(media_id=media_id, comment_text=comment_text, **kwargs)
        return i


@dataclass
class PostUpdateCaption(_PostBase):
    caption_text: str = None
    usertags: str = None
    location: str = None
    action = 'edit_media'

    @classmethod
    def create(cls, media_id: str, caption_text: str, **kwargs) -> "PostUpdateCaption":
        """Instantiates a instance of the class.
        Parameters
        ----------
        media_id : str
            The media_id of the post to unlike
        caption_text : str
            The text to which the caption should be set. Probably limited, haven't tested yet. TODO
        kwargs
            Kwargs can be used to overwrite any of the default values.
        Returns
        -------
        PostUpdateCaption
            The newly instantiated class instance.
        """
        i = cls()
        i._create(media_id=media_id, caption_text=caption_text, **kwargs)
        return i


@dataclass
class PostPostLocation:
    """Contains all information about the location. This can be used to set the location tag for an Instagram post."""
    name: str = ""
    address: str = ""
    lat: str = ""
    lng: str = ""
    external_source: str = ""
    facebook_places: str = ""
    facebook_places_id: str = ""


@dataclass
class PostPostDevice:
    """Contains information about the device that is used to post the image. This defaults to the same info used in
    the DeviceProfile of the ApiClient class."""
    manufacturer: str
    model: str
    android_version: int
    android_release: str


@dataclass
class PostPostEdits:
    """Contains information about how the image was edited (zooming and positioning). Defaults to no edits."""
    crop_original_size: List[int]
    crop_center: List[float] = field(default_factory=lambda: [0.0, 0.0])
    crop_zoom: float = 1.0


@dataclass
class PostPostExtra:
    """Contains information about the image uploaded. Defaults to the actual size of the image."""
    source_width: int
    source_height: int


@dataclass
class PostPost(_PostBase):
    """Contains all information about a post, that is necessary to upload it to Instagram."""
    scene_capture_type: str = ''
    timezone_offset: str = field(default_factory=lambda: str(time.localtime().tm_gmtoff))
    media_folder: str = 'Pictures'
    source_type: str = None  #: 4 will post to your feed, 3 to your story
    device_id: str = None
    caption: str = None
    x_fb_waterfall_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    upload_id: str = field(default_factory=lambda: str(time.time()))
    location: Optional[str] = None
    suggested_venue_position: int = -1
    device: PostPostDevice = None
    edits: PostPostEdits = None
    extra: PostPostExtra = None
    is_suggested_venue: bool = False
    entity_name: str = None
    entity_length: int = None
    entity_type: str = None
    image_path: str = None
    multi_sharing: str = "-1"

    @classmethod
    def create(cls, path: Union[str, Path], source_type: WhereToPost, caption: str,
               location: Optional[PostPostLocation] = None, edits: Optional[PostPostEdits] = None,
               extra: Optional[PostPostExtra] = None, **kwargs) -> "PostPost":
        """Instantiates a instance of the class.
        Parameters
        ----------
        path : str; Path
            The location to the image that needs to be uploaded
        source_type: WhereToPost
            Specifies if the image will be posted to your feed, or the story. Story hasn't been tested. TODO
        caption : str
            The caption that goes along with the post
        kwargs
            Kwargs can be used to overwrite any of the default values.
        location
        edits
        extra
        Returns
        -------
        PostUpdateCaption
            The newly instantiated class instance.
        """
        source_type = str(source_type)
        with open(path, 'rb') as f:
            f.seek(0, 2)
            entity_length = f.tell()

        if edits is not None and extra is None:
            extra = PostPostExtra(edits.crop_original_size[0], edits.crop_original_size[1])
        elif extra is not None and edits is None:
            edits = PostPostEdits([extra.source_width, extra.source_height])
        elif extra is None and edits is None:
            size = imagesize.get(path)
            edits = PostPostEdits(size)
            extra = PostPostExtra(*size)

        image_type = get_image_type(path)

        if location:
            instance = cls(location=json.dumps(location), source_type=source_type, caption=caption,
                           edits=edits, extra=extra)
        else:
            instance = cls(source_type=source_type, caption=caption, edits=edits, extra=extra)

        entity_name = f'{instance.upload_id}_0_{random.randint(1000000000, 9999999999)}'
        instance.entity_length = entity_length
        instance.entity_name = entity_name
        instance.entity_type = f'image/{image_type}'

        instance.image_path = path

        # do not use the functionality from _BasePost, so we can warn users about using values that will be
        # overwritten later on.
        overwritten_kwargs = ['device_id', 'device', '_csrftoken', '_uid', '__uuid']
        for k, v in kwargs.items():
            if not hasattr(instance, k):
                raise NameError(f"PostPost object does not have an attribute named {k}")
            if k in overwritten_kwargs:
                logger.warning(f"{k} was provided as a keyword argument. This argument will be overwritten.")
            setattr(instance, k, v)

        return instance
