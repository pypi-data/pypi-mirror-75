#!/usr/bin/env python
# -*- coding: utf-8 -*0


"""An asynchronous subprocess utility."""


import asyncio
import concurrent.futures
import logging
import typing


def cast_proc(obj) -> asyncio.subprocess.Process:
    """Cast helper method."""
    if isinstance(obj, asyncio.subprocess.Process):
        return obj
    raise


"""Callback function definition for class SubProcess

Parameters
----------
line : str
    A string of string sub-process outputs.
isstdout : bool
    If the string is for STDOUT, then True.
    If the string is for STDERR, then False.
"""
CallbackPerLine = typing.Callable[[str, bool], None]


"""Callback function definition for class SubProcess

Parameters
----------
line : bytes
    A bytes of string sub-process outputs.
isstdout : bool
    If the string is for STDOUT, then True.
    If the string is for STDERR, then False.
"""
CallbackPerLineBytes = typing.Callable[[bytes, bool], None]


class SubProcess:
    """Execute a sub process and capture stdout and stderr.

    This class wraps :class:`asyncio.subprocess.Process`.

    Set program(path) and the arguments,
    and then call exec() with concurrent.futures functionality.
    You should use with asyncio event loop as::

        # event loop sample code
        import asyncio
        import typing
        import zobepy

        print('event loop start')
        p = zobepy.SubProcess()
        p.program = '/bin/ls'
        p.args = ['-al']
        loop = typing.cast(asyncio.events.AbstractEventLoop, asyncio.get_event_loop())
        loop.run_until_complete(
          p.exec()
        )
        print('event loop end')

    To capture all stdout and stderr in semi-realtime(line based),
    use callback.

    """

    def __init__(self):
        """ctor."""
        self._logger = logging.getLogger(__name__)
        self._log_prefix: str = ''
        self._program: str = ''
        self._args: list[str] = []
        self._pid: int = -1
        self._return_code: int = None
        self._process: asyncio.subprocess.Process = None
        self._callback_per_line: CallbackPerLine = None
        # self._callback_per_line: CallbackPerLine = lambda a='', b=True: None
        self._callback_per_line_bytes: CallbackPerLineBytes = None
        self._callback_per_line_async = None
        self._callback_per_line_bytes_async = None

    def _get_logger(self) -> logging.Logger:
        return self._logger

    def _set_logger(self, logger: logging.Logger):
        self._logger = logger

    logger = property(_get_logger, _set_logger)
    """Get or set(change) logger."""

    def _get_log_prefix(self) -> str:
        return self._log_prefix

    def _set_log_prefix(self, str: str):
        self._log_prefix = str

    log_prefix = property(_get_log_prefix, _set_log_prefix)

    def _get_program(self):
        return self._program

    def _set_program(self, program: str):
        self._program = program

    program = property(_get_program, _set_program)
    """Program path to execute."""

    def _get_args(self):
        return self._args

    def _set_args(self, args):
        self._args = args

    def set_args(self, *args):
        """Set arguments to the program."""
        self._args = args

    args = property(_get_args, _set_args)
    """Arguments to be passed to the program"""

    @property
    def pid(self) -> int:
        """Processid of the executing program process.

        -1 if the process has not been started yet.
        """
        return self._pid

    @pid.setter
    def pid(self, pid: int):
        self._pid = pid

    def _get_return_code(self) -> int:
        return self._return_code

    def _set_return_code(self, return_code: int):
        self._return_code = return_code

    return_code = property(_get_return_code)
    """The return value of the executing program process.

    None if the process is running or before run.
    """

    # def _adapt_stdout(self, line):
    #     self._process_stream(line, True)
    #
    # def _adapt_stderr(self, line):
    #     self._process_stream(line, False)

    @property
    def callback_per_line(self) -> CallbackPerLine:
        """Set callback function to get subprocess output in real time.

        Callback function specification:
            func(line: str, isstdout: bool) -> None

        Set
        callback function::

            def your_function(line: str, isstdout: bool):
                print(line)

            sp = zobepy.SubProcess()
            sp.callback_per_line = your_function


        Lambda function
        is also available::

            sp = zobepy.SubProcess()
            sp.callback_per_line = lambda line, isstdout: print(line)

        Note:
            This function implicitly converts subprocess output bytes
            into string as 'utf-8'.

            Use :func:`callback_per_line_bytes` to get data as-is.

        Warning:
            Do not block for a long time in this function
            to keep condition good about parallel execution.
            Otherwise use :func:`callback_per_line_async` instead.

        """
        return self._callback_per_line

    @callback_per_line.setter
    def callback_per_line(self, callback_per_line: CallbackPerLine):
        self._callback_per_line = callback_per_line

    # def _get_callback_per_line(self) -> CallbackPerLine:
    #     return self._callback_per_line
    #
    # def _set_callback_per_line(self, callback_per_line: CallbackPerLine):
    #     self._callback_per_line = callback_per_line

    # callback_per_line: CallbackPerLine = property(
    #     _get_callback_per_line, _set_callback_per_line)
    # """Set callback function to get subprocess output in real time.
    #
    # Callback function specification:
    #     func(line: str, isstdout: bool) -> None
    #
    #     .. csv-table::
    #        :header: , B, A and B
    #        :widths: 5, 5, 5
    #
    #        False, False, False
    #        True, False, False
    #        False, True, False
    #        True, True, True
    #
    # Set
    # callback function::
    #     def your_function(line: str, isstdout: bool):
    #         print(line)
    #
    #     sp = zobepy.SubProcess()
    #     sp.callback_per_line = your_function
    #
    #
    # Lambda function
    # is also available::
    #     sp = zobepy.SubProcess()
    #     sp.callback_per_line = lambda line, isstdout: print(line)
    #
    # Note:
    #     This function implicitly converts subprocess output bytes
    #     into string as 'utf-8'.
    #
    #     Use :func:`callback_per_line_bytes`
    #
    # Warning:
    #     warning?
    #
    # .. csv-table::
    #    :header: A, B, A and B
    #    :widths: 5, 5, 5
    #
    #    False, False, False
    #    True, False, False
    #    False, True, False
    #    True, True, True
    #
    # .. index:: Foo
    #
    # """

    @property
    def callback_per_line_bytes(self) -> CallbackPerLineBytes:
        """Set callback function to get subprocess output bytes in real time."""
        return self._callback_per_line_bytes

    @callback_per_line_bytes.setter
    def callback_per_line_bytes(self, func: CallbackPerLineBytes):
        self._callback_per_line_bytes = func

    def _get_callback_per_line_async(self):
        return self._callback_per_line_async

    def _set_callback_per_line_async(self, callback_per_line_async):
        if callback_per_line_async is None:
            self._callback_per_line_async = None
        elif asyncio.iscoroutinefunction(callback_per_line_async):
            self._callback_per_line_async = callback_per_line_async
        else:
            raise TypeError('A coroutine function or None is '
                            'required')

    callback_per_line_async = property(
        _get_callback_per_line_async, _set_callback_per_line_async)
    """Set callback coroutine function to get subprocess output bytes.

    """

    def _get_callback_per_line_bytes_async(self):
        return self._callback_per_line_bytes_async

    def _set_callback_per_line_bytes_async(self, callback_per_line_bytes_async):
        if callback_per_line_bytes_async is None:
            self._callback_per_line_bytes_async = None
        elif asyncio.iscoroutinefunction(callback_per_line_bytes_async):
            self._callback_per_line_bytes_async = callback_per_line_bytes_async
        else:
            raise TypeError('A coroutine function or None is '
                            'required')

    callback_per_line_bytes_async = property(
        _get_callback_per_line_bytes_async, _set_callback_per_line_bytes_async)
    """Set callback coroutine function to get subprocess output bytes.

    """

    async def _process_stream_async(self, line, isstdout: bool = True):
        prefix = 'STDOUT'
        if not isstdout:
            prefix = 'STDERR'

        if isstdout:
            s = '{}pid={}: {}: {}'
            s = s.format(self.log_prefix, self.pid, prefix, line)
            self._logger.info(s)
        else:
            s = '{}pid={}: {}: {}'
            s = s.format(self.log_prefix, self.pid, prefix, line)
            self._logger.warning(s)
        # print('{}pid={}: {}: {}'.format(self.log_prefix, self.pid, prefix, line))

        if self._callback_per_line_bytes is not None:
            self._callback_per_line_bytes(line, isstdout)
        if self._callback_per_line is not None:
            self._callback_per_line(line.decode('utf-8'), isstdout)
        if self._callback_per_line_bytes_async is not None:
            await self._callback_per_line_bytes_async(line, isstdout)
        if self._callback_per_line_async is not None:
            await self._callback_per_line_async(line.decode('utf-8'), isstdout)

    async def _read_stream_async(self, stream, cb_async):
        futures = []
        while True:
            line = await stream.readline()
            if line:
                # call _adapt_stdout_async or _adapt_stderr_async
                f = asyncio.ensure_future(cb_async(line))
                futures.append(f)
            else:
                break
        if(len(futures) > 0):
            await asyncio.wait(futures)

    async def _adapt_stdout_async(self, line):
        f = asyncio.ensure_future(self._process_stream_async(line, True))
        await f

    async def _adapt_stderr_async(self, line):
        f = asyncio.ensure_future(self._process_stream_async(line, False))
        await f

    async def exec(self):
        """Execute sub-process and returns code.

        This method is a coroutine.

        Returns
        -------
        int
            Return code of sub-process

        """
        create = asyncio.create_subprocess_exec(
            self.program, *self.args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        str = '{}launching process'
        self._logger.info(str.format(self.log_prefix))
        proc = await create
        proc = cast_proc(proc)
        # self._set_pid(proc.pid)
        self.pid = proc.pid
        str = '{}process started. id: {}'
        self._logger.info(str.format(self.log_prefix, self.pid))

        coReadStdout = self._read_stream_async(
            proc.stdout, self._adapt_stdout_async)
        coReadStdErr = self._read_stream_async(
            proc.stderr, self._adapt_stderr_async)
        coProcItself = proc.wait()

        fReadStdout = asyncio.ensure_future(coReadStdout)
        fReadStderr = asyncio.ensure_future(coReadStdErr)
        fProcItself = asyncio.ensure_future(coProcItself)

        futures = [fReadStdout, fReadStderr, fProcItself]
        return_when = concurrent.futures.ALL_COMPLETED

        self._process = proc
        await asyncio.wait(futures, return_when=return_when)
        self._process = None

        return_code = proc.returncode
        self._set_return_code(return_code)
        s = '{}pid={}: return code {}'
        s = s.format(self.pid, self.log_prefix, return_code)
        self._logger.info(s)
        return return_code

    def kill(self) -> None:
        """Kill running process.

        Call kill method(signal.SIGKILL) of the process(asyncio.subprocess.Process).
        """
        if self._process is not None:
            self._process.kill()

    def terminate(self) -> None:
        """Terminate running process.

        Call terminate method(signal.SIGTERM) of the process(asyncio.subprocess.Process).
        """
        if self._process is not None:
            self._process.terminate()

    def send_signal(self, signal_: int) -> None:
        """Send signal to the running process.

        Call send_signal method of the process(asyncio.subprocess.Process).
        """
        if self._process is not None:
            self._process.send_signal(signal_)


class SubProcessStdoutReceiver:
    """STDOUT receiver class for SubProcess.

    Gets whole output of SubProcess.

    #. Instantiate This
    #. Set this.callback() to SubProcess.callback_per_line
    #. Use whole STDOUT

        #. Use STDOUT as binary: this.get()
        #. Use STDOUT as string: this.get_string()

    """

    def __init__(self):
        """Init."""
        self._buffer = b''

    def callback(self, line, isstdout):
        """Store received data."""
        if isstdout:
            self._buffer += line

    def print(self):
        """Print all received data to console."""
        print(self._buffer)

    def print_string(self):
        """Print all received data as a utf-8 string to console."""
        print(self._buffer.decode('utf-8'))

    def get(self) -> str:
        """Get all received data."""
        return self._buffer

    def get_string(self) -> str:
        """Get all received data as a utf-8 string."""
        return self._buffer.decode('utf-8')
