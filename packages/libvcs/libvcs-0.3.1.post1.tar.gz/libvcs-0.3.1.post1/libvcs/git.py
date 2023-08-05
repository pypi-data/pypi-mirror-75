# -*- coding: utf-8 -*-
"""Git Repo object for libvcs.

libvcs.git
~~~~~~~~~~

From https://github.com/saltstack/salt (Apache License):

- :py:meth:`GitRepo.remote`
- :py:meth:`GitRepo.remote_get`
- :py:meth:`GitRepo.remote_set`

From pip (MIT Licnese):

- :py:meth:`GitRepo.get_url_and_revision_from_pip_url` (get_url_rev)
- :py:meth:`GitRepo.get_revision`

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import re

from . import exc
from ._compat import urlparse
from .base import BaseRepo

logger = logging.getLogger(__name__)


class GitRepo(BaseRepo):
    bin_name = 'git'
    schemes = ('git', 'git+http', 'git+https', 'git+ssh', 'git+git', 'git+file')

    def __init__(self, url, remotes=None, **kwargs):
        """A git repository.

        :param url: URL of repo
        :type url: str

        :param remotes: list of remotes in dict format::

            [{
            "remote_name": "myremote",
            "url": "https://github.com/tony/vim-config.git"
            }]
        :type remotes: list

        :param git_remote_name: name of the remote (default "origin")
        :type git_remote_name: str

        :param git_shallow: clone with ``--depth 1`` (default False)
        :type git_shallow: bool

        :param git_submodules: Git submodules that shall be updated, all if
            empty
        :type git_submodules: list

        :param tls_verify: Should certificate for https be checked (default
            False)
        :type tls_verify: bool
        """
        if 'git_remote_name' not in kwargs:
            self.git_remote_name = "origin"
        if 'git_shallow' not in kwargs:
            self.git_shallow = False
        if 'git_submodules' not in kwargs:
            self.git_submodules = []
        if 'tls_verify' not in kwargs:
            self.tls_verify = False
        BaseRepo.__init__(self, url, **kwargs)

        self.remotes = remotes

    def get_revision(self):
        """Return current revision. Initial repositories return 'initial'."""
        try:
            return self.run(['rev-parse', '--verify', 'HEAD'])
        except exc.CommandError:
            return 'initial'

    @classmethod
    def get_url_and_revision_from_pip_url(cls, pip_url):
        """
        Prefixes stub URLs like 'user@hostname:user/repo.git' with 'ssh://'.
        That's required because although they use SSH they sometimes doesn't
        work with a ssh:// scheme (e.g. Github). But we need a scheme for
        parsing. Hence we remove it again afterwards and return it as a stub.
        The manpage for git-clone(1) refers to this as the "scp-like styntax".
        """
        if '://' not in pip_url:
            assert 'file:' not in pip_url
            pip_url = pip_url.replace('git+', 'git+ssh://')
            url, rev = super(GitRepo, cls).get_url_and_revision_from_pip_url(pip_url)
            url = url.replace('ssh://', '')
        elif 'github.com:' in pip_url:
            raise exc.LibVCSException(
                "Repo %s is malformatted, please use the convention %s for"
                "ssh / private GitHub repositories."
                % (pip_url, "git+https://github.com/username/repo.git")
            )
        else:
            url, rev = super(GitRepo, cls).get_url_and_revision_from_pip_url(pip_url)

        return url, rev

    def obtain(self):
        """Retrieve the repository, clone if doesn't exist."""
        self.check_destination()

        url = self.url

        cmd = ['clone', '--progress']
        if self.git_shallow:
            cmd.extend(['--depth', '1'])
        if self.tls_verify:
            cmd.extend(['-c', 'http.sslVerify=false'])
        cmd.extend([url, self.path])

        self.info('Cloning.')
        self.run(cmd, log_in_real_time=True)

        if self.remotes:
            for r in self.remotes:
                self.error('Adding remote %s <%s>' % (r['remote_name'], r['url']))
                self.remote_set(name=r['remote_name'], url=r['url'])

        self.info('Initializing submodules.')
        self.run(['submodule', 'init'], log_in_real_time=True)
        cmd = ['submodule', 'update', '--recursive', '--init']
        cmd.extend(self.git_submodules)
        self.run(cmd, log_in_real_time=True)

    def update_repo(self):
        self.check_destination()

        if not os.path.isdir(os.path.join(self.path, '.git')):
            self.obtain()
            self.update_repo()
            return

        # Get requested revision or tag
        url, git_tag = self.url, getattr(self, 'rev', None)

        if not git_tag:
            self.debug("No git revision set, defaulting to origin/master")
            symref = self.run(['symbolic-ref', '--short', 'HEAD'])
            if symref:
                git_tag = symref.rstrip()
            else:
                git_tag = 'origin/master'
        self.debug("git_tag: %s" % git_tag)

        self.info("Updating to '%s'." % git_tag)

        # Get head sha
        try:
            head_sha = self.run(['rev-list', '--max-count=1', 'HEAD'])
        except exc.CommandError:
            self.error("Failed to get the hash for HEAD")
            return

        self.debug("head_sha: %s" % head_sha)

        # If a remote ref is asked for, which can possibly move around,
        # we must always do a fetch and checkout.
        show_ref_output = self.run(['show-ref', git_tag], check_returncode=False)
        self.debug("show_ref_output: %s" % show_ref_output)
        is_remote_ref = "remotes" in show_ref_output
        self.debug("is_remote_ref: %s" % is_remote_ref)

        # show-ref output is in the form "<sha> refs/remotes/<remote>/<tag>"
        # we must strip the remote from the tag.
        git_remote_name = self.git_remote_name
        if "refs/remotes/%s" % git_tag in show_ref_output:
            m = re.match(
                r'^[0-9a-f]{40} refs/remotes/'
                r'(?P<git_remote_name>[^/]+)/'
                r'(?P<git_tag>.+)$',
                show_ref_output,
                re.MULTILINE,
            )
            git_remote_name = m.group('git_remote_name')
            git_tag = m.group('git_tag')
        self.debug("git_remote_name: %s" % git_remote_name)
        self.debug("git_tag: %s" % git_tag)

        # This will fail if the tag does not exist (it probably has not
        # been fetched yet).
        try:
            error_code = 0
            tag_sha = self.run(
                [
                    'rev-list',
                    '--max-count=1',
                    git_remote_name + '/' + git_tag if is_remote_ref else git_tag,
                ]
            )
        except exc.CommandError as e:
            error_code = e.returncode
            tag_sha = ""
        self.debug("tag_sha: %s" % tag_sha)

        # Is the hash checkout out what we want?
        somethings_up = (error_code, is_remote_ref, tag_sha != head_sha)
        if all(not x for x in somethings_up):
            self.info("Already up-to-date.")
            return

        try:
            process = self.run(['fetch'], log_in_real_time=True)
        except exc.CommandError:
            self.error("Failed to fetch repository '%s'" % url)
            return

        if is_remote_ref:
            # Check if stash is needed
            try:
                process = self.run(['status', '--porcelain'])
            except exc.CommandError:
                self.error("Failed to get the status")
                return
            need_stash = len(process) > 0

            # If not in clean state, stash changes in order to be able
            # to be able to perform git pull --rebase
            if need_stash:
                # If Git < 1.7.6, uses --quiet --all
                git_stash_save_options = '--quiet'
                try:
                    process = self.run(['stash', 'save', git_stash_save_options])
                except exc.CommandError:
                    self.error("Failed to stash changes")

            # Pull changes from the remote branch
            try:
                process = self.run(['rebase', git_remote_name + '/' + git_tag])
            except exc.CommandError:
                # Rebase failed: Restore previous state.
                self.run(['rebase', '--abort'])
                if need_stash:
                    self.run(['stash', 'pop', '--index', '--quiet'])

                self.error(
                    "\nFailed to rebase in: '%s'.\n"
                    "You will have to resolve the conflicts manually" % self.path
                )
                return

            if need_stash:
                try:
                    process = self.run(['stash', 'pop', '--index', '--quiet'])
                except exc.CommandError:
                    # Stash pop --index failed: Try again dropping the index
                    self.run(['reset', '--hard', '--quiet'])
                    try:
                        process = self.run(['stash', 'pop', '--quiet'])
                    except exc.CommandError:
                        # Stash pop failed: Restore previous state.
                        self.run(['reset', '--hard', '--quiet', head_sha])
                        self.run(['stash', 'pop', '--index', '--quiet'])
                        self.error(
                            "\nFailed to rebase in: '%s'.\n"
                            "You will have to resolve the "
                            "conflicts manually" % self.path
                        )
                        return

        else:
            try:
                process = self.run(['checkout', git_tag])
            except exc.CommandError:
                self.error("Failed to checkout tag: '%s'" % git_tag)
                return

        cmd = ['submodule', 'update', '--recursive', '--init']
        cmd.extend(self.git_submodules)
        self.run(cmd, log_in_real_time=True)

    @property
    def remotes_get(self):
        """Return remotes like git remote -v.

        :rtype: dict of tuples
        """
        remotes = {}

        cmd = self.run(['remote'])
        ret = filter(None, cmd.split('\n'))

        for remote_name in ret:
            remotes[remote_name] = self.remote_get(remote_name)
        return remotes

    def remote_get(self, remote='origin'):
        """Get the fetch and push URL for a specified remote name.

        :param remote: the remote name used to define the fetch and push URL
        :type remote: str
        :returns: remote name and url in tuple form
        :rtype: tuple
        """
        try:
            ret = self.run(['remote', 'show', '-n', remote])
            lines = ret.split('\n')
            remote_fetch_url = lines[1].replace('Fetch URL: ', '').strip()
            remote_push_url = lines[2].replace('Push  URL: ', '').strip()
            if remote_fetch_url != remote and remote_push_url != remote:
                res = (remote_fetch_url, remote_push_url)
                return res
            else:
                return None
        except exc.LibVCSException:
            return None

    def remote_set(self, url, name='origin'):
        """Set remote with name and URL like git remote add.

        :param url: defines the remote URL
        :type url: str
        :param name: defines the remote name.
        :type name: str
        """

        url = self.chomp_protocol(url)

        if self.remote_get(name):
            self.run(['remote', 'rm', 'name'])

        self.run(['remote', 'add', name, url])
        return self.remote_get(remote=name)

    @staticmethod
    def chomp_protocol(url):
        """Return clean VCS url from RFC-style url

        :param url: url
        :type url: str
        :rtype: str
        :returns: url as VCS software would accept it
        :seealso: #14
        """
        if '+' in url:
            url = url.split('+', 1)[1]
        scheme, netloc, path, query, frag = urlparse.urlsplit(url)
        rev = None
        if '@' in path:
            path, rev = path.rsplit('@', 1)
        url = urlparse.urlunsplit((scheme, netloc, path, query, ''))
        if url.startswith('ssh://git@github.com/'):
            url = url.replace('ssh://', 'git+ssh://')
        elif '://' not in url:
            assert 'file:' not in url
            url = url.replace('git+', 'git+ssh://')
            url = url.replace('ssh://', '')
        return url
