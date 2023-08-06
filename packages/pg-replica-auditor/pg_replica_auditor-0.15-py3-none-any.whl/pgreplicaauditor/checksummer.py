'''Check that two tables on two databases have reasonably identical rows.
Assumes that both tables have "id" and "updated_at" columns and indexes on those columns.'''
import psycopg2
import os
from tqdm import tqdm
from colorama import Fore
import colorama
import click
import psycopg2.extras
import random
from datadiff import diff
from datetime import datetime
from multiprocessing.pool import ThreadPool
import math

colorama.init()

ROWS = 8128
VERSION = '0.15'

__version__ = VERSION
__author__ = 'Lev Kokotov <lev.kokotov@instacart.com>'


def _debug(cursor):
    '''Print the executed query in a pretty color.'''
    if os.getenv('DEBUG'):
        print(Fore.BLUE, '\b{}: '.format(cursor.connection.dsn) + cursor.query.decode('utf-8'), Fore.RESET)


def _debug2(text):
    if os.getenv('DEBUG'):
        _debug3(text)


def _debug3(text):
    print(Fore.BLUE, '\b{}'.format(text), Fore.RESET)


def connect():
    '''Connect to source and replicaination DBs.'''
    primary = psycopg2.connect(os.getenv('PRIMARY_DB_URL'))
    replica = psycopg2.connect(os.getenv('REPLICA_DB_URL'))

    return primary, replica


def _minmax(cursor, table):
    assert table is not None

    cursor.execute('SELECT MIN(id) AS "min", MAX(id) as "max" FROM {}'.format(table))
    _debug(cursor)

    result = cursor.fetchone()

    return result['min'], result['max']


def _get(cursor, table, id_):
    assert id_ is not None
    assert table is not None

    query = 'SELECT * FROM {table} WHERE id = %s LIMIT 1'.format(table=table)

    cursor.execute(query, (id_,))
    _debug(cursor)

    return cursor.fetchone()


def _exec(cursor, query, params=tuple()):
    cursor.execute(query, params)
    _debug(cursor)

    return cursor


def _pick(cursor, table, mi, ma):
    assert mi is not None
    assert ma is not None

    result = None
    attempts = 0
    ids = []

    while result is None and attempts < 3:
        id_ = random.randint(mi, ma)
        result = _get(cursor, table, id_)
        attempts += 1
        ids.append(id_)

    return result, ids


def _result(checked, skipped):
    print(Fore.GREEN, '\bChecked: {}'.format(checked), Fore.RESET)
    print(Fore.GREEN, '\bSkipped: {}'.format(skipped), Fore.RESET)


def _result2(text):
    print(Fore.GREEN, '\b{}'.format(text), Fore.RESET)


def _error(p, r):
    id_ = p['id']
    print(Fore.RED, '\bRows at id = {} are different'.format(id_), Fore.RESET)
    print(diff(p, r))
    _debug2('primary: {}'.format(p))
    _debug2('replica: {}'.format(r))
    if os.getenv('EXIT_ON_ERROR'):
        exit(1)


def _error2(text):
    print(Fore.RED, '\b{}'.format(text), Fore.RESET)
    if os.getenv('EXIT_ON_ERROR'):
        exit(1)


def _announce(name, table):
    print(Fore.YELLOW, '\bRunning check "{}" on table "{}"'.format(name, table), Fore.RESET)


def _check_if_empty(cursor, table):
    cursor.execute("SELECT * FROM {} LIMIT 1".format(table))
    return cursor.fetchone() is None


def randcheck(primary, replica, table, rows, show_skipped):
    '''Check rows at random.'''
    _announce('random check', table)
    rmin, rmax = _minmax(primary, table)

    checked = 0
    skipped = 0
    for _ in tqdm(range(rows)):
        p, attempts = _pick(primary, table, rmin, rmax)
        if p is None:
            skipped += 1
            if show_skipped:
                _debug3('Skipped: {}'.format(', '.join(map(lambda x: str(x), attempts))))
            continue
        r = _get(replica, table, p['id'])
        if r is None:
            _error2('Row does not exist on replica at id = {}'.format(p['id']))
        else:
            assert r['id'] == p['id'] # Kind of obvious, but let's not leave anything out
            _debug2('Comparing id = {}'.format(r['id']))
            if dict(p) != dict(r):
                _error(dict(p), dict(r))
            checked += 1
    _result(checked, skipped)


