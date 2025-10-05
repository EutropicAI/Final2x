<script lang="ts" setup>
import { IpcChannelInvoke } from '@shared/const/ipc'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { useGlobalSettingsStore } from '../store/globalSettingsStore'
import { useIOPathStore } from '../store/ioPathStore'
import { useSRSettingsStore } from '../store/SRSettingsStore'
import IOPath from '../utils/IOPath'
import { modelOptions } from '../utils/modelOptions'
import { saveFormatList, torchDeviceList } from '../utils/SROptions'

const { openOutputFolder }
  = storeToRefs(useGlobalSettingsStore())
const { selectedSRModel, ghProxy, targetScale, selectedTorchDevice, useTile, saveFormat, useCustomModelPath } = storeToRefs(useSRSettingsStore())
const { outputpath } = storeToRefs(useIOPathStore())
const { t } = useI18n()

function getPath(): void {
  const handleSelected = (_, path): void => {
    if (path[0] !== undefined) {
      // console.log(ioPath.getoutputpath())
      IOPath.setoutputpathManual(path[0])
    }
  }

  window.electron.ipcRenderer.invoke(IpcChannelInvoke.OPEN_DIRECTORY_DIALOG, ['openDirectory'])
    .then((path) => {
      handleSelected(null, path)
    })
    .catch((error) => {
      console.error('Error selecting directory:', error)
    })
}
</script>

<template>
  <n-card :bordered="false" class="settings-card">
    <n-space class="vertical" vertical justify="center">
      <n-space>
        <n-button dashed type="success" style="width: 80px">
          {{ t('Final2xSettings.text11') }}
        </n-button>
        <n-select
          v-model:value="selectedSRModel"
          :options="modelOptions"
          filterable
          tag
          clearable
          style="width: 465px"
        />
      </n-space>

      <n-space>
        <n-button dashed type="success" style="width: 80px">
          {{ t('Final2xSettings.text10') }}
        </n-button>

        <n-select
          v-model:value="selectedTorchDevice"
          :options="torchDeviceList"
          style="width: 150px"
        />

        <n-button dashed type="success" style="width: 120px">
          {{ t('Final2xSettings.text15') }}
        </n-button>

        <n-input-number
          v-model:value="targetScale"
          :max="99999999"
          :min="0"
          :step="0.2"
          :placeholder="t('Final2xSettings.text16')"
          style="width: 171px"
        />
      </n-space>

      <n-space>
        <n-button dashed type="success" style="width: 80px">
          {{ t('Final2xSettings.text19') }}
        </n-button>

        <n-select
          v-model:value="saveFormat"
          :options="saveFormatList"
          style="width: 150px"
        />

        <n-button dashed type="success" style="width: 120px">
          {{ t('Final2xSettings.text20') }}
        </n-button>

        <n-switch v-model:value="useTile" size="large" style="height: 35px; width: 76px">
          <template #checked>
            ON
          </template>
          <template #unchecked>
            OFF
          </template>
        </n-switch>
      </n-space>

      <n-space>
        <n-button dashed type="success" style="width: 80px">
          {{ t('Final2xSettings.text18') }}
        </n-button>

        <n-input
          v-model:value="ghProxy"
          placeholder="Github Proxy, Example: https://github.abskoop.workers.dev/"
          style="width: 465px"
        />
      </n-space>

      <n-space>
        <n-button round type="success" style="height: 35px; width: 150px" @click="getPath">
          {{ t('Final2xSettings.text17') }}
        </n-button>

        <n-switch v-model:value="openOutputFolder" size="large" style="height: 35px; width: 76px">
          <template #checked>
            OPEN
          </template>
        </n-switch>

        <n-input v-model:value="outputpath" :placeholder="outputpath" round style="width: 308px" />
      </n-space>
    </n-space>
  </n-card>
</template>

<style lang="scss" scoped>
.settings-card {
  width: fit-content;
  margin: 0 auto;
  height: 100%;
  // transparent
  background-color: rgba(255, 255, 255, 0);

  .vertical {
    height: 100%;

    > div {
      margin-bottom: 20px;
    }
  }
}
</style>
