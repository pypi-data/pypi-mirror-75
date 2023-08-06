# -*- coding: iso-8859-1 -*-
# main.py - qt5-based hg rev log browser
#
# Copyright (C) 2007-2010 Logilab. All rights reserved.
#
# This software may be used and distributed according to the terms
# of the GNU General Public License, incorporated herein by reference.
"""
Help window for hgview
"""

import re

from PyQt5 import QtCore, QtGui, QtWidgets

from hgviewlib.util import tohg
from hgviewlib.qt5.mixins import HgDialogMixin, ui2cls
from hgviewlib.hgviewhelp import help_msg, get_options_helpmsg

Qt = QtCore.Qt
bold = QtGui.QFont.Bold

try:
    from docutils.core import publish_string
except:
    def publish_string(s, *args, **kwargs):
        return s


class HelpViewer(HgDialogMixin, ui2cls('helpviewer.ui'), QtWidgets.QDialog):
    """hgview simple help viewer"""
    def __init__(self, repo, rest, parent=None):
        self.repo = repo
        super(HelpViewer, self).__init__(parent)
        self.load_ui()
        self.load_config(repo)
        self.set_text(rest)
        self.textBrowser.anchorClicked.connect(self.anchor_clicked)

    def set_text(self, rest):
        formated_text = publish_string(rest, writer_name='html', settings_overrides={'output_encoding': 'unicode'})
        self.textBrowser.setText(formated_text)

    def anchor_clicked(self, qurl):
        """Callback called when a link is clicked in the text browser"""
        QtGui.QDesktopServices.openUrl(qurl)

    # must be redefined cause it's a QDialog
    def accept(self):
        QtWidgets.QDialog.accept(self)

    def reject(self):
        QtWidgets.QDialog.reject(self)

class HgHelpViewer(HelpViewer):
    """Display a Mercurial help topic and allow to navigate in hg topics"""
    def __init__(self, repo, topic, parent=None):
        super(HgHelpViewer, self).__init__(repo, self.get_hg_helper(topic), parent)

    def set_text(self, rest):
        # handle cross hg doc references with special url
        for reference in re.findall(':hg:`.*?`', rest):
            topic = reference[5:-1]
            if not self.get_hg_helper(topic):
                rest = re.sub(reference, '*%s*' % topic, rest)
            else:
                rest = re.sub(reference, '`%s <hg://%s>`_'%(topic,topic), rest)
        formated_text = publish_string(rest, writer_name='html', settings_overrides={'output_encoding': 'unicode'})
        self.textBrowser.setText(formated_text)

    def anchor_clicked(self,qurl):
        """Callback called when a link is clicked in the text browser"""
        topic = qurl.toString()
        if topic.startswith('hg://'):
            self.set_text(self.get_hg_helper(topic[5:]))
        else:
            QtGui.QDesktopServices.openUrl(qurl)

    @staticmethod
    def get_hg_helper(topic):
        topic = tohg(topic)
        from mercurial import help, cmdutil, commands, error
        try:
            rest = cmdutil.findcmd(topic, commands.table, strict=False)[1][0]()
        except (error.UnknownCommand, error.SignatureError,
                error.AmbiguousCommand, KeyError):
            try:
                rest = (f for n,h,f in help.helptable if topic in n).next()()
            except StopIteration:
                rest = None
        return rest


class HgviewHelpViewer(HelpViewer):
    def __init__(self, repo, parent=None):
        rest = help_msg + get_options_helpmsg(rest=True)
        super(HgviewHelpViewer, self).__init__(repo, rest, parent)
