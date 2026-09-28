import type { Precision } from '@shared/type/core'
import type { Ref } from 'vue'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSRSettingsStore = defineStore(
  'SRSettings',
  () => {
    const selectedSRModel = ref('RealESRGAN_RealESRGAN_x2plus_2x.pth')
    const selectedTorchDevice = ref('auto')
    const ghProxy: Ref<string | null> = ref(null)
    const targetScale: Ref<number | null> = ref(null)
    const useTile: Ref<boolean> = ref(true)
    const precision: Ref<Precision> = ref('fp32')
    const saveFormat: Ref<string> = ref('.png')

    return {
      selectedSRModel,
      selectedTorchDevice,
      ghProxy,
      targetScale,
      useTile,
      precision,
      saveFormat,
    }
  },
  {
    persist: true,
  },
)
