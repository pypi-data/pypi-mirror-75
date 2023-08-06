"""Extract regions from a raster by category."""

import time
import warnings
import concurrent.futures

import click
import numpy as np
import rasterio

import rio_terrain as rt
import rio_terrain.tools.messages as msg
from rio_terrain import __version__ as plugin_version


def do_extract(img, categorical, category):
    if category is None:
        _category = [1]
    else:
        _category = list(category)
    mask = np.isin(categorical, _category)
    result = img * mask
    return result


@click.command('extract', short_help="Extract regions by category.")
@click.argument('input', nargs=1, type=click.Path(exists=True))
@click.argument('categorical', nargs=1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path())
@click.option('-c', '--category', multiple=True, type=int, help='Category to extract.')
@click.option('-j', '--njobs', type=int, default=1, help='Number of concurrent jobs to run')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.version_option(version=plugin_version, message='rio-terrain v%(version)s')
@click.pass_context
def extract(ctx, input, categorical, output, category, njobs, verbose):
    """Extract regions from a raster by category.

    \b
    INPUT should be a single-band raster.
    CATEGORICAL should be a single-band raster with categories to extract.

    The categorical data may be the input raster or another raster.

    \b
    Example:
    rio extract diff.tif categorical.tif extract.tif -c 1 -c 3

    """
    if verbose:
        np.warnings.filterwarnings('default')
    else:
        np.warnings.filterwarnings('ignore')

    t0 = time.time()
    command = click.get_current_context().info_name

    with rasterio.open(input) as src, rasterio.open(categorical) as cat:

        if not rt.is_raster_intersecting(src, cat):
            raise ValueError(msg.NONINTERSECTING)
        if not rt.is_raster_aligned(src, cat):
            raise ValueError(msg.NONALIGNED)

        profile = src.profile
        affine = src.transform

        if njobs >= 1:
            block_shape = (src.block_shapes)[0]
            blockxsize = block_shape[1]
            blockysize = block_shape[0]
        else:
            blockxsize = None
            blockysize = None

        tiles = rt.tile_grid_intersection(src, cat, blockxsize=blockxsize, blockysize=blockysize)
        windows0, windows1, write_windows, affine, nrows, ncols = tiles

        profile.update(
            count=1,
            compress='lzw',
            bigtiff='yes',
            height=nrows,
            width=ncols,
            transform=affine,
        )

        with rasterio.open(output, 'w', **profile) as dst:
            if njobs < 1:
                click.echo((msg.STARTING).format(command, msg.INMEMORY))
                img = src.read(1, window=next(windows0))
                mask = cat.read(1, window=next(windows1))
                result = do_extract(img, mask, category)
                dst.write(result.astype(profile['dtype']), 1, window=next(write_windows))
            elif njobs == 1:
                click.echo((msg.STARTING).format(command, msg.SEQUENTIAL))
                with click.progressbar(length=nrows * ncols, label='Blocks done:') as bar:
                    for (window0, window1, write_window) in zip(windows0, windows1, write_windows):
                        img = src.read(1, window=window0)
                        mask = cat.read(1, window=window1)
                        result = do_extract(img, mask, category)
                        dst.write(result.astype(profile['dtype']), 1, window=write_window)
                        bar.update(result.size)
            else:
                click.echo((msg.STARTING).format(command, msg.CONCURRENT))

                def jobs():
                    for (window0, window1, write_window) in zip(windows0, windows1, write_windows):
                        img = src.read(1, window=window0)
                        mask = cat.read(1, window=window1)
                        yield img, mask, window0, window1, write_window

                with concurrent.futures.ThreadPoolExecutor(max_workers=njobs) as executor, \
                        click.progressbar(length=nrows * ncols, label='Blocks done:') as bar:

                    future_to_window = {
                        executor.submit(do_extract, img, mask, category): (
                            window0,
                            window1,
                            write_window,
                        )
                        for (img, mask, window0, window1, write_window) in jobs()
                    }

                    for future in concurrent.futures.as_completed(future_to_window):
                        window0, window1, write_window = future_to_window[future]
                        result = future.result()
                        dst.write(result.astype(profile['dtype']), 1, window=write_window)
                        bar.update(result.size)

    click.echo((msg.WRITEOUT).format(output))
    click.echo((msg.COMPLETION).format(msg.printtime(t0, time.time())))
