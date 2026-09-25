import { spawnSync } from 'node:child_process'
import { checkPipPackage } from '@main/getCorePath'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('node:child_process', () => ({
  spawnSync: vi.fn(),
}))

describe('getFinal2xCorePath', () => {
  beforeEach(() => {
    vi.mocked(spawnSync).mockReset()
  })

  it('returns true when the pip package is available', () => {
    vi.mocked(spawnSync).mockReturnValue({ status: 0 } as ReturnType<typeof spawnSync>)

    expect(checkPipPackage()).toBe(true)
    expect(spawnSync).toHaveBeenCalledWith('Final2x-core', ['-h'])
  })

  it('returns false when the pip package is not available', () => {
    vi.mocked(spawnSync).mockReturnValue({ status: 1 } as ReturnType<typeof spawnSync>)

    expect(checkPipPackage()).toBe(false)
    expect(spawnSync).toHaveBeenCalledWith('Final2x-core', ['-h'])
  })
})
