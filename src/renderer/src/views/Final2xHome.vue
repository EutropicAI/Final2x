<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'
import { IpcChannelInvoke } from '@shared/const/ipc'
import { FileImageOutlined } from '@vicons/antd'
import { useNotification } from 'naive-ui'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useIOPathStore } from '../store/ioPathStore'
import { getRandString } from '../utils'
import IOPath from '../utils/IOPath'
import PathFormat from '../utils/pathFormat'

const { t } = useI18n()
const notification = useNotification()
const useIOPath = useIOPathStore()
const { inputFileList } = storeToRefs(useIOPath)

const pathFormat = new PathFormat()

class Final2xHomeNotifications {
  static handleremove(s: string): void {
    notification.success({
      title: t('Final2xHome.text0'),
      content: s,
      duration: 1000,
    })
  }
}

function handleClickUpload(): void {
  const handleSelected = (_, path): void => {
    if (path !== undefined) {
      path.forEach((p: string) => {
        // 生成随机id
        let pathid = getRandString()
        while (IOPath.checkID(pathid)) {
          pathid = getRandString()
        }
        // console.log(pathid)
        // 插入 inputpathMap
        IOPath.add(pathid, p)
        // 插入 inputFileList
        inputFileList.value.push({
          fullPath: p,
          id: pathid,
          name: PathFormat.getFileName(p),
          percentage: 0,
          status: 'pending',
          thumbnailUrl: null,
          type: 'image',
          url: null,
        })
      })
    }
  }

  window.electron.ipcRenderer.invoke(IpcChannelInvoke.OPEN_DIRECTORY_DIALOG, ['openFile', 'multiSelections'])
    .then((path) => {
      handleSelected(null, path)
    })
    .catch((error) => {
      console.error('Error selecting file:', error)
    })
}

onMounted(() => {
  const dragWrapper = document.getElementById('file_drag')
  dragWrapper?.addEventListener('drop', (e) => {
    // 阻止默认行为
    e.preventDefault()
    // 获取文件列表
    const files = e.dataTransfer?.files

    if (files && files.length > 0) {
      const path = window.api.getPathForFile(files[0]) // Get file path, the path is absolute path, electron can use directly
      console.log(path)
      pathFormat.setRootPath(path)
      console.log(pathFormat.getRootPath())
      IOPath.setoutputpath(pathFormat.getRootPath())
    }
  })
  // 阻止拖拽结束事件默认行为
  dragWrapper?.addEventListener('dragover', (e) => {
    e.preventDefault()
  })
})

function handleUploadChange(data: { fileList: UploadFileInfo[] }): void {
  // console.log(data.fileList)
  // console.log(inputFileList.value)
  inputFileList.value = data.fileList
}

function handleBeforeUpload(options: { file: UploadFileInfo }): UploadFileInfo {
  // console.log(pathFormat.getNewPath(options.file.fullPath))
  IOPath.add(options.file.id, pathFormat.getNewPath(String(options.file.fullPath)))
  return options.file
}

function handleRemove(options: { file: UploadFileInfo, fileList: Array<UploadFileInfo> }): boolean {
  // console.log(ioPATH.show())
  // console.log(options.file.id)
  Final2xHomeNotifications.handleremove(IOPath.getByID(options.file.id))
  IOPath.delete(options.file.id)
  return true
}
</script>

<template>
  <div id="file_drag" class="for_file_drag" @click.prevent>
    <n-upload
      v-model:file-list="inputFileList"
      multiple
      directory-dnd
      class="n-upload"
      @remove="handleRemove"
      @before-upload="handleBeforeUpload"
      @change="handleUploadChange"
    >
      <n-upload-dragger class="file-drag-zone" @click="handleClickUpload">
        <div class="file-drag-zone-logo-text">
          <div style="margin-bottom: 12px">
            <n-icon size="48" depth="3.0">
              <FileImageOutlined />
            </n-icon>
          </div>
          <n-text style="font-size: 16px">
            {{ t('Final2xHome.text1') }}
          </n-text>
        </div>
      </n-upload-dragger>
    </n-upload>
  </div>
</template>

<style lang="scss" scoped>
.for_file_drag {
  width: 100%;
  height: 100%;
  padding: 0 12%;
  box-sizing: border-box;
  overflow: scroll;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  .file-drag-zone-logo-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
}

.n-upload {
  display: flex;
  flex-direction: column;
}

.n-upload :deep(.n-upload-file-list) {
  max-height: calc(100vh - 370px);
  overflow-y: auto;
  overflow-x: hidden;
  &::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  &::-webkit-scrollbar-track {
    border-radius: 3px;
    background: rgba(0, 0, 0, 0.06);
    -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.08);
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 3px;
    background: rgba(0, 0, 0, 0.12);
    -webkit-box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
  }
}
</style>
