#! /usr/bin/env python3
#
# This file was taken from the ghp-import package.
# See https://github.com/davisp/ghp-import for more info.

import errno
import optparse as op
import os
import subprocess as sp
import sys
import time
import unicodedata

__usage__ = "%prog [OPTIONS] DIRECTORY"


def enc(text):
    if isinstance(text, bytes):
        return text
    return text.encode()

def dec(text):
    if isinstance(text, bytes):
        return text.decode('utf-8')
    return text

def write(pipe, data):
    try:
        pipe.stdin.write(data)
    except IOError as e:
        if e.errno != errno.EPIPE:
            raise


class Git(object):
    def __init__(self):
        self.cmd = None
        self.pipe = None
        self.stderr = None
        self.stdout = None

    def check_repo(self, parser):
        if self.call('rev-parse') != 0:
            error = self.stderr
            if not error:
                error = "Unknown Git error"
            error = dec(error)
            if error.startswith("fatal: "):
                error = error[len("fatal: "):]
            parser.error(error)

    # make branch point to remote/branch
    def try_rebase(self, remote, branch):
        rc = self.call('rev-list', '--max-count=1', '%s/%s' % (remote, branch))
        if rc != 0:
            return True
        rev = dec(self.stdout.strip())
        rc = self.call('update-ref', 'refs/heads/%s' % branch, rev)
        if rc != 0:
            return False
        return True

    def get_config(self, key):
        self.call('config', key)
        return self.stdout.strip()

    def get_prev_commit(self, branch):
        rc = self.call('rev-list', '--max-count=1', branch, '--')
        if rc != 0:
            return None
        return dec(self.stdout).strip()

    def open(self, *args, **kwargs):
        self.cmd = ['git'] + list(args)
        if sys.version_info >= (3, 2, 0):
            kwargs['universal_newlines'] = False
        for k in 'stdin stdout stderr'.split():
            kwargs[k] = sp.PIPE
        self.pipe = sp.Popen(self.cmd, **kwargs)
        return self.pipe

    def call(self, *args, **kwargs):
        self.open(*args, **kwargs)
        (self.stdout, self.stderr) = self.pipe.communicate()
        return self.pipe.wait()

    def check_call(self, *args, **kwargs):
        sp.check_call(['git'] + list(args), **kwargs)


def normalize_path(path):
    # Fix unicode pathnames on OS X
    # See: http://stackoverflow.com/a/5582439/44289
    if sys.platform == "darwin":
        return unicodedata.normalize("NFKC", dec(path))
    return path


def mk_when(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    currtz = time.strftime('%z')
    return "%s %s" % (timestamp, currtz)


def start_commit(pipe, git, branch, message):
    uname = dec(git.get_config("user.name"))
    email = dec(git.get_config("user.email"))
    write(pipe, enc('commit refs/heads/%s\n' % branch))
    write(pipe, enc('committer %s <%s> %s\n' % (uname, email, mk_when())))
    write(pipe, enc('data %d\n%s\n' % (len(enc(message)), message)))
    head = git.get_prev_commit(branch)
    if head:
        write(pipe, enc('from %s\n' % head))
    write(pipe, enc('deleteall\n'))


def add_file(pipe, srcpath, tgtpath):
    with open(srcpath, "rb") as handle:
        if os.access(srcpath, os.X_OK):
            write(pipe, enc('M 100755 inline %s\n' % tgtpath))
        else:
            write(pipe, enc('M 100644 inline %s\n' % tgtpath))
        data = handle.read()
        write(pipe, enc('data %d\n' % len(data)))
        write(pipe, enc(data))
        write(pipe, enc('\n'))


def gitpath(fname):
    norm = os.path.normpath(fname)
    return "/".join(norm.split(os.path.sep))


def run_import(git, srcdir, opts):
    cmd = ['git', 'fast-import', '--date-format=raw', '--quiet']
    kwargs = {
        "stdin": sp.PIPE
    }
    if sys.version_info >= (3, 2, 0):
        kwargs["universal_newlines"] = False
    pipe = sp.Popen(cmd, **kwargs)
    start_commit(pipe, git, opts.branch, opts.mesg)
    for path, dnames, fnames in os.walk(srcdir, followlinks=opts.followlinks):
        for fn in fnames:
            fpath = os.path.join(path, fn)
            fpath = normalize_path(fpath)
            gpath = gitpath(os.path.relpath(fpath, start=srcdir))
            add_file(pipe, fpath, gpath)
    write(pipe, enc('\n'))
    pipe.stdin.close()
    if pipe.wait() != 0:
        sys.stdout.write(enc("Failed to process commit.\n"))


def options():
    return [
        op.make_option('-m', '--message', dest='mesg',
            default='Update documentation',
            help='The commit message to use on the target branch.'),
        op.make_option('-r', '--remote', dest='remote', default='origin',
            help='Name of the remote. [%default]'),
        op.make_option('-b', '--branch', dest='branch', default='gh-pages',
            help='Name of the branch to write to. [%default]'),
        op.make_option('-l', '--follow-links', dest='followlinks',
            default=False, action='store_true',
            help='Follow symlinks when adding files. [%default]')
    ]


def main():
    parser = op.OptionParser(usage=__usage__, option_list=options())
    opts, args = parser.parse_args()

    if len(args) == 0:
        parser.error("No import directory specified.")

    if len(args) > 1:
        parser.error("Unknown arguments specified: %s" % ', '.join(args[1:]))

    if not os.path.isdir(args[0]):
        parser.error("Not a directory: %s" % args[0])

    git = Git()
    git.check_repo(parser)

    if not git.try_rebase(opts.remote, opts.branch):
        parser.error("Failed to rebase %s branch." % opts.branch)

    run_import(git, args[0], opts)


if __name__ == '__main__':
    main()
