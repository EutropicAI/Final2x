import { IpcChannelInvoke, IpcChannelSend } from '@shared/const/ipc'
import { app, BrowserWindow, ipcMain } from 'electron'
import { openDirectory } from './openDirectory'
import { killCommand, runCommand } from './runCommand'

let registered = false

export function registerIpcHandlers(): void {
  if (registered)
    return

  registered = true
  ipcMain.on(IpcChannelSend.EXECUTE_COMMAND, runCommand)
  ipcMain.on(IpcChannelSend.KILL_COMMAND, killCommand)
  ipcMain.handle(IpcChannelInvoke.OPEN_DIRECTORY_DIALOG, openDirectory)

  ipcMain.on(IpcChannelSend.MINIMIZE, (event) => {
    BrowserWindow.fromWebContents(event.sender)?.minimize()
  })

  ipcMain.on(IpcChannelSend.MAXIMIZE, (event) => {
    const window = BrowserWindow.fromWebContents(event.sender)
    if (window?.isMaximized())
      window.restore()
    else
      window?.maximize()
  })

  ipcMain.on(IpcChannelSend.CLOSE, () => {
    if (process.platform === 'darwin')
      app.hide()
    else
      app.quit()
  })
}