def last_1000(primary, replica, table, show_skipped):
    _announce('last 1000', table)
    _, rmax = _minmax(primary, table)
    rmin = rmax - 1000

    checked = 0
    skipped = 0
    for id_ in tqdm(range(rmin, rmax)):
        p = _get(primary, table, id_)
        r = _get(replica, table, id_)
        if p is None or r is None:
            skipped += 1
            if show_skipped:
                _debug3('Skipped: {}'.format(id_))
            continue
        assert p['id'] == r['id']
        if dict(p) != dict(r):
            _error(dict(p), dict(r))
        checked += 1
    _result(checked, skipped)


def lag(primary, replica, table, column='updated_at'):
    '''Check logical lag between primary and replica table using Django/Rails "updated_at".'''
    _announce('replica lag', table)
    query = 'SELECT MAX({column}) AS "max" FROM "{table}"'.format(column=column, table=table)
    primary = _exec(primary, query)
    replica = _exec(replica, query)
    p = primary.fetchone()['max']
    r = replica.fetchone()['max']

    # Table is empty, so no lag is possible.
    if p is None and r is None:
        _result2('0')
    elif r is None:
        _error2('Replica has no rows / no values in "{}" column'.format(column))
    else:
        _result2(p - r)


def minmax(primary, replica, table):
    '''Check MIN(id) and MAX(id) match between primary and replica.'''
    _announce('minmax', table)
    pmin, pmax = _minmax(primary, table)
    rmin, rmax = _minmax(replica, table)

    if rmin != pmin:
        _error2('Minimum does not match. replica: {}, primary: {}'.format(rmin, pmin))
    elif rmax != pmax:
        _error2('Maximum does not match. replica: {}, primary: {}'.format(rmax, pmax))
    else:
        _result2('replica: {}/{}'.format(rmin, rmax))
        _result2('primary: {}/{}'.format(pmin, pmax))



def bulk_1000_sum(primary, replica, table):
    '''Check that two databases have the same ids in blocks of 1000.
    Assuming Postgres is good at retrieving adjacent blocks, this should be a fast checksum.'''
    _announce('bulk 1000 sum', table)
    rmin, rmax = _minmax(replica, table)
    blocks = max(round(rmax / 1000), 1) # Never have 0 here if not enough rows
    for _ in tqdm(range(1000)):
        block = random.randint(1, blocks)
        query = 'SELECT SUM(id::bigint) AS "sum" FROM {} WHERE id > %s AND id < %s'.format(table)
        gt = block * 1000
        lt = gt + 1000
        psum = _exec(primary, query, (gt, lt)).fetchone()['sum']
        rsum = _exec(replica, query, (gt, lt)).fetchone()['sum']
        _debug2('primary: {}'.format(psum))
        _debug2('replica: {}'.format(rsum))

        if psum != rsum:
            _error2('Sum failed at id = ({}, {}), psum = {}, rsum = {}'.format(lt, gt, psum, rsum))
    _result2('OK')


def slow_count_all_rows(primary, replica, table, column, before = datetime.now()):
    '''Sum the number of rows in a table. This will be very slow if the table is large.'''
    _announce('slow count all rows', table)

    if column != 'id':
        _error2('Slow check is only supported on the primary key = "id" for now. Sorry about that :/')
        return
    try:
        int(before)
    except TypeError:
        _error2('Slow check only supports integer columns. Please specifiy --count-before=<integer>')
        return

    query = 'SET statement_timeout = 0; SELECT COUNT({}) AS "count", SUM({}) AS "sum" FROM {} WHERE {} <= %s'.format(column, column, table, column)

    ppool = ThreadPool(processes=1)
    rpool = ThreadPool(processes=1)

    presult = ppool.apply_async(_exec, (primary, query, (before,)))
    rresult = rpool.apply_async(_exec, (replica, query, (before,)))

    p = presult.get().fetchone()
    r = rresult.get().fetchone()

    if p['count'] != r['count']:
        _error2('Count failed with replica = {} and primary = {}'.format(r['count'], p['count']))
    elif p['sum'] != r['sum']:
        _error2('Sum failed with replica = {} and primary = {}'.format(r['sum'], p['sum']))
    else:
        _result2('{} rows, {} total sum'.format(r['count'], p['count']))


