import { useSRSettingsStore } from '@renderer/store/SRSettingsStore'
import { getFinal2xCoreConfig } from '@renderer/utils/getFinal2xCoreConfig'
import IOPath from '@renderer/utils/IOPath'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'

describe('precision configuration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    IOPath.add('test-image', '/tmp/image.png')
    IOPath.setoutputpathManual('/tmp')
  })

  it('sends the default FP32 mode to the core', () => {
    expect(getFinal2xCoreConfig().config.precision).toBe('fp32')
  })

  it('sends the selected FP16 mode to the core', () => {
    useSRSettingsStore().precision = 'fp16'
    expect(getFinal2xCoreConfig().config.precision).toBe('fp16')
  })

  it('sends the selected BF16 mode to the core', () => {
    useSRSettingsStore().precision = 'bf16'
    expect(getFinal2xCoreConfig().config.precision).toBe('bf16')
  })
})
