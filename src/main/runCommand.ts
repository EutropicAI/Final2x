import type { Final2xCoreConfig } from '@shared/type/core'
import type { IpcMainEvent } from 'electron'
import type { ChildProcessWithoutNullStreams } from 'node:child_process'
import { spawn } from 'node:child_process'
import { once } from 'node:events'
import { IpcChannelOn } from '@shared/const/ipc'
import kill from 'tree-kill'
import { getCoreArgs, getCorePath } from './getCorePath'

let child: ChildProcessWithoutNullStreams | null = null

export async function runCommand(event: IpcMainEvent, coreConfig: Final2xCoreConfig): Promise<void> {
  let config_json = JSON.stringify(coreConfig.config)
  // eslint-disable-next-line node/prefer-global/buffer
  config_json = Buffer.from(config_json, 'utf8').toString('base64')

  const resourceUrl = getCorePath()
  const args = [...getCoreArgs(), '-b', config_json]

  if (!coreConfig.options.open_output_folder)
    args.push('-n')

  console.log(resourceUrl, args)

  const runningChild = spawn(resourceUrl, args)
  child = runningChild

  runningChild.stdout.on('data', (data) => {
    event.sender.send(IpcChannelOn.COMMAND_STDOUT, data.toString())
  })

  runningChild.stderr.on('data', (data) => {
    event.sender.send(IpcChannelOn.COMMAND_STDERR, data.toString())
  })

  try {
    const [code] = await once(runningChild, 'close')
    event.sender.send(IpcChannelOn.COMMAND_CLOSE, code)
    console.log(`Child process exited with code: ${code}`)
  }
  catch (error) {
    event.sender.send(IpcChannelOn.COMMAND_STDERR, `${error}\n`)
    event.sender.send(IpcChannelOn.COMMAND_CLOSE, 1)
  }
  finally {
    if (child === runningChild)
      child = null
  }
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
