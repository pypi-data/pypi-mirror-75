import time
import os
import tempfile
import pytest
import sys

import paramsurvey
import paramsurvey.stats
from paramsurvey.examples import sleep_worker, burn_worker


@pytest.fixture(scope="module")
def paramsurvey_init(request):
    paramsurvey.init()

    def finalize():
        # needed to get pytest multiprocessing coverage
        paramsurvey.finalize()

    request.addfinalizer(finalize)


def test_basics(paramsurvey_init):
    ncores = max(4, paramsurvey.current_core_count())

    duration = 0.1
    psets = [{'duration': duration}] * ncores * 4

    start = time.time()
    results = paramsurvey.map(sleep_worker, psets, name='simple')
    elapsed = time.time() - start
    assert elapsed > duration, 'must take at least {} time'.format(duration)

    assert [r['result']['slept'] == duration for r in results.results], 'everyone slept '+str(duration)
    assert len(results.results) == len(psets), 'one return for each pset'
    assert '_pset_id' not in results.results[0]['pset']
    assert len(results.results_flattened) == len(psets), 'one return for each pset'

    psets = psets[:ncores]
    start = time.time()
    results = paramsurvey.map(sleep_worker, psets, name='group_size 5', group_size=5)
    elapsed = time.time() - start
    assert elapsed > duration*3, 'must take at least {} time'.format(duration)

    assert [r['result']['slept'] == duration for r in results.results], 'everyone slept '+str(duration)
    assert len(results.results) == len(psets), 'one return for each pset'

    start = time.time()
    results = paramsurvey.map(burn_worker, psets, name='burn group_size 4', group_size=4)
    elapsed = time.time() - start
    assert elapsed > duration*3, 'must take at least {} time'.format(duration)

    assert [r['result']['burned'] == duration for r in results.results], 'everyone burned '+str(duration)
    assert len(results.results) == len(psets), 'one return for each pset'


def do_test_args(pset, system_kwargs, user_kwargs, raw_stats):
    # this function cannot be nested inside test_args() because nested funcs can't be pickled
    assert os.getcwd() == user_kwargs['expected_cwd'], 'chdir appears to work'
    assert 'out_subdir' in system_kwargs


def test_args(capsys, paramsurvey_init):
    chdir = tempfile.gettempdir()
    if os.getcwd() == chdir:
        # whoops
        pass

    out_func_called = False
    test_user_kwargs = {'test': 1, 'expected_cwd': chdir}
    outfile = 'foo'

    def out_func(user_ret, system_kwargs, user_kwargs):
        nonlocal out_func_called
        out_func_called = True
        user_kwargs['out_func_called'] = True
        assert user_kwargs == test_user_kwargs
        assert 'outfile' in system_kwargs
        assert system_kwargs['outfile'] == outfile

    psets = [{'duration': 0.1}] * 2

    name = 'test_args dt=0'
    results = paramsurvey.map(do_test_args, psets,
                              out_func=out_func, user_kwargs=test_user_kwargs,
                              chdir=chdir, outfile=outfile, out_subdirs=10,
                              progress_dt=0., name=name)

    assert out_func_called
    assert test_user_kwargs.get('out_func_called')
    assert len(results.results) == 2

    captured = capsys.readouterr()
    sys.stdout.write(captured.out)
    sys.stderr.write(captured.err)
    assert len(captured.err.splitlines()) >= len(psets)

    # because of progress_dt being 0., we should have at least len(psets) progress lines
    has_name = [line for line in captured.err.splitlines() if 'progress' in line and name in line]
    assert len(has_name) >= len(psets)

    # same as previous but verbose=2 instead of progress_dt=0
    name = 'test_args verbose=2'
    results = paramsurvey.map(do_test_args, psets,
                              out_func=out_func, user_kwargs=test_user_kwargs,
                              chdir=chdir, outfile=outfile, out_subdirs=10,
                              verbose=2, name=name)

    assert out_func_called
    assert test_user_kwargs.get('out_func_called')
    assert len(results.results) == 2

    captured = capsys.readouterr()
    sys.stdout.write(captured.out)
    sys.stderr.write(captured.err)
    assert len(captured.err.splitlines()) >= len(psets)

    # because of progress_dt being 0., we should have at least len(psets) progress lines
    has_name = [line for line in captured.err.splitlines() if 'progress' in line and name in line]
    assert len(has_name) >= len(psets)

    results = paramsurvey.map(do_test_args, [], name='no psets')
    assert results is None


def do_raise(pset, system_kwargs, user_kwargs, raw_stats):
    if 'raise' in pset and pset['raise']:
        raise ValueError('foo')
    return {'foo': 'bar'}


def test_worker_exception(capsys, paramsurvey_init):
    psets = [{}, {}, {}, {'raise': True}, {}, {}, {}]

    results = paramsurvey.map(do_raise, psets, name='test_worker_exception')
    assert len(results.results) == 6
    assert len(results.missing) == 1
    assert '_exception' in results.missing[0]
    assert results.progress.total == 7
    assert results.progress.finished == 6
    assert results.progress.failures == 1
    assert results.progress.exceptions == 1

    assert sum('pset' in r for r in results.results) == 6
    assert sum('result' in r for r in results.results) == 6

    captured = capsys.readouterr()
    sys.stdout.write(captured.out)
    sys.stderr.write(captured.err)

    # ray redirects stderr to stdout, while multiprocessing prints it in the worker
    # TODO: add stderr/out capture everywhere and use it here
    #assert 'Traceback ' in captured.out or 'Traceback ' in captured.err

    # the standard progress function prints this
    assert 'failures: 1' in captured.out or 'failures: 1' in captured.err


def do_nothing(pset, system_kwargs, user_kwargs, raw_stats):
    return {'foo': True}


def test_wrapper_exception(capsys, paramsurvey_init):
    psets = [{}, {'actually_raise': True}, {}, {'actually_raise': True}, {}]

    results = paramsurvey.map(do_nothing, psets, raise_in_wrapper=ValueError('test_wrapper_exception'))

    assert len(results.results) == 3
    assert len(results.missing) == 2
    assert results.progress.total == 5
    assert results.progress.finished == 3
    assert results.progress.failures == 2

    # ray and multiprocessing behave differently for 'exception'
    #assert '_exception' in results.missing[0]
    #assert results.progress.exceptions == 1

    assert sum('result' in r for r in results.results) == 3

    # XXX ray prints traceback in the worker, multiprocessing and ray local_mode prints in the parent

    captured = capsys.readouterr()
    sys.stdout.write(captured.out)
    sys.stderr.write(captured.err)
    assert 'failures: 2' in captured.out or 'failures: 2' in captured.err


def test_overlarge_pset():
    pass
