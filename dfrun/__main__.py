import os
import shutil
import argparse
import time


def cp_with_ignore(file_name_ignore, source_dir, target_dir, ignore_path='exps'):
    """
    ignoring all files and dirs which starts with '.'
    :param file_name:
    :param top_dir:
    :return:
    """

    # file_names = os.listdir(source_dir)
    if file_name_ignore is not None:
        with open(file_name_ignore, 'r+') as f:
            ignore_files = f.readlines()
            ignore_files = [ignore_file.strip('\r').strip('\n') for ignore_file in ignore_files]
            ignore_files.append('.*')
            ignore_files.append('exps')
            if not ignore_path in ignore_files:
                ignore_files.append(ignore_path)

                # add current ignore-path into .dfignore
                f.seek(f.tell() - 1, 0)
                char_last = f.read(1)
                if char_last == '\n':
                    f.writelines(ignore_path + '\n')
                else:
                    f.writelines('\n' + ignore_path + '\n')

    else:
        ignore_files = [ignore_path, '.*', 'exps']
    # print(file_names)
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns(*ignore_files))


def _process_time_str(tic, toc):
    assert isinstance(tic, float)
    assert isinstance(toc, float)
    DAY_SECONDS = 24 * 60 * 60
    HOUR_SECONDS = 60 * 60
    MIN_SECONDS = 60

    out_str = ''
    time_spent = toc - tic
    days, left = divmod(time_spent, DAY_SECONDS)
    hours, left = divmod(left, HOUR_SECONDS)
    mins, left = divmod(left, MIN_SECONDS)
    secs = round(left)

    if days > 0:
        out_str += '%d days,' % days
    if hours > 0:
        out_str += '%d hours,' % hours
    if mins > 0:
        out_str += '%d minutes,' % mins
    if secs > 0:
        out_str += '%d seconds.' % secs

    return out_str


def wait_for_gpus(gpu_args):
    tic = time.time()

    gpu_args = [int(x) for x in gpu_args.split('x')]
    assert len(gpu_args) == 2, 'Parse gpu args error, %s' % str(gpu_args)
    gpu_num, mem_req = gpu_args
    assert gpu_num >= 1, 'gpu number must be positive'
    assert mem_req >= 1, 'memory requirement must be positive'
    try:
        import pynvml
    except:
        raise ImportError('Import gpu requirements failed.')
    pynvml.nvmlInit()
    gpus_on_machine = pynvml.nvmlDeviceGetCount()
    assert gpu_num <= gpus_on_machine, 'Device don\'t have so many gpus'

    handles = [pynvml.nvmlDeviceGetHandleByIndex(ind) for ind in range(gpus_on_machine)]
    satisfied = False

    while not satisfied:
        memoinfos = [pynvml.nvmlDeviceGetMemoryInfo(handle) for handle in handles]
        memo_free = sorted([memo.free >> 30 for memo in memoinfos], reverse=True)  ##  GB unit
        if memo_free[gpu_num - 1] >= mem_req:
            ## enough resources
            break
        else:
            toc = time.time()
            wait_time = _process_time_str(tic, toc)
            print('\rwaiting for resources: %d GPUs with %d GB memory. You have been waiting for %s' % (
                gpu_num, mem_req, wait_time), end='')
            # check every 2.5 seconds
            time.sleep(2.5)


def main():
    parser = argparse.ArgumentParser()
    parser.description = 'Gadget for DL experiments'
    parser.add_argument('--exp-dir', '-d', dest='exp_dir', help='top experiment directory', type=str, default='exps')
    parser.add_argument('--exp-name', '-n', dest='exp_name', help='experiment name', type=str, default='experiment_mmm')
    parser.add_argument('--create-ignore', '-t', dest='create_ignore', action='store_true',
                        help='if create .dfignore file in the current dir')
    parser.add_argument('--gpu', '-g', type=str, dest='gpu', help='GPU required(FORMAT: (NUM)x(Gb))')
    parser.add_argument('command', type=str, default=None, nargs=argparse.REMAINDER,
                        help='the python command line, e.g. srun -p ... python ...')

    args = parser.parse_args()

    if args.create_ignore:
        if os.path.exists('.dfignore'):
            with open('.dfignore', 'r+') as f:
                ig_list = f.readlines()
                if not ig_list[-1].endswith('\n'):
                    f.write('\n')
                ig_list = [ignore_file.strip('\r').strip('\n') for ignore_file in ig_list]

                if not args.exp_dir in ig_list:
                    f.writelines(args.exp_dir + '\n')
                if not 'exps' in ig_list:
                    f.writelines('exps\n')
        else:
            with open('.dfignore', 'w') as f:
                f.writelines(args.exp_dir + '\n')
                if not 'exps' == args.exp_dir:
                    f.writelines('exps\n')
    else:
        assert args.command is not None, "Command needed. Please refer to help."
        assert len(args.command) > 0, "Command length 0, please verify your command"

    if args.command is not None and len(args.command) > 0:
        now_dir = os.getcwd()
        print('now in dir:{}'.format(now_dir))

        ## create some dirs if not exists
        if not os.path.exists(args.exp_dir):
            os.mkdir(args.exp_dir)
        else:
            if os.path.exists('.dfignore'):
                # check & add
                with open('.dfignore') as f:
                    ignore_files = f.readlines()
                    ignore_files = [ignore_file.strip('\r').strip('\n') for ignore_file in ignore_files]

        exp_dir = os.path.join(args.exp_dir, args.exp_name)
        if os.path.exists(exp_dir):
            for _ in range(5):
                cc = input(
                    "Target experiment folder exists, please enter your command\n\'y\' for overwrite\n\'n\' for exit:")
                if cc.lower() == 'y':
                    print('Overwriting files in {}'.format(exp_dir))
                    shutil.rmtree(exp_dir)
                    break
                elif cc.lower() == 'n':
                    print('Exiting....')
                    exit()
                else:
                    if _ == 4:
                        print('Too many failing, exit.')
                        exit()
                    else:
                        print('Please enter again.')

        ## copy files to target dir
        ignore_path = os.path.join(now_dir, '.dfignore') if os.path.exists(os.path.join(now_dir, '.dfignore')) else None
        cp_with_ignore(ignore_path, now_dir, exp_dir, ignore_path=args.exp_dir)
        print('copy target dir finished: {}'.format(exp_dir))

        ## change folder into target dir
        os.chdir(exp_dir)
        print('changed dir to {}'.format(os.getcwd()))

        # wait for gpu resources
        if args.gpu:
            wait_for_gpus(args.gpu)
        command_2_run = " ".join(args.command)
        print('command starting:' + command_2_run)
        ## run target command
        os.system(command_2_run)


if __name__ == '__main__':
    main()
