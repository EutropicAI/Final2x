// download Final2x-core from https://github.com/EutropicAI/Final2x-core/releases
// and put it in resources folder

const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args))
const child_process = require('node:child_process')
const fs = require('node:fs')

const path = require('node:path')

const coreDict = {
  'macos-arm64':
    'https://github.com/EutropicAI/Final2x-core/releases/download/2025-08-15/Final2x-core-macos-arm64.7z',
  'windows-x64':
    'https://github.com/EutropicAI/Final2x-core/releases/download/2025-08-15/Final2x-core-windows-x64.7z',
}

console.log('-'.repeat(50))

// 判断当前平台
const PLATFORM = process.env.PLATFORM || process.platform
// 判断当前平台架构
const ARCH = process.env.ARCH || process.arch
console.log(`Platform: ${PLATFORM}`, `| Arch: ${ARCH}`)
if (process.env.SKIP_DOWNLOAD_CORE) {
  console.log('Skip download Final2x-core by env SKIP_DOWNLOAD_CORE')
  process.exit(0)
}

async function downloadAndUnzip(url, targetPath) {
  const zipFileName = path.basename(url)
  const zipFilePath = path.join(targetPath, zipFileName)

  const res = await fetch(url)
  const dest = fs.createWriteStream(zipFilePath)

  dest.on('finish', () => {
    console.log(`Download ${zipFileName} success!`)
    // 解压缩文件, 命令行调用 7z
    const Final2xCorePath = path.join(targetPath, 'Final2x-core')
    const unzipCmd = `7z x ${zipFilePath} -o${Final2xCorePath}`
    console.log(`Unzip command: ${unzipCmd}`)
    // 使用异步方式执行解压命令
    child_process.exec(unzipCmd, (error) => {
      if (error) {
        console.error(`Unzip error: ${error}`)
        return
      }
      console.log(`Unzip ${zipFileName} success!`)
      // 删除压缩文件
      fs.unlinkSync(zipFilePath)
      console.log(`Delete ${zipFileName} success!`)
    })
  })

  res.body.pipe(dest)
}

async function downloadAndUnzipCore(platform) {
  const url = coreDict[platform]
  if (!url) {
    console.error('Invalid platform')
    return
  }

  const targetPath = path.join(__dirname)
  console.log(`Target path: ${targetPath}`)

  if (fs.existsSync(path.join(targetPath, 'Final2x-core'))) {
    console.log('Final2x-core already exists, skip download!')
    return
  }

  if (!fs.existsSync(targetPath)) {
    fs.mkdirSync(targetPath, { recursive: true })
  }

  await downloadAndUnzip(url, targetPath)
}

// 选择要下载的平台
let platformToDownload = ''
if (PLATFORM === 'darwin') {
  platformToDownload = ARCH === 'arm64' ? 'macos-arm64' : 'macos-x64'
}
else if (PLATFORM === 'linux') {
  console.error('Skip download Final2x-core for linux! Please use pip to install Final2x-core')
  process.exit(0)
}
else if (PLATFORM === 'win32') {
  platformToDownload = 'windows-x64'
}
else {
  console.error('Unsupported platform!')
  process.exit(1)
}

console.log(`Downloading Final2x-core for ${platformToDownload}...`)
// 执行下载和解压
downloadAndUnzipCore(platformToDownload)
  .then()
  .catch((err) => {
    console.error(err)
  })
