import path from 'node:path'
import { openDirectory } from '@main/openDirectory'
import { describe, expect, it, vi } from 'vitest'

const { showOpenDialog } = vi.hoisted(() => ({
  showOpenDialog: vi.fn(),
}))

vi.mock('electron', () => ({
  dialog: { showOpenDialog },
}))

describe('openDirectory', () => {
  it('reopens the dialog in the last used directory', async () => {
    const file = path.join('photos', 'cat.png')
    showOpenDialog.mockResolvedValueOnce({
      canceled: false,
      filePaths: [file],
    })
    showOpenDialog.mockResolvedValueOnce({ canceled: true, filePaths: [] })

    expect(await openDirectory(null, ['openFile'])).toEqual([file])
    expect(await openDirectory(null, ['openDirectory'])).toEqual([])

    expect(showOpenDialog).toHaveBeenNthCalledWith(1, {
      defaultPath: undefined,
      properties: ['openFile'],
    })
    expect(showOpenDialog).toHaveBeenNthCalledWith(2, {
      defaultPath: 'photos',
      properties: ['openDirectory'],
    })
  })
})
