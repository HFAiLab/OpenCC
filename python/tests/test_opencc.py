from __future__ import unicode_literals

import os
from glob import glob

_this_dir = os.path.dirname(os.path.abspath(__file__))
_opencc_rootdir = os.path.abspath(os.path.join(_this_dir, '..', '..'))
_test_assets_dir = os.path.join(_opencc_rootdir, 'test', 'testcases')


def test_import():
    import ds_opencc  # noqa


def test_init_delete_converter():
    import ds_opencc

    for config in ds_opencc.CONFIGS:
        converter = ds_opencc.OpenCC(config)
        del converter


def test_conversion():
    import ds_opencc

    for inpath in glob(os.path.join(_test_assets_dir, '*.in')):
        pref = os.path.splitext(inpath)[0]
        config = os.path.basename(pref)
        converter = ds_opencc.OpenCC(config)
        anspath = '{}.{}'.format(pref, 'ans')
        assert os.path.isfile(anspath)

        with open(inpath, 'rb') as f:
            intexts = [l.strip().decode('utf-8') for l in f]
        with open(anspath, 'rb') as f:
            anstexts = [l.strip().decode('utf-8') for l in f]
        assert len(intexts) == len(anstexts)

        for text, ans in zip(intexts, anstexts):
            assert converter.convert(text) == ans, \
                'Failed to convert {} for {} -> {}'.format(pref, text, ans)
