#-----------------------------------------------------------------------------
# Product: QView in Python (requires Python 3.3+)
# Last updated for version 6.8.3
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
import time
import sys
import traceback
import os
import webbrowser

from tkinter import *
from tkinter.ttk import * # override the basic Tk widgets with Ttk widgets
from tkinter.simpledialog import *
from struct import *

#=============================================================================
# QView GUI
# https://www.state-machine.com/qtools/qview.html
#
class QView:
    VERSION = 683     ##< current vesion of QView

    # public class variables...
    custom_menu = None   ##< custom menu for the customization script 
    canvas      = None   ##< canvas to be customized
    home_dir    = None   ##< home directory of the customization script

    # privte class variables...
    _have_info   = False
    _text_lines  = "end - 500 lines"
    _attach_dialog = None
    _gui  = None
    _cust = None
    _err  = 0


    @staticmethod
    def _init_gui():
        Tk.report_callback_exception = QView._trap_error

        # menus...............................................................
        main_menu = Menu(QView._gui, tearoff=0)
        QView._gui.config(menu=main_menu)
        
        # File menu...
        m = Menu(main_menu, tearoff=0)
        m.add_command(label="Store Dictionaries", accelerator='Ctrl+d')
        m.add_command(label="Screen Output", accelerator='Ctrl+o')
        m.add_command(label="Save QS Binary", accelerator='Ctrl+s')
        m.add_command(label="Matlab Output")
        m.add_separator()
        m.add_command(label="Exit", accelerator='Alt+F4',
                      command=QView._quit)
        QView._gui.bind('<Alt-F4>', QView._onExit)
        main_menu.add_cascade(label="File", menu=m)

        # View menu...
        m = Menu(main_menu, tearoff=0)
        QView._view_canvas = IntVar()
        QView._view_canvas.set(0)
        m.add_checkbutton(label="Canvas", variable=QView._view_canvas,
                          command=QView._onCanvasView)
        main_menu.add_cascade(label="View", menu=m)

        # Filters menu...
        m = Menu(main_menu, tearoff=0)
        m.add_command(label="Global Filters...", accelerator='Ctrl+g',
                      command=QView._onGlbFilters)
        QView._gui.bind('<Control-g>', QView._onGlbFilters)
        m.add_command(label="Local Filters...", accelerator='Ctrl+l',
                      command=QView._onLocFilters)
        QView._gui.bind('<Control-l>', QView._onLocFilters)
        m.add_command(label="AO Filter...", command=QView._onAoFilter)
        main_menu.add_cascade(label="Filters", menu=m)

        # Commands menu...
        m = Menu(main_menu, tearoff=0)
        m.add_command(label="Reset Target", accelerator='Ctrl+r',
                      command=QView._onGlbFilters)
        QView._gui.bind('<Control-r>', QView._onGlbFilters)
        m.add_command(label="Queary Target Info", accelerator='Ctrl+i',
                      command=QView._onLocFilters)
        QView._gui.bind('<Control-i>', QView._onLocFilters)
        m.add_command(label="Tick[0]", accelerator='Ctrl+t',
                      command=QView._onLocFilters)
        QView._gui.bind('<Control-t>', QView._onLocFilters)
        m.add_command(label="Tick[1]", accelerator='Ctrl+u',
                      command=QView._onLocFilters)
        QView._gui.bind('<Control-u>', QView._onLocFilters)
        m.add_command(label="Peek Obj/Addr...",
                      command=QView._onLocFilters)
        m.add_command(label="Poke Obj/Addr...",
                      command=QView._onLocFilters)
        m.add_separator()
        main_menu.add_cascade(label="Commands", menu=m)

        # Custom menu...
        QView.custom_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Custom", menu=QView.custom_menu)

        # Help menu...
        m = Menu(main_menu, tearoff=0)
        m.add_command(label="Online Help", accelerator='F1',
                      command=QView._onF1Help)
        QView._gui.bind('<F1>', QView._onF1Help)
        m.add_separator()
        m.add_command(label="About...",
                      command=QView._onLocFilters)
        main_menu.add_cascade(label="Help", menu=m)

        # statusbar (pack before text-area) ..................................
        QView._scroll_text = IntVar()
        QView._scroll_text.set(1) # text scrolling enabled
        QView._echo_text = IntVar()
        QView._echo_text.set(0) # text echo disabled
        frame = Frame(QView._gui, borderwidth=1, relief="raised")
        QView._target = Label(frame, text="Target: UNKNOWN")
        QView._target.pack(side="left")
        c = Checkbutton(frame, text="Scroll", variable=QView._scroll_text)
        c.pack(side="right")
        c = Checkbutton(frame, text="Echo",
            variable=QView._echo_text,
            command=QSpy._reattach)
        c.pack(side="right")
        frame.pack(side="bottom", fill="x", pady=0)

        # text-area with scrollbar............................................
        frame = Frame(QView._gui, borderwidth=1, relief="sunken")
        scrollbar = Scrollbar(frame)
        QView._text = Text(frame, width=100, height=30,
            wrap="word", yscrollcommand=scrollbar.set)
        QView._text.bind("<Key>", lambda e: 'break') # read-only text
        scrollbar.config(command=QView._text.yview)
        scrollbar.pack(side="right", fill="y")
        QView._text.pack(side="left", fill="both", expand=True)
        frame.pack(side="left", fill="both", expand=True)

        # canvas..............................................................
        QView._canvas_toplevel = Toplevel()
        QView._canvas_toplevel.title('QView -- Canvas')
        QView._canvas_toplevel.protocol('WM_DELETE_WINDOW',
                                            func=QView._onCanvClose)
        QView.canvas = Canvas(QView._canvas_toplevel)
        QView.canvas.pack()
        QView._onCanvasView()


    @staticmethod
    def _quit(err=0):
        QView._err = err
        QView._gui.quit()

    @staticmethod
    def _trap_error(*args):
        messagebox.showerror('Runtime Error',
           traceback.format_exc(3))
        QView._quit(-3)

    @staticmethod
    def setCust(cust):
        '''! Set QView customization.
        @param cust the customization class instance
        '''
        QView._cust = cust

    @staticmethod
    def dispTxt(str):
        QView._text.delete(1.0, QView._text_lines)
        QView._text.insert(END, '\n')
        QView._text.insert(END, str)
        if QView._scroll_text.get():
            QView._text.yview_moveto(1) # scroll to the bottom

    @staticmethod
    def _onCanvasView():
        if QView._view_canvas.get():
            QView._canvas_toplevel.state('normal')
            # make the canvas jump to the front
            QView._canvas_toplevel.attributes('-topmost', 1)
            QView._canvas_toplevel.attributes('-topmost', 0)
        else:
            QView._canvas_toplevel.withdraw()

    @staticmethod
    def _onCanvClose():
        QView._view_canvas.set(0)
        QView._onCanvasView()

    @staticmethod
    def _onExit(*args):
        QView._quit()

    @staticmethod
    def _onGlbFilters(*args):
        print('_onGlbFilters()')
        pass

    @staticmethod
    def _onLocFilters(*args):
        print('_onLocFilters()')
        pass

    @staticmethod
    def _onAoFilter(*args):
        print('_onAoFilter()')
        pass

    @staticmethod
    def _onF1Help(*args):
        webbrowser.open('https://www.state-machine.com/qtools/qspyview.html',
                        new=2)
        pass


    #-------------------------------------------------------------------------
    # dialog boxes...
    #
    class _AttachDialog(Dialog):
        def __init__(self):
            QView._attach_dialog = self
            Dialog.__init__(self, QView._gui, "Attach to QSpy")

        def body(self, master):
            self.resizable(height=False, width=False)
            Label(master,
                     text="Make sure that QSpy is running and\n"
                     "not already used by other front-end.\n\n"
                     "Press OK to re-try to attach or\n"
                     "Cancel to quit.").pack()

        def close(self):
            super().cancel()
            QView._attach_dialog = None

        def validate(self):
            QSpy._attach()
            return 0

        def apply(self):
            QView._attach_dialog = None

        def cancel(self, event=None):
            super().cancel()
            QView._quit()


