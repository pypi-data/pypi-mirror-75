#-----------------------------------------------------------------------------
# Product: QUTest Python scripting (requires Python 3.3+)
# Last updated for version 6.8.4
# Last updated on  2020-08-01
#
#                    Q u a n t u m  L e a P s
#                    ------------------------
#                    Modern Embedded Software
#
# Copyright (C) 2005-2020 Quantum Leaps, LLC. All rights reserved.
#
# This program is open source software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alternatively, this program may be distributed and modified under the
# terms of Quantum Leaps commercial licenses, which expressly supersede
# the GNU General Public License and are specifically designed for
# licensees interested in retaining the proprietary status of their code.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <www.gnu.org/licenses/>.
#
# Contact information:
# <www.state-machine.com/licensing>
# <info@state-machine.com>
#-----------------------------------------------------------------------------

import socket
import struct
import time
import sys
import traceback
import os
if os.name == 'nt':
    import msvcrt
else:
    import select

from fnmatch import fnmatchcase
from glob import glob
from platform import python_version
from subprocess import Popen
from inspect import getframeinfo, stack

#=============================================================================
# QUTest test-script runner
# https://www.state-machine.com/qtools/qutest_script.html
#
class QUTest:
    VERSION = 684

    # class variables
    _host_exe = ''
    _is_debug = False
    _exit_on_fail = False
    _have_target = False
    _have_info   = False
    _need_reset  = True
    _last_record = ''
    _num_groups  = 0
    _num_tests   = 0
    _num_failed  = 0
    _num_skipped = 0

    # states of the internal state machine
    _INIT = 0
    _TEST = 1
    _FAIL = 2
    _SKIP = 3

    # timeout value [seconds]
    _TOUT = 1.000

    # options for implemented commands
    _OPT_NORESET = 0x01

    # output strings with decorations (colors/backgrounds)
    _STR_TEST_PASS  = 'PASS' # no decorations
    _STR_TEST_FAIL  = '\033[1;91mFAIL\033[0m'
    _STR_ERR1       = '\033[41m\033[37m' # WHITE on RED
    _STR_ERR2       = '\033[0m'    # expectation end DEFAULT
    _STR_EXP1       = '\033[44m\033[37m' # WHITE on BLUE
    _STR_EXP2       = '\033[0m'    # expectation end DEFAULT
    _STR_EXC1       = '\033[31m' # exception text begin RED
    _STR_EXC2       = '\033[0m'    # exception text end   DEFAULT
    _STR_FINAL_OK   = '\033[42m    \033[30m OK     \033[0m'
    _STR_FINAL_FAIL = '\033[41m   \033[1;37m FAIL    \033[0m'
    _STR_QSPY_FAIL  = '\033[1;91mFAIL\033[0m'

    def __init__(self):
        QUTest._have_target = False
        QUTest._have_info   = False
        QUTest._need_reset  = True

        self._state     = QUTest._INIT
        self._timestamp = 0
        self._startTime = 0
        self._to_skip   = 0

        # The following _DSL_dict dictionary defines the QUTest testing
        # DSL (Domain Specific Language), which is documented separately
        # in the file "QUTest_dsl.py".
        #
        self._DSL_dict  = {
            'test': self.test,
            'skip': self.skip,
            'expect': self.expect,
            'glb_filter': self.glb_filter,
            'loc_filter': self.loc_filter,
            'current_obj': self.current_obj,
            'query_curr': self.query_curr,
            'tick': self.tick,
            'expect_pause': self.expect_pause,
            'continue_test': self.continue_test,
            'command': self.command,
            'init': self.init,
            'dispatch': self.dispatch,
            'post': self.post,
            'publish': self.publish,
            'probe': self.probe,
            'peek': self.peek,
            'poke': self.poke,
            'fill': self.fill,
            'pack': struct.pack,
            'on_reset': self._dummy_on_reset,
            'on_setup': self._dummy_on_setup,
            'on_teardown': self._dummy_on_teardown,
            'VERSION': QUTest.VERSION,
            'NORESET': QUTest._OPT_NORESET,
            'OBJ_SM': QSpy._OBJ_SM,
            'OBJ_AO': QSpy._OBJ_AO,
            'OBJ_MP': QSpy._OBJ_MP,
            'OBJ_EQ': QSpy._OBJ_EQ,
            'OBJ_TE': QSpy._OBJ_TE,
            'OBJ_AP': QSpy._OBJ_AP,
            'OBJ_SM_AO': QSpy._OBJ_SM_AO,
            'GRP_OFF': 0,
            'GRP_ON': QSpy._GRP_ON,
            'GRP_SM': QSpy._GRP_SM,
            'GRP_AO': QSpy._GRP_AO,
            'GRP_EQ': QSpy._GRP_EQ,
            'GRP_MP': QSpy._GRP_MP,
            'GRP_TE': QSpy._GRP_TE,
            'GRP_QF': QSpy._GRP_QF,
            'GRP_SC': QSpy._GRP_SC,
            'GRP_U0': QSpy._GRP_U0,
            'GRP_U1': QSpy._GRP_U1,
            'GRP_U2': QSpy._GRP_U2,
            'GRP_U3': QSpy._GRP_U3,
            'GRP_U4': QSpy._GRP_U4,
            'GRP_UA': QSpy._GRP_UA
        }

    def __del__(self):
        #print('~QUTest', self)
        pass

    #-------------------------------------------------------------------------
    # QUTest Domain Specific Language (DSL) commands

    # test DSL command .......................................................
    def test(self, name, opt = 0):
        # end the previous test
        self._test_end()

        # start the new test...
        self._startTime = QUTest._time()
        QUTest._num_tests += 1
        print('%s: ' %name, end = '')

        if self._to_skip > 0:
            self._to_skip -= 1
            QUTest._num_skipped += 1
            print('SKIPPED')
            self._tran(QUTest._SKIP)
            return

        if opt & QUTest._OPT_NORESET != 0:
            if self._state == QUTest._FAIL:
                self._fail('NORESET-test follows a failed test')
                return
            if QUTest._need_reset:
                self._fail('NORESET-test needs reset')
                return
            self._tran(QUTest._TEST)
        else:
            self._tran(QUTest._TEST)
            if not self._reset_target():
                return

        if not self._on_setup():
            self._fail('on_setup() failed')
            return

    # expect DSL command .....................................................
    def expect(self, match):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('expect')
        elif self._state == QUTest._TEST:

            if not QSpy._receive(): # timeout?
                self._fail('got: "" (timeout)',
                           'exp: "%s"' %match)
                return False

            if match.startswith('@timestamp'):
                self._timestamp += 1
                expected = '%010d' %self._timestamp + match[10:]
            elif match[0:9].isdigit():
                self._timestamp += 1
                expected = match
            else:
                expected = match

            received = QUTest._last_record[3:].decode('utf-8')

            if fnmatchcase(received, expected):
                return True
            else:
                self._fail('got: "%s"' %received,
                           'exp: "%s"' %expected)
                return False
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in expect: ' + match

    # glb_filter DSL command .................................................
    def glb_filter(self, *args):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('glb_filter')
        elif self._state == QUTest._TEST:
            filter = [0, 0, 0, 0]

            for arg in args:
                if arg == 0:
                    pass
                elif arg < 0x7F:
                    filter[arg // 32] |= 1 << (arg % 32)
                elif arg == QSpy._GRP_ON:
                    # all filters on
                    filter[0] = 0xFFFFFFFF
                    filter[1] = 0xFFFFFFFF
                    filter[2] = 0xFFFFFFFF
                    filter[3] = 0x1FFFFFFF
                    break  # no point in continuing
                elif arg == QSpy._GRP_SM:  # state machines
                    filter[0] |= 0x000003FE
                    filter[1] |= 0x03800000
                elif arg == QSpy._GRP_AO:   # active objects
                    filter[0] |= 0x0007FC00
                    filter[1] |= 0x00002000
                elif arg == QSpy._GRP_EQ:  # raw queues
                    filter[0] |= 0x00780000
                    filter[2] |= 0x00004000
                elif arg == QSpy._GRP_MP:  # raw memory pools
                    filter[0] |= 0x03000000
                    filter[2] |= 0x00008000
                elif arg == QSpy._GRP_QF:  # framework
                    filter[0] |= 0xFC000000
                    filter[1] |= 0x00001FC0
                elif arg == QSpy._GRP_TE:  # time events
                    filter[1] |= 0x0000007F
                elif arg == QSpy._GRP_SC:  # scheduler
                    filter[1] |= 0x007F0000
                elif arg == QSpy._GRP_U0:  # user 70-79
                    filter[2] |= 0x0000FFC0
                elif arg == QSpy._GRP_U1:  # user 80-89
                    filter[2] |= 0x03FF0000
                elif arg == QSpy._GRP_U2:  # user 90-99
                    filter[2] |= 0xFC000000
                    filter[3] |= 0x0000000F
                elif arg == QSpy._GRP_U3:  # user 100-109
                    filter[3] |= 0x00003FF0
                elif arg == QSpy._GRP_U4:  # user 110-124
                    filter[3] |= 0x1FFFC000
                elif arg == QSpy._GRP_UA:  # user 70-124 (all)
                    filter[2] |= 0xFFFFFFC0
                    filter[3] |= 0x1FFFFFFF
                else:
                    assert 0, 'invalid global filter'

            QSpy._sendTo(struct.pack(
                '<BBLLLL', QSpy._TRGT_GLB_FILTER, 16,
                filter[0], filter[1], filter[2], filter[3]))

            self.expect('           Trg-Ack  QS_RX_GLB_FILTER')

        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in glb_filter'

    # loc_filter DSL command .................................................
    def loc_filter(self, obj_kind, obj_id):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('loc_filter')
        elif self._state == QUTest._TEST:
            fmt = '<BB' + QSpy.fmt_objPtr
            if isinstance(obj_id, int):
                # Send directly to Target
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._TRGT_LOC_FILTER, obj_kind, obj_id))
            else:
                # Have QSpy interpret obj_id string and send filter
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._QSPY_SEND_LOC_FILTER, obj_kind, 0),
                    obj_id)
            self.expect('           Trg-Ack  QS_RX_LOC_FILTER')

        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in loc_filter'

    # current_obj DSL command ................................................
    def current_obj(self, obj_kind, obj_id):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('current_obj')
        elif self._state == QUTest._TEST:
            fmt = '<BB' + QSpy.fmt_objPtr
            # Build packet according to obj_id type
            if isinstance(obj_id, int):
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._TRGT_CURR_OBJ, obj_kind, obj_id))
            else:
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._QSPY_SEND_CURR_OBJ, obj_kind, 0),
                    obj_id) # add string object ID to end
            self.expect('           Trg-Ack  QS_RX_CURR_OBJ')

        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in current_obj'

    # query_curr DSL command .................................................
    def query_curr(self, obj_kind):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('query_curr')
        elif self._state == QUTest._TEST:
            QSpy._sendTo(struct.pack('<BB', QSpy._TRGT_QUERY_CURR, obj_kind))
            # test-specific expect
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in query_curr'

    # expect_pause DSL command ...............................................
    def expect_pause(self):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('expect_pause')
        elif self._state == QUTest._TEST:
            self.expect('           TstPause')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in expect_pause'

    # continue_test DSL command ..............................................
    def continue_test(self):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('continue_test')
        elif self._state == QUTest._TEST:
            QSpy._sendTo(struct.pack('<B', QSpy._TRGT_CONTINUE))
            self.expect('           Trg-Ack  QS_RX_TEST_CONTINUE')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in continue_test'

    # command DSL command ....................................................
    def command(self, cmdId, param1 = 0, param2 = 0, param3 = 0):
        if self._to_skip > 0:
            pass # ignore
        if self._state == QUTest._INIT:
            self._before_test('command')
        elif self._state == QUTest._TEST:
            fmt = '<BBIII'
            if isinstance(cmdId, int):
                QSpy._sendTo(struct.pack(fmt, QSpy._TRGT_COMMAND,
                                     cmdId, param1, param2, param3))
            else:
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._QSPY_SEND_COMMAND, 0, param1, param2, param3),
                    cmdId) # add string command ID to end
            self.expect('           Trg-Ack  QS_RX_COMMAND')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in command'

    # init DSL command .......................................................
    def init(self, signal = 0, params = None):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('init')
        elif self._state == QUTest._TEST:
            QSpy._sendEvt(QSpy._EVT_INIT, signal, params)
            self.expect('           Trg-Ack  QS_RX_EVENT')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in init'

    # dispatch DSL command ...................................................
    def dispatch(self, signal, params = None):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('dispatch')
        elif self._state == QUTest._TEST:
            QSpy._sendEvt(QSpy._EVT_DISPATCH, signal, params)
            self.expect('           Trg-Ack  QS_RX_EVENT')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in dispatch'

    # post DSL command .......................................................
    def post(self, signal, params = None):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('post')
        elif self._state == QUTest._TEST:
            QSpy._sendEvt(QSpy._EVT_POST, signal, params)
            self.expect('           Trg-Ack  QS_RX_EVENT')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in post'

    # publish DSL command ....................................................
    def publish(self, signal, params = None):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('publish')
        elif self._state == QUTest._TEST:
            QSpy._sendEvt(QSpy._EVT_PUBLISH, signal, params)
            self.expect('           Trg-Ack  QS_RX_EVENT')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in publish'

    # probe DSL command ......................................................
    def probe(self, func, data):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('probe')
        elif self._state == QUTest._TEST:
            fmt = '<BI' + QSpy.fmt_funPtr
            if isinstance(func, int):
                # Send directly to target
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._TRGT_TEST_PROBE, data, func))
            else:
                # Send to QSpy to provide 'func' from Fun Dictionary
                QSpy._sendTo(struct.pack(
                    fmt, QSpy._QSPY_SEND_TEST_PROBE, data, 0),
                    func) # add string func name to end
            self.expect('           Trg-Ack  QS_RX_TEST_PROBE')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in probe'

    # tick DSL command .......................................................
    def tick(self, tick_rate = 0):
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('tick')
        elif self._state == QUTest._TEST:
            QSpy._sendTo(struct.pack('<BB', QSpy._TRGT_TICK, tick_rate))
            self.expect('           Trg-Ack  QS_RX_TICK')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in tick'

    # peek DSL command .......................................................
    def peek(self, offset, size, num):
        assert size == 1 or size == 2 or size == 4, \
            'Size must be 1, 2, or 4'
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('peek')
        elif self._state == QUTest._TEST:
            QSpy._sendTo(struct.pack('<BHBB', QSpy._TRGT_PEEK,
                offset, size, num))
            # explicit expectation of peek output
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in peek'

    # poke DSL command .......................................................
    def poke(self, offset, size, data):
        assert size == 1 or size == 2 or size == 4, \
            'Size must be 1, 2, or 4'
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('poke')
        elif self._state == QUTest._TEST:
            length = len(data)
            num = length // size
            QSpy._sendTo(struct.pack('<BHBB', QSpy._TRGT_POKE,
                         offset, size, num) + data)
            self.expect('           Trg-Ack  QS_RX_POKE')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in poke'

    # fill DSL command .......................................................
    def fill(self, offset, size, num, item = 0):
        assert size == 1 or size == 2 or size == 4, \
            'Size must be 1, 2, or 4'
        if self._to_skip > 0:
            pass # ignore
        elif self._state == QUTest._INIT:
            self._before_test('fill')
        elif self._state == QUTest._TEST:
            if size == 1:
                item_fmt = 'B'
            elif size == 2:
                item_fmt = 'H'
            elif size == 4:
                item_fmt = 'L'
            else:
                assert False, 'size for sendFill must be 1, 2, or 4!'
            fmt = '<BHBB' + item_fmt
            packet = struct.pack(fmt, QSpy._TRGT_FILL, offset, size, num, item)
            QSpy._sendTo(packet)
            self.expect('           Trg-Ack  QS_RX_FILL')
        elif self._state == QUTest._FAIL or self._state == QUTest._SKIP:
            pass # ignore
        else:
            assert 0, 'invalid state in fill'

    # skip DSL command .......................................................
    def skip(self, nTests = 9999):
        if self._to_skip == 0: # not skipping already?
            self._to_skip = nTests

    # dummy callbacks --------------------------------------------------------
    def _dummy_on_reset(self):
        #print('_dummy_on_reset')
        pass

    def _dummy_on_setup(self):
        #print('_dummy_on_setup')
        pass

    def _dummy_on_teardown(self):
        #print('_dummy_on_teardown')
        pass

    # helper methods ---------------------------------------------------------
    @staticmethod
    def _run_script(fname):
        print('--------------------------------------------------'
              '\nGroup:', fname)
        QUTest._num_groups += 1

        err = 0 # assume no errors
        with open(fname) as f:
            QUTest_inst = QUTest()
            try:
                code = compile(f.read(), fname, 'exec')
                # execute the script code in a separate instance of QUTest
                exec(code, QUTest_inst._DSL_dict)
            except (AssertionError,
                    RuntimeError,
                    OSError) as e:
                QUTest_inst._fail()
                print(QUTest._STR_EXC1 + repr(e) + QUTest._STR_EXC2)
                err = -2
            except: # most likely an error in a test script
                #exc_type, exc_value, exc_traceback = sys.exc_info()
                QUTest_inst._fail()
                QUTest._quit_host_exe()
                traceback.print_exc(2)
                err = -3

            QUTest_inst._test_end()
            QUTest._quit_host_exe()
            err = QUTest._num_failed

        return err;

    def _tran(self, state):
        #print('tran(%d->%d)' %(self._state, state))
        self._state = state

    def _test_end(self):
        if not self._state == QUTest._TEST:
            return

        if not QUTest._have_info:
            return

        QSpy._sendTo(struct.pack('<B', QSpy._TRGT_TEST_TEARDOWN))
        if not QSpy._receive(): # timeout?
            self._fail('got: "" (timeout)',
                       'exp: end-of-test')
            return

        expected = '           Trg-Ack  QS_RX_TEST_TEARDOWN'
        received = QUTest._last_record[3:].decode('utf-8')
        if received == expected:
            self._DSL_dict['on_teardown']()
            print('%s (%.3fs)' %(
                QUTest._STR_TEST_PASS,
                QUTest._time() - self._startTime))
            return
        else:
            self._fail('got: "%s"' %received,
                       'exp: end-of-test')
            # ignore all input until timeout
            while QSpy._receive():
                pass

    def _reset_target(self):
        if QUTest._host_exe != '': # running a host executable?
            QUTest._quit_host_exe()

            # lauch a new instance of the host executable
            QUTest._have_target = True
            QUTest._have_info = False
            Popen([QUTest._host_exe,
                   QSpy._host_addr[0] + ':' + str(QSpy._tcp_port)])

        else: # running an embedded target
            QUTest._have_target = True
            QUTest._have_info = False
            if not QUTest._is_debug:
                QSpy._sendTo(struct.pack('<B', QSpy._TRGT_RESET))

        # ignore all input until a timeout (False)
        while QSpy._receive():
            if QUTest._have_info:
                break

        if QUTest._have_info:
            QUTest._need_reset = False;
        else:
            QUTest._quit_host_exe()
            raise RuntimeError('Target reset failed')

        self._timestamp = 0
        self._DSL_dict['on_reset']()
        return (self._state == QUTest._TEST)

    def _on_setup(self):
        assert self._state == QUTest._TEST, \
            'on_setup() outside the TEST state %d' %self._state
        if not QUTest._have_info:
            return False

        QSpy._sendTo(struct.pack('<B', QSpy._TRGT_TEST_SETUP))
        self.expect('           Trg-Ack  QS_RX_TEST_SETUP')
        if self._state == QUTest._TEST:
            self._timestamp = 0
            self._DSL_dict['on_setup']()
            return True

    def _before_test(self, command):
        QUTest._num_failed += 1
        self._tran(QUTest._FAIL)
        msg = '"' + command + '" before any test'
        raise SyntaxError(msg)

    def _fail(self, err = '', exp = ''):
        print('%s @line:%d (%.3fs):'
            %(QUTest._STR_TEST_FAIL,
            getframeinfo(stack()[-4][0]).lineno,
            QUTest._time() - self._startTime))
        if exp != '':
            print(QUTest._STR_EXP1 + exp + QUTest._STR_EXP2)
        if err != '':
            print(QUTest._STR_ERR1 + err + QUTest._STR_ERR2)
        QUTest._num_failed += 1
        QUTest._need_reset = True
        self._tran(QUTest._FAIL)

    @staticmethod
    def _quit_host_exe():
        if QUTest._host_exe != '' and QUTest._have_target:
            QUTest._have_target = False
            QSpy._sendTo(struct.pack('<B', QSpy._TRGT_RESET))
            time.sleep(QUTest._TOUT) # wait until host-exe quits

    @staticmethod
    def _time():
        if sys.version_info[0] == 2: # Python 2 ?
            return time.time()
        else: # Python 3+
            return time.perf_counter()

