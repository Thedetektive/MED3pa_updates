const { contextBridge, ipcRenderer } = require('electron')

const handler = {
  invoke(channel, ...args) {
    return ipcRenderer.invoke(channel,...args);
  },
  send(channel, value) {
    ipcRenderer.send(channel, value)
  },
  on(channel, callback) {
    const subscription = (_event, ...args) => callback(...args)
    ipcRenderer.on(channel, subscription)

    return () => {
      ipcRenderer.removeListener(channel, subscription)
    }
  },

}

contextBridge.exposeInMainWorld('ipc', handler)