def find_missing_seq_records(primary, replica, table, step_size):
    '''This assumes that a sequential chunk of records will be missing or not updated,
    we will hit one of those records.'''
    _announce('find missing records', table)
    pmin, pmax = _minmax(primary, table)
    range_ = pmax - pmin
    step_size = round(range_ * step_size)
    try:
        steps = round(range_ / step_size)
    except ZeroDivisionError:
        _error2('Not enough rows to run this test.')
        return

    for step in tqdm(range(steps)):
        id_ = pmin + step * step_size
        r = _get(replica, table, id_)
        p = _get(primary, table, id_)
        if not r and p:
            _error2('Row does not exist on replica at id = {}'.format(id_))
            return
        if p != r:
           _error(p, r)
           return
    _result2('OK')


def check_one_row(primary, replica, table, row_id):
    '''Just check one row...'''
    _announce('one row check', table)
    r = _get(replica, table, row_id)
    p = _get(primary, table, row_id)

    if p is None:
        _error2('Row does not exist on the primary.')
    elif r is None:
        _error2('Row does not exist on the replica.')
    elif p != r:
        _error(p, r)
    else:
        _result2('OK.')


def main(table, rows, exclude_tables, lag_column, show_skipped, count_before, step_size, row_id, slow_check):
    print(Fore.CYAN, '\b=== Welcome to the Postgres auditor v{} ==='.format(VERSION), Fore.RESET)
    print()

    pconn, rconn = connect()

    primary = pconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    replica = rconn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    _debug2('Primary: {}'.format(primary.connection.dsn))
    _debug2('Replica: {}'.format(replica.connection.dsn))
    if table:
        tables = [table]
        _debug2('Checking table "{}"'.format(table))
    else:
        _debug2('Checking all tables in schema "public"')
        tables = map(lambda t: t['table_name'],
            _exec(replica, "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'").fetchall())


    for table in tables:
        if table in exclude_tables:
            continue
        # Skip pg_stat_statements obviously
        if table == 'pg_stat_statements':
            continue
        # So you found the one, eh? <3
        if row_id:
            check_one_row(primary, replica, table, row_id)
            print()
            return

        # Stop checking empty tables, it breaks my math
        pempty = _check_if_empty(primary, table)
        rempty = _check_if_empty(replica, table)

        if pempty and rempty:
            _result2('Skipping empty table "{}"'.format(table))
            continue
        elif pempty and not rempty:
            _error2('"{}" is empty on the primary but has rows on the replica.'.format(table))
            continue
        elif not pempty and rempty:
            _error2('"{}" has rows on the primary but is empty on the replica.'.format(table))
            continue

        lag(primary, replica, table, lag_column)
        print()
        last_1000(primary, replica, table, show_skipped)
        print()
        minmax(primary, replica, table)
        print()
        find_missing_seq_records(primary, replica, table, step_size)
        print()
        randcheck(primary, replica, table, rows, show_skipped)
        print()
        bulk_1000_sum(primary, replica, table)
        print()
        if slow_check:
            slow_count_all_rows(primary, replica, table, lag_column, count_before)
            print()


@click.command()
@click.option('--primary', required=True, help='DSN of the primary.')
@click.option('--replica', required=True, help='DSN of the replica.')
@click.option('--table', required=False, help='Scan this table only.')
@click.option('--debug/--release', default=False, help='Print debug information as we go along.')
@click.option('--rows', default=ROWS, help='Number of rows to sample in the randcheck.')
@click.option('--exclude-tables', default='', help='Exclude these tables (comma separated) from the check.')
@click.option('--lag-column', default='updated_at', help='Use this column to compute replica lag.')
@click.option('--show-skipped/--hide-skipped', default=False, help='Print skipped IDs for debugging.')
@click.option('--count-before', default=datetime.now(), help='Count rows that were created/updated before this timestamp.')
@click.option('--exit-on-error/--continue-on-error', default=True, help='Exit immediately when possible error condition found.')
@click.option('--step-size', default=0.0001, help='The size of the search step for find missing sequential records test.')
@click.option('--row-id', default=None, help='Compare this specific row given id.')
@click.option('--slow-check/--no-slow-check', default=True, help='Run/Do not run the slow check that counts and sums all rows.')
def checksummer(primary, replica, table, debug, rows, exclude_tables, lag_column, show_skipped, count_before, exit_on_error, step_size, row_id, slow_check):
    os.environ['REPLICA_DB_URL'] = replica
    os.environ['PRIMARY_DB_URL'] = primary

    if debug:
        os.environ['DEBUG'] = 'True'
    if exit_on_error:
        os.environ['EXIT_ON_ERROR'] = 'True'

    main(table, rows, exclude_tables.split(','), lag_column, show_skipped, count_before, step_size, row_id, slow_check)

