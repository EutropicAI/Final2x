import { registerIpcHandlers } from '@main/registerIpcHandlers'
import { IpcChannelInvoke, IpcChannelSend } from '@shared/const/ipc'
import { describe, expect, it, vi } from 'vitest'

const { on, handle, fromWebContents } = vi.hoisted(() => ({
  on: vi.fn(),
  handle: vi.fn(),
  fromWebContents: vi.fn(),
}))

vi.mock('electron', () => ({
  app: { hide: vi.fn(), quit: vi.fn() },
  BrowserWindow: { fromWebContents },
  ipcMain: { on, handle },
}))
vi.mock('@main/runCommand', () => ({ runCommand: vi.fn(), killCommand: vi.fn() }))
vi.mock('@main/openDirectory', () => ({ openDirectory: vi.fn() }))

describe('registerIpcHandlers', () => {
  it('registers each channel only once when a window is recreated', () => {
    registerIpcHandlers()
    registerIpcHandlers()

    expect(handle.mock.calls.filter(([channel]) => channel === IpcChannelInvoke.OPEN_DIRECTORY_DIALOG)).toHaveLength(1)
    for (const channel of Object.values(IpcChannelSend)) {
      expect(on.mock.calls.filter(([registeredChannel]) => registeredChannel === channel)).toHaveLength(1)
    }
  })

  it('uses the sender window rather than a closed window', () => {
    registerIpcHandlers()
    const minimize = on.mock.calls.find(([channel]) => channel === IpcChannelSend.MINIMIZE)?.[1]
    const maximize = on.mock.calls.find(([channel]) => channel === IpcChannelSend.MAXIMIZE)?.[1]
    const sender = {}
    const newWindow = { minimize: vi.fn(), isMaximized: vi.fn(() => false), maximize: vi.fn(), restore: vi.fn() }
    fromWebContents.mockReturnValue(newWindow)

    minimize({ sender })
    maximize({ sender })
    expect(fromWebContents).toHaveBeenCalledWith(sender)
    expect(newWindow.minimize).toHaveBeenCalledOnce()
    expect(newWindow.maximize).toHaveBeenCalledOnce()
  })
})
