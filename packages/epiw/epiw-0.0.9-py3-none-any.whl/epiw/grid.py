import os
import shutil
import subprocess

_resolution = 10000
_left, _bottom, _right, _top = 746100, 1458570, 1387980, 2068800


def grid(
        src_path,
        dst_path,
        field,
        query=None, left=_left, bottom=_bottom, right=_right, top=_top, resolution=_resolution
):
    tmp_path = f'{dst_path}.tmp'
    cmd = [
        'gdal_grid',
        '-q',
        '-ot', 'float32',
        '-co', 'compress=deflate',
        '-co', 'tiled=yes',
        '-zfield', field,
        '-a_srs', 'EPSG:5179',
        '-txe', str(left), str(right),
        '-tye', str(top), str(bottom),
        '-outsize', str(int((right - left) / resolution)), str(int((bottom - top) / resolution)),
        '-a', 'invdistnn:radius=999999999,max_points=3',
        src_path,
        tmp_path
    ]

    if query:
        cmd.append('-query')
        cmd.append(query)

    proc = subprocess.Popen(cmd, env=os.environ, stdin=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        raise Exception(f'Failed to run gdal_grid! proc.returncode:{proc.returncode} err:{err} cmd:{cmd}')
    shutil.move(tmp_path, dst_path)
