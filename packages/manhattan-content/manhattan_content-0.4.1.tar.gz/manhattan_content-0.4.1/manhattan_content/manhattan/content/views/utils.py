
import json

import cssutils
import flask
from manhattan.assets import Asset
from manhattan.assets.transforms.base import BaseTransform
from manhattan.assets.transforms.images import Fit, Output

__all__ = [
    'sync_image_fixtures',
    'sync_images',
    'sync_picture_fixtures'
]


def get_default_output_transform():
    """Get the default output transform for images"""

    config = flask.current_app.config

    return Output(
        format=config.get('CONTENT_IMAGE_FORMAT', 'jpg'),
        quality=config.get('CONTENT_IMAGE_QUALITY', 85),
        lossless=config.get('CONTENT_IMAGE_LOSSLESS', False)
    )

def sync_image_fixtures(snippet, soup):
    """Synchronize image fixtures in the HTML soup with the given snippet"""

    asset_mgr = flask.current_app.asset_mgr
    config = flask.current_app.config

    # The name of the variation generated to match the image in the page
    variation_name = config.get('CONTENT_VARIATION_NAME', 'image')

    # A list of image tags
    img_fixtures = soup.find_all(
        **{
            'data-ce-tag': 'img-fixture',
            'data-mh-asset-key': True
        }
    )

    # A table of assets for the snippet
    assets = snippet.assets

    # Build a list of assets to make permanent (persist) and to generate new
    # variations for (transform).
    assets_to_persist = []
    assets_to_transform = []

    for img_fixture in img_fixtures:

        # Find the image within the image fixture
        img = img_fixture.find('img')

        # Get the asset key
        asset_key = img_fixture.get('data-mh-asset-key', '').strip()

        if not asset_key:
            # No valid asset key
            continue

        # Get base and transforms
        base_transforms = json.loads(
            img_fixture.get('data-mh-base-transforms') or '[]'
        )

        # Look for local transforms
        local_transforms = []
        if img_fixture.get('data-mh-local-transforms'):
            local_transforms = json.loads(
                img_fixture['data-mh-local-transforms']
            )
            del img_fixture['data-mh-local-transforms']

        # Determine if we need to persist and/or transform the image
        asset = asset_mgr.get_temporary_by_key(asset_key)
        transform_required = False

        if asset:

            # New image
            assets_to_persist.append(asset)
            transform_required = True
            assets[asset_key] = asset

        elif asset_key in assets:

            # Existing image
            asset = Asset(assets[asset_key])

            if not base_transforms:

                # Legacy support - previously base transforms were cleared
                # from tags, we now keep them to provide support for setting
                # the initial crop/rotate values in the client side image
                # editor to match those currently applied to the image.
                base_transforms = asset.base_transforms

            if json.dumps(base_transforms) != json.dumps(asset.base_transforms):
                transform_required = True

        else:

            # Can't find a matching asset
            continue

        if transform_required:

            if not local_transforms \
                    or local_transforms[-1]['id'] != 'image.output':

                local_transforms \
                        = [get_default_output_transform().to_json_type()]

            assets_to_transform.append((
                asset,
                {
                    variation_name: [
                        BaseTransform.from_json_type(t)
                        for t in local_transforms
                    ]
                },
                [BaseTransform.from_json_type(t) for t in base_transforms]
            ))

    # Persist all new images and apply transforms to all new and modified
    # images.
    asset_mgr.persist_many(assets_to_persist)
    asset_mgr.generate_variations_for_many(
        [a[0] for a in assets_to_transform],
        {a[0].key: a[1] for a in assets_to_transform},
        {a[0].key: a[2] for a in assets_to_transform}
    )

    for img_fixture in img_fixtures:

        # Find the image within the image fixture
        img = img_fixture.find('img')

        # Get the asset key
        asset_key = img_fixture.get('data-mh-asset-key', '').strip()
        asset = assets.get(asset_key)

        if not asset:
            # Asset not in in the assets map for the snippet, ignore it.
            continue

        # Update the image src
        if not isinstance(asset, Asset):
            asset = Asset(asset)

        variation = asset.variations[variation_name]
        if not isinstance(variation, Asset):
            variation = Asset(variation)

        img['src'] = variation.url

        # Update the background image for the fixture
        style = cssutils.parseStyle(img_fixture['style'])
        style['background-image'] = f'url(\'{img["src"]}\')'
        img_fixture['style'] = style.cssText

        # Update the draft URL
        draft = asset.variations['--draft--']
        if not isinstance(draft, Asset):
            draft = Asset(draft)

        img_fixture['data-mh-draft'] = draft.url

    # Update the assets for the snippet
    snippet.assets = assets