#=============================================================================
# Helper class for UDP-communication with the QSpy front-end
# (non-blocking UDP-socket version for QView)
#
class QSpy:
    # private class variables...
    _sock = None
    _is_attached = False
    _tx_seq = 0
    _host_addr = ['localhost', 7701] # list, to be converted to a tuple
    _local_port = 0 # let the OS decide the best local port

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

    # QSPY UDP socket poll interval [ms]
    _POLLI = 10

    # tuple of QS records from the Target.
    # !!! NOTE: Must match qs_copy.h !!!
    _QS = ('QS_EMPTY',
        # [1] SM records
        'QS_QEP_STATE_ENTRY',
        'QS_QEP_STATE_EXIT',
        'QS_QEP_STATE_INIT',
        'QS_QEP_INIT_TRAN',
        'QS_QEP_INTERN_TRAN',
        'QS_QEP_TRAN',
        'QS_QEP_IGNORED',
        'QS_QEP_DISPATCH',
        'QS_QEP_UNHANDLED',

        # [10] Active Object (AO) records
        'QS_QF_ACTIVE_DEFER',
        'QS_QF_ACTIVE_RECALL',
        'QS_QF_ACTIVE_SUBSCRIBE',
        'QS_QF_ACTIVE_UNSUBSCRIBE',
        'QS_QF_ACTIVE_POST',
        'QS_QF_ACTIVE_POST_LIFO',
        'QS_QF_ACTIVE_GET',
        'QS_QF_ACTIVE_GET_LAST',
        'QS_QF_ACTIVE_RECALL_ATTEMPT',

        # [19] Event Queue (EQ) records
        'QS_QF_EQUEUE_POST',
        'QS_QF_EQUEUE_POST_LIFO',
        'QS_QF_EQUEUE_GET',
        'QS_QF_EQUEUE_GET_LAST',

        'QS_QF_RESERVED2',

        # [24] Memory Pool (MP) records
        'QS_QF_MPOOL_GET',
        'QS_QF_MPOOL_PUT',

        # [26] QF records
        'QS_QF_PUBLISH',
        'QS_QF_NEW_REF',
        'QS_QF_NEW',
        'QS_QF_GC_ATTEMPT',
        'QS_QF_GC',
        'QS_QF_TICK',

        # [32] Time Event (TE) records
        'QS_QF_TIMEEVT_ARM',
        'QS_QF_TIMEEVT_AUTO_DISARM',
        'QS_QF_TIMEEVT_DISARM_ATTEMPT',
        'QS_QF_TIMEEVT_DISARM',
        'QS_QF_TIMEEVT_REARM',
        'QS_QF_TIMEEVT_POST',

        # [38] Additional QF records
        'QS_QF_DELETE_REF',
        'QS_QF_CRIT_ENTRY',
        'QS_QF_CRIT_EXIT',
        'QS_QF_ISR_ENTRY',
        'QS_QF_ISR_EXIT',
        'QS_QF_INT_DISABLE',
        'QS_QF_INT_ENABLE',

        # [45] Additional Active Object (AO) records
        'QS_QF_ACTIVE_POST_ATTEMPT',

        # [46] Additional Event Queue (EQ) records
        'QS_QF_EQUEUE_POST_ATTEMPT',

        # [47] Additional Memory Pool (MP) records
        'QS_QF_MPOOL_GET_ATTEMPT',

        # [48] Scheduler (SC) records
        'QS_MUTEX_LOCK',
        'QS_MUTEX_UNLOCK',
        'QS_SCHED_LOCK',
        'QS_SCHED_UNLOCK',
        'QS_SCHED_NEXT',
        'QS_SCHED_IDLE',
        'QS_SCHED_RESUME',

        # [55] Additional QEP records
        'QS_QEP_TRAN_HIST',
        'QS_QEP_TRAN_EP',
        'QS_QEP_TRAN_XP',

        # [58] Miscellaneous QS records (not maskable)
        'QS_TEST_PAUSED',
        'QS_TEST_PROBE_GET',
        'QS_SIG_DICT',
        'QS_OBJ_DICT',
        'QS_FUN_DICT',
        'QS_USR_DICT',
        'QS_TARGET_INFO',
        'QS_TARGET_DONE',
        'QS_RX_STATUS',
        'QS_QUERY_DATA',
        'QS_PEEK_DATA',
        'QS_ASSERT_FAIL',

        # [70] Reserved QS records
        'QS_RESERVED_70',
        'QS_RESERVED_71',
        'QS_RESERVED_72',
        'QS_RESERVED_73',
        'QS_RESERVED_74',
        'QS_RESERVED_75',
        'QS_RESERVED_76',
        'QS_RESERVED_77',
        'QS_RESERVED_78',
        'QS_RESERVED_79',
        'QS_RESERVED_80',
        'QS_RESERVED_81',
        'QS_RESERVED_82',
        'QS_RESERVED_83',
        'QS_RESERVED_84',
        'QS_RESERVED_85',
        'QS_RESERVED_86',
        'QS_RESERVED_87',
        'QS_RESERVED_88',
        'QS_RESERVED_89',
        'QS_RESERVED_90',
        'QS_RESERVED_91',
        'QS_RESERVED_92',
        'QS_RESERVED_93',
        'QS_RESERVED_94',
        'QS_RESERVED_95',
        'QS_RESERVED_96',
        'QS_RESERVED_97',
        'QS_RESERVED_98',
        'QS_RESERVED_99',

        # [100] Application-specific (User) QS records
        'QS_USER_00',
        'QS_USER_01',
        'QS_USER_02',
        'QS_USER_03',
        'QS_USER_04',
        'QS_USER_05',
        'QS_USER_06',
        'QS_USER_07',
        'QS_USER_08',
        'QS_USER_09',
        'QS_USER_10',
        'QS_USER_11',
        'QS_USER_12',
        'QS_USER_13',
        'QS_USER_14',
        'QS_USER_15',
        'QS_USER_16',
        'QS_USER_17',
        'QS_USER_18',
        'QS_USER_19',
        'QS_USER_20',
        'QS_USER_21',
        'QS_USER_22',
        'QS_USER_23',
        'QS_USER_24')

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

    # packets to QSpy to be "massaged" and forwarded to the Target...
    QSPY_SEND_EVENT      = 135
    QSPY_SEND_LOC_FILTER = 136
    QSPY_SEND_CURR_OBJ   = 137
    QSPY_SEND_COMMAND    = 138
    QSPY_SEND_TEST_PROBE = 139

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
    OBJ_SM = 0
    OBJ_AO = 1
    OBJ_MP = 2
    OBJ_EQ = 3
    OBJ_TE = 4
    OBJ_AP = 5
    OBJ_SM_AO = 6

    # special event sub-commands for QSPY_SEND_EVENT
    EVT_PUBLISH   = 0
    EVT_POST      = 253
    EVT_INIT      = 254
    EVT_DISPATCH  = 255

    @staticmethod
    def _init():
        # Create socket
        QSpy._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        QSpy._sock.setblocking(0) # NON-BLOCKING socket
        try:
            QSpy._sock.bind(('localhost', QSpy._local_port))
        except:
            messagebox.showerror("UDP Socket Error",
               "Can't bind the UDP socket\n"
               "to the specified local_host.\n"
               "Check if other instances of qspyview\n"
               "or qutest are running...")
            QView._quit(-1)
            return -1
        return 0

    @staticmethod
    def _attach():
        QSpy._is_attached = False
        if QView._echo_text.get():
            channels = 0x3
        else:
            channels = 0x1
        QSpy.sendTo(pack('<BB', QSpy._QSPY_ATTACH, channels))
        QSpy._attach_ctr = 50
        QView._gui.after(1, QSpy._poll0) # start poll0

    @staticmethod
    def _detach():
        if QSpy._sock is None:
            return
        QSpy.sendTo(pack('<B', QSpy._QSPY_DETACH))
        time.sleep(0.25) # let the socket finish sending the packet
        #QSpy._sock.shutdown(socket.SHUT_RDWR)
        QSpy._sock.close()
        QSpy._sock = None

    @staticmethod
    def _reattach():
        # channels: 0x1-binary, 0x2-text, 0x3-both
        if QView._echo_text.get():
            channels = 0x3
        else:
            channels = 0x1
        QSpy.sendTo(pack('<BB', QSpy._QSPY_ATTACH, channels))

    @staticmethod
    def _poll0():
        ''' poll the UDP socket until the QSpy confirms ATTACH '''
        #print("poll0 ", QSpy._attach_ctr)
        QSpy._attach_ctr -= 1
        if QSpy._attach_ctr == 0:
            if QView._attach_dialog is None:
                QView._AttachDialog() # launch the AttachDialog
            return

        try:
            packet = QSpy._sock.recv(4096)
            if not packet:
                messagebox.showerror("UDP Socket Error",
                   'Connection closed by QSpy')
                QView._quit(-1)
                return
        except OSError: # non-blocking socket...
            QView._gui.after(QSpy._POLLI, QSpy._poll0)
            return # <======== no packet at this time
        except:
            messagebox.showerror("UDP Socket Error",
               'Uknown UDP socket error')
            QView._quit(-1)
            return

        # parse the packet...
        dlen = len(packet)
        if dlen < 2:
            messagebox.showerror("Communication Error",
               'UDP packet from QSpy too short')
            QView._quit(-2)
            return

        recID = packet[1]
        if recID == QSpy._PKT_ATTACH_CONF:
            QSpy._is_attached = True
            if QView._attach_dialog is not None:
                QView._attach_dialog.close()

            # send target-info request (keep the poll0 loop running)
            QView._have_info = False
            QSpy.sendTo(pack('<B', QSpy._TRGT_INFO))

            # switch to the regular polling...
            QView._gui.after(QSpy._POLLI, QSpy._poll)
            return

        elif recID == QSpy._PKT_DETACH:
            QView._quit()
            return


    @staticmethod
    def _poll():
        ''' regullar poll of the UDP socket after it has attached '''

        while True:
            try:
                packet = QSpy._sock.recv(4096)
                if not packet:
                    messagebox.showerror("UDP Socket Error",
                       'Connection closed by QSpy')
                    QView._quit(-1)
                    return
            except OSError: # non-blocking socket...
                QView._gui.after(QSpy._POLLI, QSpy._poll)
                return # <============= no packet at this time
            except:
                messagebox.showerror("UDP Socket Error",
                   'Uknown UDP socket error')
                QView._quit(-1)
                return

            # parse the packet...
            dlen = len(packet)
            if dlen < 2:
                messagebox.showerror("UDP Socket Data Error",
                   'UDP packet from QSpy too short')
                QView._quit(-2)
                return

            recID = packet[1]
            if recID == QSpy._PKT_TEXT_ECHO:
                # no need to check QView._echo_text.get()
                # because the text channel is closed
                QView.dispTxt(packet[3:])

            elif recID == QSpy._PKT_TARGET_INFO:
                if dlen != 18:
                    messagebox.showerror("UDP Socket Data Error",
                       'Corrupted Target-info')
                    QView._quit(-2)
                    return

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
                fmt_targetTstamp = 'Target: %02d%02d%02d_%02d%02d%02d'\
                    %(tstamp[12], tstamp[11], tstamp[10],
                      tstamp[9], tstamp[8], tstamp[7])
                #print('******* Target:', fmt_targetTstamp)
                QView._target.configure(text=fmt_targetTstamp)
                QView._have_info = True

            elif recID == QSpy._PKT_DETACH:
                QView._quit()
                return

            elif recID <= 124: # other binary data
                    # find the (global) handler for the packet
                    handler = getattr(QView._cust,
                                      QSpy._QS[recID], None)
                    if handler is not None:
                        try:
                            handler(packet) # call the packet handler
                        except:
                            messagebox.showerror('Runtime Error',
                               traceback.format_exc(3))
                            QView._quit(-3)
                            return

    @staticmethod
    def sendTo(packet, str=None):
        tx_packet = bytearray([QSpy._tx_seq])
        tx_packet.extend(packet)
        if str is not None:
            tx_packet.extend(bytes(str, 'utf-8'))
            tx_packet.extend(b'\0') # zero-terminate
        QSpy._sock.sendto(tx_packet, QSpy._host_addr)
        QSpy._tx_seq = (QSpy._tx_seq + 1) & 0xFF
        #print('sendTo', QSpy._tx_seq)

    @staticmethod
    def sendEvt(ao_prio, signal, parameters = None):
        fmt = '<BB' + QSpy.fmt_sig + 'H'
        if parameters is not None:
            length = len(parameters)
        else:
            length = 0

        if isinstance(signal, int):
            packet = bytearray(pack(
                fmt, QSpy._TRGT_EVENT, ao_prio, signal, length))
            if parameters is not None:
                packet.extend(parameters)
            QSpy.sendTo(packet)
        else:
            packet = bytearray(pack(
                fmt, QSpy.QSPY_SEND_EVENT, ao_prio, 0, length))
            if parameters is not None:
                packet.extend(parameters)
            QSpy.sendTo(packet, signal)

    @staticmethod
    def command(cmdId, param1 = 0, param2 = 0, param3 = 0):
        fmt = '<BBIII'
        if isinstance(cmdId, int):
            QSpy.sendTo(pack(fmt, QSpy._TRGT_COMMAND,
                             cmdId, param1, param2, param3))
        else:
            QSpy.sendTo(pack(fmt, QSpy.QSPY_SEND_COMMAND,
                             0, param1, param2, param3),
                cmdId) # add string command ID to end

    @staticmethod
    def current_obj(obj_kind, obj_id):
        fmt = '<BB' + QSpy.fmt_objPtr
        # Build packet according to obj_id type
        if isinstance(obj_id, int):
            QSpy.sendTo(pack(fmt, QSpy._TRGT_CURR_OBJ, obj_kind, obj_id))
        else:
            QSpy.sendTo(pack(fmt, QSpy.QSPY_SEND_CURR_OBJ, obj_kind, 0),
                obj_id) # add string object ID to end


