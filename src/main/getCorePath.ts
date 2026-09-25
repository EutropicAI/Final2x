import { spawnSync } from 'node:child_process'
import path from 'node:path'
import { app } from 'electron'

/**
 * 获取 Final2x-core 的路径。
 * 开发模式直接通过 uv 运行 monorepo 中的 core 项目。
 * 生产模式优先使用已安装的 CLI，否则使用 electron-builder extraResources 中的 bundled core。
 */
export function getCorePath(): string {
  if (process.env.NODE_ENV === 'development')
    return 'uv'

  if (checkPipPackage())
    return 'Final2x-core'

  return path.join(
    app.getAppPath(),
    '..',
    'Final2x-core',
    process.platform === 'win32' ? 'Final2x-core.exe' : 'Final2x-core',
  )
}

export function getCoreArgs(): string[] {
  if (process.env.NODE_ENV === 'development')
    return ['run', '--project', path.join(app.getAppPath(), 'core'), 'Final2x-core']

  return []
}

export function checkPipPackage(): boolean {
  const result = spawnSync('Final2x-core', ['-h'])

  return result.status === 0
}
