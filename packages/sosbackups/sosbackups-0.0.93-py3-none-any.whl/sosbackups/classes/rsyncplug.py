# -*- coding: utf-8 -*-
"""rsync plugin"""

__author__  = "Adrien DELLE CAVE <adc@doowan.net>"
__license__ = """
    Copyright (C) 2018  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import abc
import copy
import gc
import logging
import os
import re
import shutil
import traceback
import time
import six

import shellescape

from dwho.classes.inoplugs import DWhoInoEventPlugBase

from pyinotify import IN_DELETE # pylint: disable-msg=no-name-in-module
from sonicprobe import helpers

import subprocess32 as subprocess

from sosbackups.plugins.sbcronsync import DATE_FORMAT, DEFAULT_STATS


DEFAULT_TIMEOUT         = 90
LOG                     = logging.getLogger('sosbackups.classes.rsync')
_MATCH_STATS_NB_FILES   = re.compile(r'^Number of files: (?P<total>[0-9]+)( \(reg: (?P<files>[0-9]+), dir: (?P<dirs>[0-9]+)\))?$').match
_MATCH_STATS_TOTAL_SIZE = re.compile(r'^Total file size: (?P<size>[0-9,]+) bytes$').match


class SosBackupsRsyncPlug(DWhoInoEventPlugBase):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def PLUGIN_NAME(self):
        return

    # pylint: disable-msg=attribute-defined-outside-init
    def init(self, config):
        DWhoInoEventPlugBase.init(self, config)

        self.last_gc                = time.time()

        self.cfg_path               = None
        self.event                  = None
        self.filepath               = None
        self.proc                   = None

        self.nb_retries             = 0
        self.nb_conn_retries        = 0
        self.rsync_max_retries      = 0
        self.rsync_max_conn_retries = 0
        self.rsync_timeout          = None
        self.rsync_path             = 'rsync'
        self.remote_rsync_path      = 'rsync'
        self.rsync_args             = []
        self.prefix_path            = self.config['inotify'].get('prefix_path')
        self.with_stats             = False

        if 'rsync' in self.config['inotify']:
            self.rsync_max_retries      = int(self.config['inotify']['rsync'].get('max_retries') or 0)
            self.rsync_max_conn_retries = int(self.config['inotify']['rsync'].get('max_conn_retries') or 0)
            self.rsync_timeout          = self.config['inotify']['rsync'].get('timeout')
            self.rsync_path             = self.config['inotify']['rsync'].get('bin_path') or 'rsync'
            self.remote_rsync_path      = self.config['inotify']['rsync'].get('remote_bin_path') or 'rsync'
            self.rsync_args             = self.config['inotify']['rsync'].get('args')

    def get_event_params(self):
        if hasattr(self.event, 'plugins') \
           and isinstance(self.event.plugins, dict) \
           and self.PLUGIN_NAME in self.event.plugins:
            return self.event.plugins[self.PLUGIN_NAME].copy()

        return {}

    def _get_rsync_params(self, params, filepath):
        bin_path         = self.rsync_path
        remote_bin_path  = self.remote_rsync_path
        args             = list(self.rsync_args)
        max_retries      = self.rsync_max_retries
        max_conn_retries = self.rsync_max_conn_retries
        timeout          = self.rsync_timeout
        to_delete        = (self.event.mask & IN_DELETE) != 0

        if params.get('dest'):
            dest = params['dest']
        else:
            if 'prefix_path' in params:
                prefix_path = params['prefix_path']
            else:
                prefix_path = self.prefix_path

            dest = self.realdstpath(self.event, filepath, prefix_path)

        if 'rsync' in params:
            if params['rsync'].get('bin_path'):
                bin_path = params['rsync']['bin_path']

            if params['rsync'].get('remote_bin_path'):
                remote_bin_path = params['rsync']['remote_bin_path']

            if 'args' in params['rsync']:
                args += params['rsync']['args']

            if 'max_retries' in params['rsync']:
                max_retries = int(params['rsync']['max_retries'])

            if 'max_conn_retries' in params['rsync']:
                max_conn_retries = int(params['rsync']['max_conn_retries'])

            if 'timeout' in params['rsync']:
                timeout = params['rsync']['timeout']

        destdir   = os.path.dirname(dest)

        if params.get('host'):
            if not to_delete:
                args += ['--rsync-path', "mkdir -p %s && %s"
                         % (shellescape.quote(destdir),
                            shellescape.quote(remote_bin_path))]
            else:
                dest  = destdir
                args += ['--delete-after',
                         '--existing',
                         '--ignore-existing',
                         '--rsync-path',
                         remote_bin_path]

                if self.event.dir:
                    dest     = os.path.dirname(destdir)
                    filepath = os.path.dirname(filepath.rstrip(os.path.sep)) + os.path.sep
                else:
                    filepath = os.path.dirname(filepath) + os.path.sep

            destarg = "%s:%s" % (params['host'], dest)
        else:
            destarg = dest

            if to_delete:
                if os.path.exists(dest):
                    if self.event.dir:
                        shutil.rmtree(dest, True)
                    elif not os.path.isdir(dest):
                        os.unlink(dest)
                return None

            if not os.path.exists(filepath):
                return None

            if not os.path.isdir(destdir):
                helpers.make_dirs(destdir)

        if self.with_stats:
            args += ['--stats']

        args += ['-s']

        return {'max_retries':      max_retries,
                'max_conn_retries': max_conn_retries,
                'timeout':          timeout,
                'args':             [bin_path] + args,
                'filepath':         filepath,
                'destarg':          destarg}

    def _run_process(self, opts, retry_args):
        args = opts['args'] + retry_args + [opts['filepath'], opts['destarg']]

        LOG.debug("rsync cmd: %r", " ".join(args))
        self.proc = subprocess.Popen(args, # pylint: disable-msg=no-member
                                     stdout = subprocess.PIPE, # pylint: disable-msg=no-member
                                     stderr = subprocess.PIPE, # pylint: disable-msg=no-member
                                     universal_newlines = True)

        (stdout, stderr)       = self.proc.communicate(timeout = opts['timeout'])
        returncode             = self.proc.returncode
        self._kill_process()
        (nb_files, total_size) = (None, None)

        stats_matched          = 0

        if stderr:
            stderr = stderr.splitlines()

        if not stdout:
            return (returncode, stderr, nb_files, total_size)

        for x in stdout.splitlines():
            if not x:
                continue
            elif not self.with_stats:
                continue

            m = _MATCH_STATS_NB_FILES(x)
            if m:
                stats_matched = 1
                nb_files      = m
            elif stats_matched:
                m = _MATCH_STATS_TOTAL_SIZE(x)
                if m:
                    stats_matched = 2
                    total_size    = m

        return (returncode, stderr, nb_files, total_size)

    def _close_fds_process(self):
        if not self.proc:
            return

        try:
            if self.proc.stdout:
                self.proc.stdout.close()
        except Exception:
            pass

        try:
            if self.proc.stderr:
                self.proc.stderr.close()
        except Exception:
            pass

    def _kill_process(self):
        if not self.proc:
            return

        self._close_fds_process()

        try:
            self.proc.terminate()
        except OSError:
            pass

        self.proc = None

    def _process_failed(self, filepath, returncode, stderr, opts, error):
        errors = {'error':    error,
                  'filepath': filepath,
                  'stderr':   stderr}

        if returncode in (3, 23):
            if not os.path.exists(filepath):
                LOG.warning("file deleted before synchronization. (path: %r)", filepath)
                return False
            if errors['stderr']:
                err = []
                for x in errors['stderr']:
                    if not x.startswith("Time value of "):
                        err.append(x)
                if len(err) < 2:
                    return False
                errors['stderr'] = err
        elif returncode == 24:
            LOG.debug("vanished source file. (path: %r)", filepath)
            if self.nb_retries < opts['max_retries']:
                self.nb_retries += 1
                LOG.warning("retrying %d/%d caused by vanished source file.",
                            self.nb_retries,
                            opts['max_retries'])
                return None
        elif returncode and returncode > 0 and errors['stderr']:
            for x in errors['stderr']:
                if not x.lower().find("connection reset by peer"):
                    continue
                if self.nb_conn_retries < opts['max_conn_retries']:
                    self.nb_conn_retries += 1
                    LOG.warning("retrying %d/%d caused by connection error.",
                                self.nb_conn_retries,
                                opts['max_conn_retries'])
                    time.sleep(0.5)
                    return None

        if errors['stderr']:
            for x in errors['stderr']:
                LOG.error(x)

        if self.nb_retries < opts['max_retries']:
            self.nb_retries += 1
            LOG.warning("retrying %s/%s caused by %s.", self.nb_retries, opts['max_retries'], error)
        else:
            LOG.exception(error)
            return errors

        return None

    def exec_rsync(self, params, filepath, set_state = False):
        if self.last_gc + DEFAULT_TIMEOUT >= time.time():
            gc.collect()
            self.last_gc = time.time()

        if self.event.dir:
            filepath += os.path.sep

        (errors,
         returncode,
         stderr,
         nb_files,
         total_size) = (None,
                        None,
                        None,
                        None,
                        None)

        if getattr(self.event, 'meta', None) is True:
            return (errors, nb_files, total_size)

        opts                 = self._get_rsync_params(params, filepath)
        self.nb_retries      = 0
        self.nb_conn_retries = 0
        retry_args           = []

        if not opts:
            return (errors, nb_files, total_size)

        while True:
            try:
                errors       = None
                (returncode,
                 stderr,
                 nb_files,
                 total_size) = self._run_process(opts, retry_args)
                if returncode:
                    raise subprocess.CalledProcessError(returncode, opts['args'][0]) # pylint: disable-msg=no-member
                break
            except Exception:
                self._kill_process()
                retry_args = []
                errors     = self._process_failed(filepath,
                                                  returncode,
                                                  stderr,
                                                  opts,
                                                  traceback.format_exc())
                if errors or errors is False:
                    break

        if set_state:
            self._set_state(filepath, errors, nb_files, total_size)

        return (errors, nb_files, total_size)

    def try_exec_rsync(self, params, filepath, set_state = True):
        (errors, nb_files, total_size) = (None, None, None)

        try:
            (errors,
             nb_files,
             total_size) = self.exec_rsync(params, filepath, False)
        except Exception as e:
            errors = {'error':    traceback.format_exc(),
                      'filepath': filepath,
                      'stderr':   repr(e)}
            LOG.exception(e)

        if set_state:
            self._set_state(filepath, errors, nb_files, total_size)

        return errors

    def _set_state(self, filepath, errors = None, nb_files = None, total_size = None):
        if not hasattr(self.event, 'state') or not self.with_stats:
            return

        if self.event.dir:
            filetype = 'directory'
        else:
            filetype = 'file'

        state = {'errors':    [],
                 'filepath':  filepath,
                 'filetype':  filetype,
                 'logged_at': time.strftime(DATE_FORMAT),
                 'stats':     copy.deepcopy(DEFAULT_STATS)}

        if not errors:
            status = 'success'
        else:
            status = 'failure'
            state['errors'].append({'error':  errors['error'],
                                    'filepath': errors['filepath'],
                                    'logged_at': time.strftime(DATE_FORMAT),
                                    'stderr': errors['stderr']})

        state['status'] = status

        if nb_files:
            dirs = files = total = int(nb_files.group('total'))

            if nb_files.group('files') is not None:
                files = int(nb_files.group('files'))

            if nb_files.group('dirs') is not None:
                dirs = int(nb_files.group('dirs'))

            state['stats']['files'][status] += int(files)
            state['stats']['dirs'][status]  += int(dirs)
            state['stats']['total'][status] += total
            state['stats']['total']['sum']  += total
        else:
            state['stats']['total'][status] += 1

        if total_size:
            total_size = int(total_size.group('size').replace(',', ''))
            state['stats']['files']['size'] += total_size
            state['stats']['total']['size'] += total_size

        self.event.state[self.PLUGIN_NAME] = state

    @abc.abstractmethod
    def run(self):
        """Do the action."""

    def __call__(self, cfg_path, event, filepath):
        self.cfg_path = cfg_path
        self.event    = event
        self.filepath = filepath

        if getattr(self.event, 'caller', None) == 'cronsync':
            self.with_stats = True

        try:
            self.run()
        except Exception as e:
            LOG.exception("exception during run: %r", e)

    def at_stop(self):
        self._kill_process()