def sync_images(snippet, soup):
    """Synchronize the <img> tags in the HTML soup with the given snippet"""

    asset_mgr = flask.current_app.asset_mgr
    config = flask.current_app.config

    # The name of the variation generated to match the image in the page
    variation_name = config.get('CONTENT_VARIATION_NAME', 'image')

    # A list of image tags
    imgs = soup.find_all('img', **{'data-mh-asset-key': True})

    # A table of assets for the snippet
    assets = snippet.assets

    # Build a list of assets to make permanent (persist) and to generate new
    # variations for (transform).
    assets_to_persist = []
    assets_to_transform = []

    for img in imgs:

        # Get the asset key
        asset_key = img.get('data-mh-asset-key', '').strip()

        if not asset_key:
            # No valid asset key
            continue

        # Get base and transforms
        base_transforms = json.loads(
            img.get('data-mh-base-transforms') or '[]'
        )

        # Get the width
        width = int(img['width'])

        # Determine if we need to persist and/or transform the image
        asset = asset_mgr.get_temporary_by_key(asset_key)
        transform_required = False

        if asset:

            # New image
            assets_to_persist.append(asset)
            transform_required = True
            assets[asset_key] = asset

        elif asset_key in assets:

            # Existing image
            asset = Asset(assets[asset_key])

            if not base_transforms:

                # Legacy support - previously base transforms were cleared
                # from tags, we now keep them to provide support for setting
                # the initial crop/rotate values in the client side image
                # editor to match those currently applied to the image.
                base_transforms = asset.base_transforms

            if json.dumps(base_transforms) != json.dumps(asset.base_transforms):
                transform_required = True

            variation = asset.variations.get(variation_name)
            if width != variation['core_meta']['image']['size'][0]:
                transform_required = True

        else:

            # Can't find a matching asset
            continue

        if transform_required:

            local_transforms = [
                Fit(width, 99999),
                get_default_output_transform()
            ]

            assets_to_transform.append((
                asset,
                {variation_name: local_transforms},
                [BaseTransform.from_json_type(t) for t in base_transforms]
            ))

    # Persist all new images and apply transforms to all new and modified
    # images.
    asset_mgr.persist_many(assets_to_persist)
    asset_mgr.generate_variations_for_many(
        [a[0] for a in assets_to_transform],
        {a[0].key: a[1] for a in assets_to_transform},
        {a[0].key: a[2] for a in assets_to_transform}
    )

    for img in imgs:

        # Get the asset key
        asset_key = img.get('data-mh-asset-key', '').strip()
        asset = assets.get(asset_key)

        if not asset:
            # Asset not in in the assets map for the snippet, ignore it.
            continue

        # Update the image src
        if not isinstance(asset, Asset):
            asset = Asset(asset)

        variation = asset.variations[variation_name]
        if not isinstance(variation, Asset):
            variation = Asset(variation)

        img['src'] = variation.url

        # Update the draft URL
        draft = asset.variations['--draft--']
        if not isinstance(draft, Asset):
            draft = Asset(draft)

        img['data-mh-draft'] = draft.url

    # Update the assets for the snippet
    snippet.assets = assets

