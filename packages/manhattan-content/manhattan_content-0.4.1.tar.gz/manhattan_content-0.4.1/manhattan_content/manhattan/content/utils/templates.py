
from jinja2 import Markup
from jinja2.utils import htmlsafe_json_dumps

__all__ = [
    'image_proxy',
    'image_set_proxy',
    'image_set_version',
    'image_transform'
]


def image_proxy(
    transforms,
    crop_aspect_ratio=None,
    fix_crop_aspect_ratio=False
):
    """
    Shortcut for creating data attributes for an image proxy.

    Usage:

        {{ image_proxy(
            transforms=[
                image_transform(id='fit', width=500),
                image_transform(id='output', format='webp', quality=95)
            ],
            crop_aspect_ratio=1.5,
            fixed_crop=False
        ) }}

    """

    attrs = {
        'data-mh-image-proxy': True,
        'data-mh-image-transforms': htmlsafe_json_dumps(transforms)
    }

    if crop_aspect_ratio:
        attrs['data-mh-image-crop-aspect-ratio'] = crop_aspect_ratio

    if fix_crop_aspect_ratio:
        assert crop_aspect_ratio, (
            'A fixed crop aspect ratio can only be applied if a crop aspect '
            'ratio is given.'
        )

        attrs['data-mh-image-fixed-crop'] = True

    return Markup(
        '\n'.join([
            k if v is True else '='.join([k, f"'{v}'"])
            for k, v in attrs.items()
        ])
    )

def image_set_proxy(*versions, fix_crop_aspect_ratio=False):
    """
    Shortcut for creating data attributes for an image set proxy.

    Usage:

        {{ image_set_proxy(
            image_set_version(
                version='l',
                label='Desktop',
                transforms=[
                    image_transform(id='fit', width=1000),
                    image_transform(id='output', format='webp', quality=95)
                ],
                media="(min-width: 960px)",
                crop_aspect_ratio=1.5
            ),
            image_set_version(
                version='m',
                label='Tablet',
                transforms=[
                    image_transform(id='fit', width=750),
                    image_transform(id='output', format='webp', quality=85)
                ],
                media="(min-width: 640px)",
                crop_aspect_ratio=1.333
            ),
            image_set_version(
                version='s',
                label='Mobile',
                transforms=[
                    image_transform(id='fit', width=400),
                    image_transform(id='output', format='webp', quality=75)
                ],
                media="(min-width: 320px)",
                crop_aspect_ratio=1.0
            )
            fix_crop_aspect_ratio=True
        ) }}

    """

    version_names = [v['version'] for v in versions]
    version_labels = {v['version']: v['label'] for v in versions}
    transforms = {v['version']: v['transforms'] for v in versions}
    media = {v['version']: v['media'] for v in versions}

    attrs = {
        'data-mh-image-set-proxy': True,
        'data-mh-image-set-versions': htmlsafe_json_dumps(version_names),
        'data-mh-image-set-version-labels': htmlsafe_json_dumps(version_labels),
        'data-mh-image-set-transforms': htmlsafe_json_dumps(transforms),
        'data-mh-image-set-media': htmlsafe_json_dumps(media)
    }

    crop_aspect_ratios = None
    if versions[0].get('crop_aspect_ratio'):
        crop_aspect_ratios = {
            v['version']: v['crop_aspect_ratio'] for v in versions
        }
        attrs['data-mh-image-set-crop-aspect-ratios'] = \
                htmlsafe_json_dumps(crop_aspect_ratios)

    if fix_crop_aspect_ratio:
        assert crop_aspect_ratios, (
            'A fixed crop aspect ratio can only be applied if crop aspect '
            'ratios are given.'
        )
        attrs['data-mh-image-set-fix-crop-aspect-ratio'] = True

    return Markup(
        '\n'.join([
            k if v is True else '='.join([k, f"'{v}'"])
            for k, v in attrs.items()
        ])
    )

def image_set_version(
    version,
    label,
    transforms,
    media,
    crop_aspect_ratio=None
):
    """Shortcut for defining an image version within an image set"""

    version = {
        'version': version,
        'label': label,
        'transforms': transforms,
        'media': media
    }

    if crop_aspect_ratio:
        version['crop_aspect_ratio'] = crop_aspect_ratio

    return version

def image_transform(id, **settings):
    """Shortcut for creating image transforms"""

    if '.' not in id:
        id = f'image.{id}'

    return {'id': id, 'settings': settings}

