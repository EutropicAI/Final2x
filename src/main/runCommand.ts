import type { IpcMainEvent } from 'electron'
import type { ChildProcessWithoutNullStreams } from 'node:child_process'
import { spawn } from 'node:child_process'
import { once } from 'node:events'
import { IpcChannelOn } from '@shared/const/ipc'
import kill from 'tree-kill'
import { getCorePath } from './getCorePath'

let child: ChildProcessWithoutNullStreams | null = null

export async function runCommand(
  event: IpcMainEvent,
  config_json: string,
  openOutputFolder: boolean,
): Promise<void> {
  // ---- 还是直接传base64吧
  // config_json = JSON.stringify(config_json) // 转义转义
  // ----
  // eslint-disable-next-line node/prefer-global/buffer
  config_json = Buffer.from(config_json, 'utf8').toString('base64')

  const resourceUrl = getCorePath()

  let command = `"${resourceUrl}" -b ${config_json}`

  if (!openOutputFolder) {
    command += ' -n'
  }

  console.log(command)

  child = spawn(command, { shell: true })

  child.stdout.on('data', (data) => {
    event.sender.send(IpcChannelOn.COMMAND_STDOUT, data.toString())
  })

  child.stderr.on('data', (data) => {
    event.sender.send(IpcChannelOn.COMMAND_STDERR, data.toString())
  })

  const [code] = await once(child, 'close')
  event.sender.send(IpcChannelOn.COMMAND_CLOSE, code)
  console.log(`Child process exited with code: ${code}`)

  child = null
}

export async function killCommand(): Promise<void> {
  if (!child || !child.pid) {
    console.error('Could not find child process, nothing to kill.')
    return
  }
  const pid = child.pid

  console.log(`Kill child process with pid: ${pid}`)

  await new Promise<void>((resolve) => {
    kill(pid, (err) => {
      if (err) {
        console.error(`Failed to kill process: ${err.message}`)
      }
      else {
        console.log('Process killed successfully')
      }
      if (child && child.pid === pid) {
        child = null
      }
      resolve()
    })
  })
}
