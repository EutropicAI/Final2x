import type { Final2xCoreConfig } from '@shared/type/core'
import { useGlobalSettingsStore } from '@renderer/store/globalSettingsStore'
import { storeToRefs } from 'pinia'
import { useSRSettingsStore } from '../store/SRSettingsStore'
import PathFormat from '../utils/pathFormat'
import IOPath from './IOPath'

/**
 * @description: 返回输出路径，如果输出路径不合法，则从第一个输入路径构造一个合法输出路径
 */
function getOutPutPATH(): string {
  if (!PathFormat.checkPath(IOPath.getoutputpath())) {
    const inputPATHList = IOPath.getList()
    const pathFormat = new PathFormat()
    pathFormat.setRootPath(inputPATHList[0])
    IOPath.setoutputpath(pathFormat.getRootPath())
  }
  return IOPath.getoutputpath()
}

/**
 * @description: 返回最终的json字符串配置文件
 */
export function getFinal2xCoreConfig(): Final2xCoreConfig {
  const { selectedSRModel, ghProxy, targetScale, selectedTorchDevice, useTile, precision, saveFormat } = storeToRefs(useSRSettingsStore())
  const { openOutputFolder } = storeToRefs(useGlobalSettingsStore())

  const inputPATHList = IOPath.getList()
  const outputPATH = getOutPutPATH()

  let _gh_proxy: string | null
  if (ghProxy.value === '') {
    _gh_proxy = null
  }
  else {
    _gh_proxy = ghProxy.value
  }

  return {
    config: {
      pretrained_model_name: selectedSRModel.value,
      device: selectedTorchDevice.value,
      gh_proxy: _gh_proxy,
      target_scale: targetScale.value,
      output_path: outputPATH,
      input_path: inputPATHList,
      use_tile: useTile.value,
      precision: precision.value,
      save_format: saveFormat.value,
    },
    options: {
      open_output_folder: openOutputFolder.value,
    },
  }
}