#=============================================================================
# main entry point to QView
def _main(argv):
    # process command-line arguments...
    argc = len(argv)
    arg  = 1 # skip the 'qspyview' argument

    if '-h' in argv or '--help' in argv or '?' in argv:
        print('\nUsage: python qspyview.py [custom-script] '
            '[qspy_host[:udp_port]] [local_port]\n\n'
            'help at: https://www.state-machine.com/qtools/qspyview.html')
        return 0

    script = ''
    if arg < argc:
        # is the next argument a test script?
        if argv[arg].endswith('.py'):
            script = argv[arg]
            arg += 1

        if arg < argc:
            host_port = argv[arg].split(':')
            arg += 1
            if len(host_port) > 0:
                QSpy._host_addr[0] = host_port[0]
            if len(host_port) > 1:
                QSpy._host_addr[1] = int(host_port[1])

        if arg < argc:
            QSpy._local_port = int(argv[arg])

    QSpy._host_addr = tuple(QSpy._host_addr) # convert to immutable tuple
    #print("Connection: ", QSpy._host_addr, QSpy._local_port)

    # create the QView GUI
    QView._gui = Tk()
    QView._gui.title('QView ' + \
        '%d.%d.%d'%(QView.VERSION//100, \
                   (QView.VERSION//10) % 10, \
                    QView.VERSION % 10) + ' -- ' + script)
    QView._init_gui()

    # extend the QView with a custom sript
    if script != '':
        try:
            f = open(script)

            # set the home directory of the custom script
            # (might be needed inside the script)
            QView.home_dir = os.path.dirname(os.path.realpath(script))

            code = compile(f.read(), script, 'exec')
            exec(code) # execute the script
            f.close()
        except: # error opening the file or error in the script
            messagebox.showerror('Error in ' + script,
               traceback.format_exc(3))
            return -4 # simple return: event-loop is not running yet

    QView._err = QSpy._init()
    if QView._err:
        return QView._err # simple return: event-loop is not running yet

    QSpy._attach()
    QView._gui.mainloop()
    QSpy._detach()

    return QView._err

#=============================================================================
if __name__ == '__main__':
    sys.exit(_main(sys.argv))

