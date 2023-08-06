import psutil
from cqh_psum import conf
import logging
from argparse import Action, SUPPRESS
import os
import sys
import argparse
from prettytable import PrettyTable


logger = logging.getLogger('cqh_psum')
if not logger.handlers:
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                                                  datefmt='%y%m%d %H:%M:%S'))
    logger.addHandler(stream_handler)


class DocAction(Action):

    def __init__(self,
                 option_strings,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help=None):
        super(DocAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        # parser.print_help()
        print(self.default)
        parser.exit()


parser = argparse.ArgumentParser('cqh_psum',
                                 description='sum process memory',
                                 )

parser.register("action", "doc", DocAction)

_dir = os.path.dirname(
    os.path.abspath(__file__)
)
init_path = os.path.join(_dir, '__init__.py')


def update_d(file_path):
    d = {}
    code = open(file_path).read()
    code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, d, d)
    return d


def table_output(data_arr):
    tb = PrettyTable()
    tb.field_names = ["Name", "count", "memoery"]
    for row in data_arr:
        tb.add_row(row)
    print(tb)


file_d = update_d(file_path=init_path)
doc_content = conf.doc
level_choices = logging._nameToLevel
level_choices = [e.lower() for e in level_choices]

parser.add_argument("--level", dest='level', type=str,
                    default="info", choices=level_choices)
parser.add_argument("--name", dest='name',
                    help="filter process name", required=True)
parser.add_argument("--doc", default=doc_content, action='doc')
parser.add_argument("--exclude", dest='exclude', default='')
parser.add_argument("--version", action='version', version=file_d['__version__'])
parser.add_argument('--show', dest='show')


def main(argv=None):
    if argv is not None:
        convert_args = parser.parse_args(argv)
    else:
        convert_args = parser.parse_args()
    _inner_run(convert_args.level, convert_args.name,
               convert_args.exclude,
               convert_args.show)


def pretty(size_k):
    unit_array = ['B', 'K', 'M', 'G']
    index = 0
    unit_size = 1000
    while 1:
        if index == len(unit_array) - 1:
            break
        if size_k < unit_size:
            break
        size_k = size_k / unit_size
        index = index + 1

    return '{} {}'.format(round(size_k, 2), unit_array[index])

def parse_true(value):
    true_value_list = ["1", "1", "yes", "y", "ok"]
    return value in true_value_list

def _inner_run(level, name, exclude, show):
    """Simple program that greets NAME for a total of COUNT times."""
    logger.setLevel(getattr(logging, level.upper()))
    name_list = name.split(",")
    exclude_list = []
    is_show = parse_true(show)
    if exclude:
        exclude_list = [e.strip() for e in exclude.split(",")]
    statis_d = {}  # name -> [[process_dict, memory_info]]
    for proc in psutil.process_iter():
        """
        as_dict
        {'cwd': None, 'pid': 1, 'connections': None, 'memory_full_info': None, 'cpu_num': 0, 'nice': 0, 'cmdline': ['/usr/lib/systemd/systemd', '--switched-root', '--system', '--deserialize', '21'], 'ionice': pionice(ioclass=<IOPriority.IOPRIO_CLASS_NONE: 0>, value=0), 'cpu_affinity': [0, 1, 2, 3], 'ppid': 0, 'memory_maps': None, 'username': 'root', 'status': 'sleeping', 'open_files': None, 'num_ctx_switches': pctxsw(voluntary=55527, involuntary=1586), 'cpu_percent': 0.0, 'environ': None, 'io_counters': None, 'memory_percent': 0.053628936209154196, 'create_time': 1596423414.07, 'cpu_times': pcputimes(user=8.38, system=7.51, children_user=16894.51, children_system=2057.91, iowait=0.12), 'gids': pgids(real=0, effective=0, saved=0), 'exe': '/usr/lib/systemd/systemd', 'terminal': None, 'num_fds': None, 'threads': [pthread(id=1, user_time=8.38, system_time=7.5)], 'num_threads': 1, 'name': 'systemd', 'uids': puids(real=0, effective=0, saved=0), 'memory_info': pmem(rss=3264512, vms=195469312, shared=2142208, text=1454080, lib=0, data=152170496, dirty=0)}
        """
        d = proc.as_dict()
        # generated_by_dict_unpack: d
        cmdline = d["cmdline"]
        if d['pid'] == os.getpid():
            # 忽略当前京城
            continue
        cmdline_str = cmdline
        if isinstance(cmdline, (list, tuple)):
            cmdline = ' '.join(cmdline)
        for name_piece in name_list:
            if name_piece in cmdline:
                in_exclude = False
                for exclude_name in exclude_list:
                    if exclude_name in cmdline:
                        in_exclude = True
                        break
                if not in_exclude:
                    statis_d.setdefault(name_piece, []).append([d, proc.memory_info()])
    data_list = []  # [name, count, pretty_value]
    if not is_show:
        for name, items in statis_d.items():
            count = len(items)
            value = sum([e[1].rss for e in items])
            value = pretty(value)
            data_list.append([name, count, value])

        table_output(data_list)
    else:
        field_list = ['name','pid', 'mem' ,'cmdline', ]
        tb = PrettyTable()
        tb.field_names = field_list
        for name, items in statis_d.items():
            for inner_tuple in items:
                row = [
                    name,
                    inner_tuple[0]['pid'],
                    pretty(inner_tuple[1].rss),
                    ' '.join(inner_tuple[0]['cmdline'])
                ]
                tb.add_row(row)
        print(tb)
                


if __name__ == "__main__":
    main()