def sync_picture_fixtures(snippet, soup):
    """Synchronize picture fixtures in the HTML soup with the given snippet"""

    asset_mgr = flask.current_app.asset_mgr
    config = flask.current_app.config

    # A list of image tags
    picture_fixtures = soup.find_all('picture', **{'data-fixture': True})

    # A table of assets for the snippet
    assets = snippet.assets

    # Build a list of assets to make permanent (persist) and to generate new
    # variations for (transform).
    assets_to_persist = []
    assets_to_transform = []

    for picture_fixture in picture_fixtures:

        # Get a list of sources for the picture
        sources = picture_fixture.find_all('source')

        if len(sources) == 0:

            # No image sources
            continue

        if not sources[0].get('data-mh-asset-key', '').strip():

            # Base version has no asset key
            continue

        # Determine the base source version
        base_source = sources[0]

        new_assets = {}
        for source in sources:

            # Get the version for the source
            version = source['data-mh-version']

            # Get the asset key
            asset_key = source.get('data-mh-asset-key', '').strip()

            if not asset_key:
                asset_key = base_source['data-mh-asset-key'].strip()

            asset_version_key = f'{version}:{asset_key}'

            # Get base and transforms
            base_transforms = json.loads(
                source.get('data-mh-base-transforms') or '[]'
            )

            # Look for local transforms
            local_transforms = json.loads(
                source.get('data-mh-local-transforms') or '[]'
            )
            del source['data-mh-local-transforms']

            asset = new_assets.get(
                asset_key,
                asset_mgr.get_temporary_by_key(asset_key)
            )
            transform_required = False

            if asset:

                # New image
                if asset not in assets_to_persist:
                    assets_to_persist.append(asset)
                    new_assets[asset_key] = asset

                transform_required = True
                assets[asset_version_key] = [asset, base_transforms]

            elif asset_version_key in assets:

                # Existing image
                asset, existing_base_transforms = assets[asset_version_key]
                asset = Asset(asset)

                if json.dumps(base_transforms) \
                        != json.dumps(existing_base_transforms):

                    transform_required = True

                assets[asset_version_key] = [asset, base_transforms]

            else:

                # Can't find a matching asset
                continue

            if transform_required:
                assets_to_transform.append((
                    asset,
                    {
                        version:
                            [
                                BaseTransform.from_json_type(t)
                                for t in base_transforms
                            ] + [
                                BaseTransform.from_json_type(t)
                                for t in local_transforms
                            ]
                    },
                    []
                ))

    # Persist all new images and apply transforms to all new and modified
    # images.
    merged_assets_to_transform = {}
    for asset_to_transform in assets_to_transform:
        key = asset_to_transform[0].key
        variations = asset_to_transform[1]

        if key not in merged_assets_to_transform:
            merged_assets_to_transform[key] = {}

        merged_assets_to_transform[key].update(variations)

    asset_mgr.persist_many(assets_to_persist)
    asset_mgr.generate_variations_for_many(
        [a[0] for a in assets_to_transform],
        merged_assets_to_transform,
        {a[0].key: a[2] for a in assets_to_transform}
    )

    for picture_fixture in picture_fixtures:

        # Get a list of sources for the picture
        sources = picture_fixture.find_all('source')

        if len(sources) == 0:

            # No image sources
            continue

        if not sources[0].get('data-mh-asset-key', '').strip():

            # Base version has no asset key
            continue

        # Determine the base source version
        base_source = sources[0]

        for source in sources:

            # Get the version for the source
            version = source['data-mh-version']

            # Get the asset key
            has_own_image = True
            asset_key = source.get('data-mh-asset-key', '').strip()

            if not asset_key:
                has_own_image = False
                asset_key = base_source['data-mh-asset-key'].strip()

            asset_version_key = f'{version}:{asset_key}'

            image_set = assets.get(asset_version_key)

            if not image_set:
                # Asset not in in the assets map for the snippet, ignore it.
                continue

            asset, _ = image_set

            # Update the image src
            if not isinstance(asset, Asset):
                asset = Asset(asset)

            # Set the source URL
            version_variation = asset.variations[version]
            if not isinstance(version_variation, Asset):
                version_variation = Asset(version_variation)

            source['srcset'] = version_variation.url

            if has_own_image:

                # Update the draft URL
                draft = asset.variations['--draft--']
                if not isinstance(draft, Asset):
                    draft = Asset(draft)

                source['data-mh-draft'] = draft.url

            if version == base_source['data-mh-version']:

                img = picture_fixture.find('img')
                img['src'] = source['srcset']

    # Update the assets for the snippet
    snippet.assets = assets