#=============================================================================
# Helper class for communication with the QSpy front-end
#
class QSpy:
    # private class variables...
    _sock = None
    _is_attached = False
    _tx_seq = 0
    _host_addr = ['localhost', 7701] # list, to be converted to a tuple
    _local_port = 0 # let the OS decide the best local port
    _tcp_port = 6601

    # formats of various packet elements from the Target
    fmt_objPtr   = 'L'
    fmt_funPtr   = 'L'
    fmt_tstamp   = 'L'
    fmt_sig      = 'H'
    fmt_evtSize  = 'H'
    fmt_queueCtr = 'B'
    fmt_poolCtr  = 'H'
    fmt_poolBlk  = 'H'
    fmt_tevtCtr  = 'H'
    fmt_targetTstamp = 'UNKNOWN'

    # packets from QSPY...
    _PKT_TEXT_ECHO   = 0
    _PKT_TARGET_INFO = 64
    _PKT_ASSERTION   = 69
    _PKT_ATTACH_CONF = 128
    _PKT_DETACH      = 129

    # records to the Target...
    _TRGT_INFO       = 0
    _TRGT_COMMAND    = 1
    _TRGT_RESET      = 2
    _TRGT_TICK       = 3
    _TRGT_PEEK       = 4
    _TRGT_POKE       = 5
    _TRGT_FILL       = 6
    _TRGT_TEST_SETUP = 7
    _TRGT_TEST_TEARDOWN = 8
    _TRGT_TEST_PROBE = 9
    _TRGT_GLB_FILTER = 10
    _TRGT_LOC_FILTER = 11
    _TRGT_AO_FILTER  = 12
    _TRGT_CURR_OBJ   = 13
    _TRGT_CONTINUE   = 14
    _TRGT_QUERY_CURR = 15
    _TRGT_EVENT      = 16

    # packets to QSpy only...
    _QSPY_ATTACH     = 128
    _QSPY_DETACH     = 129
    _QSPY_SAVE_DICT  = 130
    _QSPY_SCREEN_OUT = 131
    _QSPY_BIN_OUT    = 132
    _QSPY_MATLAB_OUT = 133
    _QSPY_MSCGEN_OUT = 134
    _QSPY_SEND_EVENT = 135
    _QSPY_SEND_LOC_FILTER = 136
    _QSPY_SEND_CURR_OBJ   = 137
    _QSPY_SEND_COMMAND    = 138
    _QSPY_SEND_TEST_PROBE = 139

    # gloal filter groups...
    _GRP_ON = 0xF0
    _GRP_SM = 0xF1
    _GRP_AO = 0xF2
    _GRP_MP = 0xF3
    _GRP_EQ = 0xF4
    _GRP_TE = 0xF5
    _GRP_QF = 0xF6
    _GRP_SC = 0xF7
    _GRP_U0 = 0xF8
    _GRP_U1 = 0xF9
    _GRP_U2 = 0xFA
    _GRP_U3 = 0xFB
    _GRP_U4 = 0xFC
    _GRP_UA = 0xFD

    # kinds of objects (local-filter and curr-obj)...
    _OBJ_SM = 0
    _OBJ_AO = 1
    _OBJ_MP = 2
    _OBJ_EQ = 3
    _OBJ_TE = 4
    _OBJ_AP = 5
    _OBJ_SM_AO = 6

    # special events for QS-RX
    _EVT_PUBLISH   = 0
    _EVT_POST      = 253
    _EVT_INIT      = 254
    _EVT_DISPATCH  = 255

    # special empty record
    _EMPTY_RECORD  = '    '

    @staticmethod
    def _init():
        # Create socket
        QSpy._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        QSpy._sock.settimeout(QUTest._TOUT) # timeout for the socket
        try:
            QSpy._sock.bind(('localhost', QSpy._local_port))
            #print("bind: ", ('localhost', QSpy._local_port))
        except:
            messagebox.showerror("UDP Socket Error",
               "Can't bind the UDP socket\nto the specified local_host")
            QSpyView._gui.destroy()
            return -1
        return 0

    @staticmethod
    def _attach(channels = 0x2):
        # channels: 1-binary, 2-text, 3-both
        print('Attaching to QSpy (%s:%d) ... '
            %(QSpy._host_addr[0], QSpy._host_addr[1]), end = '')
        QSpy._is_attached = False
        QSpy._sendTo(struct.pack('<BB', QSpy._QSPY_ATTACH, channels))
        try:
            QSpy._receive()
        except:
            pass

        if QSpy._is_attached:
            print('OK')
            return True
        else:
            print(QUTest._STR_QSPY_FAIL)
            return False

    @staticmethod
    def _detach():
        if QSpy._sock is None:
            return
        QSpy._sendTo(struct.pack('<B', QSpy._QSPY_DETACH))
        time.sleep(QUTest._TOUT)
        #QSpy._sock.shutdown(socket.SHUT_RDWR)
        QSpy._sock.close()
        QSpy._sock = None

    @staticmethod
    def _receive():
        '''returns True if packet received, False if timed out'''

        if not QUTest._is_debug:
            try:
                packet = QSpy._sock.recv(4096)
            except socket.timeout:
                QUTest._last_record = QSpy._EMPTY_RECORD
                return False # timeout
            # don't catch OSError
        else:
            while True:
                try:
                    packet = QSpy._sock.recv(4096)
                    break
                except socket.timeout:
                    print("\nwaiting for Target "\
                        "(press Enter to skip this test)...", end='')
                    if os.name == 'nt':
                        if msvcrt.kbhit():
                            if msvcrt.getch() == '\r':
                                print()
                                return False; # timeout
                    else:
                        dr,dw,de = select.select([sys.stdin], [], [], 0)
                        if dr != []:
                            sys.stdin.readline() # consue the Return key
                            print()
                            return False; # timeout
                # don't catch OSError

        dlen = len(packet)
        if dlen < 2:
            QUTest._last_record = QSpy._EMPTY_RECORD
            raise RuntimeError('UDP packet from QSpy too short')

        recID = packet[1]
        if recID == QSpy._PKT_TEXT_ECHO: # text packet (most common)
            QUTest._last_record = packet
            # QS_ASSERTION?
            if dlen > 3 and packet[2] == QSpy._PKT_ASSERTION:
                QUTest._need_reset = True

        elif recID == QSpy._PKT_TARGET_INFO: # target info?
            if dlen != 18:
                QUTest._last_record = QSpy._EMPTY_RECORD
                raise RuntimeError('Incorrect Target info')

            fmt = 'xBHxLxxxQ'
            tstamp = packet[5:18]
            QSpy.fmt_objPtr  = fmt[tstamp[3] & 0x0F]
            QSpy.fmt_funPtr  = fmt[tstamp[3] >> 4]
            QSpy.fmt_tstamp  = fmt[tstamp[4] & 0x0F]
            QSpy.fmt_sig     = fmt[tstamp[0] & 0x0F]
            QSpy.fmt_evtSize = fmt[tstamp[0] >> 4]
            QSpy.fmt_queueCtr= fmt[tstamp[1] & 0x0F]
            QSpy.fmt_poolCtr = fmt[tstamp[2] >> 4]
            QSpy.fmt_poolBlk = fmt[tstamp[2] & 0x0F]
            QSpy.fmt_tevtCtr = fmt[tstamp[1] >> 4]
            QSpy.fmt_targetTstamp = '%02d%02d%02d_%02d%02d%02d' \
                %(tstamp[12], tstamp[11], tstamp[10],
                  tstamp[9], tstamp[8], tstamp[7])
            #print('Target:', QSpy.fmt_targetTstamp)
            QUTest._last_record = packet
            QUTest._have_info = True

        elif recID == QSpy._PKT_ATTACH_CONF:
            QUTest._last_record = packet
            QSpy._is_attached = True

        elif recID == QSpy._PKT_DETACH:
            QUTest._quit_host_exe()
            QUTest._last_record = packet
            QSpy._detach()
            QSpy._is_attached = False

        else:
            QUTest._last_record = QSpy._EMPTY_RECORD
            raise RuntimeError('Unrecognized UDP packet type from QSpy')

        return True # some input received

    @staticmethod
    def _sendTo(packet, str=None):
        tx_packet = bytearray([QSpy._tx_seq])
        tx_packet.extend(packet)
        if str is not None:
            tx_packet.extend(bytes(str, 'utf-8'))
            tx_packet.extend(b'\0') # zero-terminate
        QSpy._sock.sendto(tx_packet, QSpy._host_addr)
        QSpy._tx_seq = (QSpy._tx_seq + 1) & 0xFF
        #print('sendTo', QSpy._tx_seq)

    @staticmethod
    def _sendEvt(ao_prio, signal, parameters = None):
        fmt = '<BB' + QSpy.fmt_sig + 'H'
        if parameters is not None:
            length = len(parameters)
        else:
            length = 0

        if isinstance(signal, int):
            packet = bytearray(struct.pack(
                fmt, QSpy._TRGT_EVENT, ao_prio, signal, length))
            if parameters is not None:
                packet.extend(parameters)
            QSpy._sendTo(packet)
        else:
            packet = bytearray(struct.pack(
                fmt, QSpy._QSPY_SEND_EVENT, ao_prio, 0, length))
            if parameters is not None:
                packet.extend(parameters)
            QSpy._sendTo(packet, signal)


