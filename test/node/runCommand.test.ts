import type { Final2xCoreConfig } from '@shared/type/core'
import type { IpcMainEvent } from 'electron'
import { runCommand } from '@main/runCommand'
import { IpcChannelOn } from '@shared/const/ipc'
import { describe, expect, it, vi } from 'vitest'

vi.mock('@main/getCorePath', () => ({
  getCorePath: (): string => `Final2x-core-missing-for-test-${process.pid}`,
  getCoreArgs: (): string[] => [],
}))

describe('runCommand', () => {
  it('reports a missing core executable and unlocks the renderer', async () => {
    const send = vi.fn()
    const event = { sender: { send } } as unknown as IpcMainEvent
    const coreConfig: Final2xCoreConfig = {
      config: {
        pretrained_model_name: 'test.pth',
        device: 'cpu',
        gh_proxy: null,
        target_scale: null,
        output_path: '.',
        input_path: [],
        use_tile: false,
        save_format: '.png',
      },
      options: { open_output_folder: false },
    }

    await runCommand(event, coreConfig)

    expect(send).toHaveBeenCalledWith(IpcChannelOn.COMMAND_STDERR, expect.stringContaining('ENOENT'))
    expect(send).toHaveBeenCalledWith(IpcChannelOn.COMMAND_CLOSE, 1)
  })
})
