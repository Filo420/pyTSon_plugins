import pytson, ts3lib, ts3defines
from ts3plugin import ts3plugin, PluginHost
from datetime import datetime
from bluscream import timestamp, channelURL, clientURL

class rewinsideTV(ts3plugin):
    name = "Rewi nifty tricks"
    apiVersion = 22
    requestAutoload = False
    version = "1.0"
    author = "Bluscream"
    description = ""
    offersConfigure = False
    commandKeyword = ""
    infoTitle = None
    hotkeys = []
    menuItems = []
    suid = "9Sx6wrlRV4i9klBiTanrksNFKvs="
    waiting = {}
    mychan = 0

    def __init__(self):
        schid = ts3lib.getCurrentServerConnectionHandlerID()
        err, clid = ts3lib.getClientID(schid)
        (err, cgid) = ts3lib.getClientVariable(schid, clid, ts3defines.ClientPropertiesRare.CLIENT_CHANNEL_GROUP_ID)
        # ts3lib.printMessageToCurrentTab("{}".format(cgid))
        if cgid == 9:
            err, cid = ts3lib.getChannelOfClient(schid, clid)
            self.mychan = cid
            ts3lib.printMessageToCurrentTab("{} > New channel is {}".format(self.name, channelURL(schid, cid)))
        if PluginHost.cfg.getboolean("general", "verbose"): ts3lib.printMessageToCurrentTab("{0}[color=orange]{1}[/color] Plugin for pyTSon by [url=https://github.com/{2}]{2}[/url] loaded.".format(timestamp(),self.name,self.author))

    def onClientMoveEvent(self, schid, clientID, oldChannelID, newChannelID, visibility, moveMessage):
        if self.mychan == 0: return
        (err, suid) = ts3lib.getServerVariable(schid, ts3defines.VirtualServerProperties.VIRTUALSERVER_UNIQUE_IDENTIFIER)
        if suid != self.suid: return
        (err, ownID) = ts3lib.getClientID(schid)
        if clientID == ownID: return
        if clientID in self.waiting and (newChannelID == 0 or newChannelID == self.mychan):
            ts3lib.printMessageToCurrentTab("{} > Removing {} from self.waiting".format(self.name, clientID))
            ts3lib.requestSetClientChannelGroup(schid, [10], [self.mychan], [self.waiting[clientID]])
            del self.waiting[clientID]
            return
        if newChannelID == 0: return
        (err, sgroups) = ts3lib.getClientVariableAsString(schid, clientID, ts3defines.ClientPropertiesRare.CLIENT_SERVERGROUPS)
        # (err2, errmsg) = ts3lib.getErrorMessage(err)
        if oldChannelID != 0: return
        if "10" in sgroups.split(','):
            (err, dbid) = ts3lib.getClientVariable(schid, clientID, ts3defines.ClientPropertiesRare.CLIENT_DATABASE_ID)
            self.waiting[clientID] = dbid
            ts3lib.printMessageToCurrentTab("{} > #{} Found new guest {} ({}) giving him channel mod until he's here ;)".format(self.name, schid, clientURL(schid, clientID), dbid))
            ts3lib.requestSetClientChannelGroup(schid, [14], [self.mychan], [dbid])
            return

    def onClientChannelGroupChangedEvent(self, schid, channelGroupID, channelID, clientID, invokerClientID, invokerName, invokerUniqueIdentity):
        (err, suid) = ts3lib.getServerVariable(schid, ts3defines.VirtualServerProperties.VIRTUALSERVER_UNIQUE_IDENTIFIER)
        if suid != self.suid: return
        (err, ownID) = ts3lib.getClientID(schid)
        if clientID == ownID:
            if channelGroupID == 9:
                self.mychan = channelID
                ts3lib.printMessageToCurrentTab("{} > New channel is {}".format(self.name, channelURL(schid, channelID)))
            else: self.mychan = 0
            return