#=============================================================================
# main entry point to QUTest
def main(*args):
    # process command-line arguments...
    argv = sys.argv
    argc = len(argv)
    arg  = 1 # skip the 'qutest' argument

    if '-h' in argv or '--help' in argv or '?' in argv:
        print('\nusage: python qutest.py [-x] [test-scripts] '
              '[host_exe] [qspy_host[:udp_port]] [qspy_tcp_port]\n\n'
              'help at: https://www.state-machine.com/qtools/qutest.html')
        return sys.exit(0)

    print('QUTest unit testing front-end %d.%d.%d running on Python %s' \
           %(QUTest.VERSION//100,
            (QUTest.VERSION//10) % 10,
             QUTest.VERSION % 10, python_version()))
    print('Copyright (c) 2005-2020 Quantum Leaps, www.state-machine.com')

    if '--version' in argv:
        return sys.exit(0)

    startTime = QUTest._time()

    # on Windows enable color escape characters in the console...
    if os.name == 'nt':
        os.system('color')

    # list of scripts to exectute...
    scripts = []

    if arg < argc and argv[arg] == '-x':
        QUTest._exit_on_fail = True
        arg += 1

    # scan argv for test scripts...
    while arg < argc:
        # if test file input uses wildcard, find matches
        if argv[arg].endswith('.py'):
            scripts.extend(glob(argv[arg]))
            arg += 1
        else:
            break
    if not scripts: # no specfic scripts found?
        scripts.extend(glob('*.py')) # take all scripts in the current dir

    if arg < argc:
        QUTest._host_exe = argv[arg]
        arg += 1
        if QUTest._host_exe == 'DEBUG':
            QUTest._host_exe = ''
            QUTest._is_debug = True
    if arg < argc:
        host_port = new_argv[arg].split(':')
        arg += 1
        if len(host_port) > 0:
            QSpy._host_addr[0] = host_port[0]
        if len(host_port) > 1:
            QSpy._host_addr[1] = int(host_port[1])
    if arg < argc:
        QSpy._tcp_port = new_argv[arg]

    QSpy._host_addr = tuple(QSpy._host_addr) # convert to immutable tuple

    # init QSpy socket
    err = QSpy._init()
    if err:
        return sys.exit(err)

    # attach the the QSPY Back-End
    if not QSpy._attach():
        return sys.exit(-1)

    # run all the test scripts...
    err = 0
    for scr in scripts:
        # run the script...
        err = QUTest._run_script(scr)

        # error encountered and shall we quit on failure?
        if err != 0 and QUTest._exit_on_fail:
            break

    if QUTest._num_failed == 0:
        # print 'OK' in GREEN
        status = QUTest._STR_FINAL_OK
    else:
        # print 'FAIL!' in RED
        status = QUTest._STR_FINAL_FAIL

    if QUTest._have_info:
        print('============= Target:',
               QSpy.fmt_targetTstamp, '==============')
    else:
        print('================= (no target ) ===================')

    print('%d Groups, %d Tests, %d Failures, %d Skipped (%.3fs)\n'
          '%s'
          %(QUTest._num_groups, QUTest._num_tests,
            QUTest._num_failed, QUTest._num_skipped,
            (QUTest._time() - startTime),
            status))

    QUTest._quit_host_exe()
    QSpy._detach()

    return sys.exit(err)

#=============================================================================
if __name__ == '__main__':
    main()
