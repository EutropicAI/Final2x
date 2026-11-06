import path from 'node:path'
import { dialog } from 'electron'

// Electron 43+ opens dialogs in Downloads unless defaultPath is set
let lastUsedPath: string | undefined

/**
 * @description Open a directory or file/multiple files
 * @param _ Unused parameter, can be used for context in future
 * @param p The properties of the dialog
 */
export async function openDirectory(_, p: Array<'openFile' | 'openDirectory' | 'multiSelections'>): Promise<Array<string>> {
  try {
    const { canceled, filePaths } = await dialog.showOpenDialog({ defaultPath: lastUsedPath, properties: p })
    if (canceled)
      return []

    if (filePaths.length > 0)
      lastUsedPath = path.dirname(filePaths[0])

    return filePaths
  }
  catch (error) {
    console.error('Error opening directory dialog:', error)
    return []
  }
}
