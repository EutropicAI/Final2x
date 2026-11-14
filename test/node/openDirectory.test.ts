import path from 'node:path'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { showOpenDialog } = vi.hoisted(() => ({
  showOpenDialog: vi.fn(),
}))

vi.mock('electron', () => ({
  dialog: { showOpenDialog },
}))

async function loadOpenDirectory(): Promise<typeof import('@main/openDirectory').openDirectory> {
  return (await import('@main/openDirectory')).openDirectory
}

describe('openDirectory', () => {
  beforeEach(() => {
    vi.resetModules()
    showOpenDialog.mockReset()
  })

  it('reopens the dialog in the folder of the last selected file', async () => {
    const openDirectory = await loadOpenDirectory()
    const file = path.join('photos', 'cat.png')
    showOpenDialog.mockResolvedValueOnce({
      canceled: false,
      filePaths: [file],
    })
    showOpenDialog.mockResolvedValueOnce({ canceled: true, filePaths: [] })

    expect(await openDirectory(null, ['openFile'])).toEqual([file])
    expect(await openDirectory(null, ['openFile'])).toEqual([])

    expect(showOpenDialog).toHaveBeenNthCalledWith(1, {
      defaultPath: undefined,
      properties: ['openFile'],
    })
    expect(showOpenDialog).toHaveBeenNthCalledWith(2, {
      defaultPath: 'photos',
      properties: ['openFile'],
    })
  })

  it('reopens the dialog in the last selected folder', async () => {
    const openDirectory = await loadOpenDirectory()
    const first = path.join('photos', 'output')
    const second = path.join('photos', 'output', 'night')
    showOpenDialog.mockResolvedValueOnce({
      canceled: false,
      filePaths: [first],
    })
    showOpenDialog.mockResolvedValueOnce({
      canceled: false,
      filePaths: [second],
    })
    showOpenDialog.mockResolvedValueOnce({ canceled: true, filePaths: [] })

    expect(await openDirectory(null, ['openDirectory'])).toEqual([first])
    expect(await openDirectory(null, ['openDirectory'])).toEqual([second])
    expect(await openDirectory(null, ['openDirectory'])).toEqual([])

    expect(showOpenDialog).toHaveBeenNthCalledWith(1, {
      defaultPath: undefined,
      properties: ['openDirectory'],
    })
    expect(showOpenDialog).toHaveBeenNthCalledWith(2, {
      defaultPath: first,
      properties: ['openDirectory'],
    })
    expect(showOpenDialog).toHaveBeenNthCalledWith(3, {
      defaultPath: second,
      properties: ['openDirectory'],
    })
  })
})
