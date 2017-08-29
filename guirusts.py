#!/usr/bin/python2

import os
import wx
import valve.source.a2s
import ConfigParser
import io
import gi

gi.require_version('Notify', '0.7')
from gi.repository import Notify

Notify.init("Hello World!")

TRAY_TOOLTIP = 'Rusts.py'
TRAY_ICON = 'rusticon16x16.png'
CONFIG_FILE = "config.cfg"

players_list = []


def config_load():
    if not os.path.isfile(CONFIG_FILE):
        # Create file if not existing
        cfgfile = open(CONFIG_FILE, 'w')
        # Add content to the file
        Config = ConfigParser.ConfigParser()
        Config.add_section('app')
        Config.set('app', 'mode', 'all')
        Config.set('app', '; mode', 'all or blacklist')
        Config.set('app', 'server', '163.172.17.175')
        Config.set('app', 'port', '30616')
        Config.set('app', 'alarmsound', False)
        Config.set('app', 'alarmsoundpath', '')
        Config.add_section('blacklist')
        Config.set('blacklist', '; names', 'Only in use if blacklist active')
        Config.set('blacklist', 'names', 'example1:example2:example3')
        Config.write(cfgfile)
        cfgfile.close()
    with open(CONFIG_FILE) as f:
        configread = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(configread))
        #print(config.get('blacklist', 'names').split(':'))
        # print(config.get('blacklist'))
        return config


def playerList():
    config = config_load()
    server = valve.source.a2s.ServerQuerier((unicode(config.get('app', 'server')), config.getint('app', 'port')))
    players = server.players()

    for p in players['players']:
        if p["name"]:
            players_list.append(p["name"])


def create_menu_item(menu, label, func, menu_id=-1):
    item = wx.MenuItem(menu, menu_id, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)
        # self.timer = wx.Timer(self, 1)
        # self.Bind(wx.EVT_TIMER, self.OnTimer)

        # self.timer.Start(1000)    # 1 second interval

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Server name (1/10)', None, 100)
        menu.Enable(100, False)
        menu.AppendSeparator()
        create_menu_item(menu, 'List', self.on_toggle)
        menu.AppendSeparator()
        create_menu_item(menu, 'Conf', self.on_toggle)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    # def performance_mode(self):
    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def send_notification(self, text):
        notification = Notify.Notification.new("Active power mode", text)
        notification.show()

    def on_left_click(self, path):
        global players_list
        players_list = []
        playerList()
        print(players_list)
        dlg = wx.MessageDialog(None, '\n'.join(players_list), 'Players list', wx.OK | wx.ICON_NONE | wx.STAY_ON_TOP)
        result = dlg.ShowModal()

    def on_toggle(self, event):
        print("Hello world")

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def OnTimer(self, event):
        # do whatever you want to do every second here
        print('Hello')


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)

        return True


def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
